const express = require('express');
const path = require('path');
const app = express();
const PORT = 8888;

// Usage metrics tracking
const metrics = {
  startTime: Date.now(),
  requests: {
    total: 0,
    chat: 0,
    audioTranscribe: 0,
    audioSynthesize: 0,
    health: 0,
    stats: 0
  },
  errors: {
    total: 0,
    byEndpoint: {}
  },
  responseTimes: {
    chat: [],
    audioTranscribe: [],
    audioSynthesize: []
  },
  activeSessions: new Set(),
  lastReset: Date.now()
};

// Serve static files from full-system/static directory
app.use(express.static('full-system/static'));

// Use raw parser for audio endpoints to preserve binary data
app.use('/api/audio', express.raw({ type: '*/*', limit: '50mb' }));

// Use JSON parser for other endpoints
app.use(express.json());

// Request tracking middleware
app.use((req, res, next) => {
  metrics.requests.total++;
  req.startTime = Date.now();
  
  // Track active sessions by IP
  if (req.ip) {
    metrics.activeSessions.add(req.ip);
  }
  
  // Clean up old response times (keep last 1000)
  Object.keys(metrics.responseTimes).forEach(endpoint => {
    if (metrics.responseTimes[endpoint].length > 1000) {
      metrics.responseTimes[endpoint] = metrics.responseTimes[endpoint].slice(-1000);
    }
  });
  
  next();
});

// Chat endpoint - proxy to Rust backend with retry logic
app.post('/api/chat', async (req, res) => {
  metrics.requests.chat++;
  const maxRetries = 2;
  let lastError = null;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const fetch = (await import('node-fetch')).default;
      const AbortController = globalThis.AbortController || (await import('abort-controller')).default;
      
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 70000); // 70s timeout
      
      const response = await fetch('http://localhost:9999/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(req.body),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        const data = await response.json();
        // Track response time
        const responseTime = Date.now() - req.startTime;
        metrics.responseTimes.chat.push(responseTime);
        return res.json(data);
      } else {
        throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      lastError = error;
      console.log(`Attempt ${attempt + 1} failed:`, error.message);
      
      // Wait before retry (except on last attempt)
      if (attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
  }
  
  // All retries failed - return error response
  metrics.errors.total++;
  metrics.errors.byEndpoint['chat'] = (metrics.errors.byEndpoint['chat'] || 0) + 1;
  const { message } = req.body;
  res.json({
    response: `I apologize, but I'm experiencing technical difficulties connecting to my AI systems right now. This could be due to high load or temporary connectivity issues. Please try again in a moment. Your message was: "${message}"`,
    timestamp: new Date().toISOString(),
    error: "backend_unavailable"
  });
});

// Audio endpoints - proxy to Rust backend
app.post('/api/audio/transcribe', async (req, res) => {
  metrics.requests.audioTranscribe++;
  try {
    const fetch = (await import('node-fetch')).default;
    
    // Forward headers but clean them up for the backend
    const forwardHeaders = {
      'content-type': req.headers['content-type'] || 'audio/webm',
      'content-length': req.headers['content-length'] || req.body.length.toString(),
    };
    
    // Add language header if provided
    if (req.headers['x-language']) {
      forwardHeaders['x-language'] = req.headers['x-language'];
    }
    
    console.log('Forwarding audio transcription request, content-type:', forwardHeaders['content-type'], 'size:', req.body.length);
    
    const response = await fetch('http://localhost:9999/api/audio/transcribe', {
      method: 'POST',
      headers: forwardHeaders,
      body: req.body // This is now raw binary data
    });
    
    if (response.ok) {
      const data = await response.json();
      // Track response time
      const responseTime = Date.now() - req.startTime;
      metrics.responseTimes.audioTranscribe.push(responseTime);
      return res.json(data);
    } else {
      const errorText = await response.text();
      console.error('Backend transcription error:', response.status, errorText);
      throw new Error(`Backend returned ${response.status}: ${errorText}`);
    }
  } catch (error) {
    console.error('Audio transcription proxy error:', error.message);
    metrics.errors.total++;
    metrics.errors.byEndpoint['audioTranscribe'] = (metrics.errors.byEndpoint['audioTranscribe'] || 0) + 1;
    res.status(500).json({ error: 'Transcription service unavailable', details: error.message });
  }
});

app.post('/api/audio/synthesize', async (req, res) => {
  metrics.requests.audioSynthesize++;
  try {
    const fetch = (await import('node-fetch')).default;
    
    // Parse raw body as JSON for synthesis requests
    let jsonData;
    try {
      jsonData = JSON.parse(req.body.toString());
    } catch (parseError) {
      console.error('Failed to parse synthesis request:', parseError.message);
      return res.status(400).json({ error: 'Invalid JSON in request body' });
    }
    
    console.log('Forwarding audio synthesis request:', jsonData);
    
    const response = await fetch('http://localhost:9999/api/audio/synthesize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jsonData)
    });
    
    if (response.ok) {
      const audioBuffer = await response.buffer();
      res.set('Content-Type', 'audio/mpeg');
      // Track response time
      const responseTime = Date.now() - req.startTime;
      metrics.responseTimes.audioSynthesize.push(responseTime);
      return res.send(audioBuffer);
    } else {
      throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Audio synthesis proxy error:', error.message);
    metrics.errors.total++;
    metrics.errors.byEndpoint['audioSynthesize'] = (metrics.errors.byEndpoint['audioSynthesize'] || 0) + 1;
    res.status(500).json({ error: 'Synthesis service unavailable' });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  metrics.requests.health++;
  res.json({ status: 'ok', server: 'proxy' });
});

// Stats endpoint
app.get('/stats', async (req, res) => {
  metrics.requests.stats++;
  try {
    const fetch = (await import('node-fetch')).default;
    
    // Try to get stats from backend
    const response = await fetch('http://localhost:9999/stats');
    
    if (response.ok) {
      const data = await response.json();
      return res.json(data);
    } else {
      throw new Error(`Backend returned ${response.status}`);
    }
  } catch (error) {
    // If backend is not available, return proxy stats
    res.json({
      status: 'ok',
      server: 'proxy',
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      timestamp: new Date().toISOString(),
      metrics: {
        requests: metrics.requests,
        errors: metrics.errors,
        activeSessions: metrics.activeSessions.size
      }
    });
  }
});

// Metrics endpoint for dashboard
app.get('/api/metrics', (req, res) => {
  // Add CORS headers
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  const calculateAverage = (arr) => {
    if (arr.length === 0) return 0;
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  };

  const calculatePercentile = (arr, percentile) => {
    if (arr.length === 0) return 0;
    const sorted = [...arr].sort((a, b) => a - b);
    const index = Math.floor((percentile / 100) * sorted.length);
    return sorted[index] || 0;
  };

  // Calculate endpoint stats
  const endpointStats = {};
  const endpoints = ['chat', 'audioTranscribe', 'audioSynthesize'];
  
  endpoints.forEach(endpoint => {
    const responseTimes = metrics.responseTimes[endpoint] || [];
    endpointStats[`/api/${endpoint}`] = {
      total_calls: metrics.requests[endpoint] || 0,
      average_response_time: calculateAverage(responseTimes),
      p95_response_time: calculatePercentile(responseTimes, 95),
      error_count: metrics.errors.byEndpoint[endpoint] || 0
    };
  });

  // Add other endpoints
  endpointStats['/api/health'] = {
    total_calls: metrics.requests.health || 0,
    average_response_time: 5, // Health checks are fast
    p95_response_time: 10,
    error_count: 0
  };

  endpointStats['/stats'] = {
    total_calls: metrics.requests.stats || 0,
    average_response_time: 20,
    p95_response_time: 30,
    error_count: 0
  };

  const uptime = (Date.now() - metrics.startTime) / 1000;
  const memUsage = process.memoryUsage();
  const totalMem = require('os').totalmem();
  const freeMem = require('os').freemem();
  const cpuUsage = process.cpuUsage();

  res.json({
    system_metrics: {
      total_requests: metrics.requests.total,
      average_response_time: calculateAverage([
        ...metrics.responseTimes.chat,
        ...metrics.responseTimes.audioTranscribe,
        ...metrics.responseTimes.audioSynthesize
      ]),
      cpu_usage: parseFloat(((cpuUsage.user + cpuUsage.system) / 1000000 / uptime * 100).toFixed(2)),
      memory_usage: parseFloat(((totalMem - freeMem) / totalMem * 100).toFixed(2)),
      active_sessions: metrics.activeSessions.size,
      error_count: metrics.errors.total,
      audio_transcriptions: metrics.requests.audioTranscribe || 0,
      audio_syntheses: metrics.requests.audioSynthesize || 0,
      whatsapp_messages: 0, // Not implemented in proxy
      uptime_seconds: Math.floor(uptime)
    },
    user_metrics: {
      total_users: metrics.activeSessions.size,
      active_users: metrics.activeSessions.size,
      new_users_today: 0 // Would need persistent storage
    },
    service_health: {
      overall_status: metrics.errors.total > 100 ? 'Degraded' : 'Healthy',
      api_health: 'Healthy',
      audio_service_health: metrics.errors.byEndpoint['audioTranscribe'] > 10 || metrics.errors.byEndpoint['audioSynthesize'] > 10 ? 'Degraded' : 'Healthy',
      whatsapp_service_health: 'Unknown'
    },
    endpoint_stats: endpointStats
  });
});

// Fallback to index.html for SPA
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'full-system/static/index.html'));
});

app.listen(PORT, () => {
  console.log(`Proxy server running on port ${PORT}`);
  console.log(`Visit: http://localhost:${PORT}`);
});