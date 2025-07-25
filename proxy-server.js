const express = require('express');
const path = require('path');
const app = express();
const PORT = 8888;

// Serve static files from full-system/static directory
app.use(express.static('full-system/static'));
app.use(express.json());

// Chat endpoint - proxy to Rust backend with retry logic
app.post('/api/chat', async (req, res) => {
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
  const { message } = req.body;
  res.json({
    response: `I apologize, but I'm experiencing technical difficulties connecting to my AI systems right now. This could be due to high load or temporary connectivity issues. Please try again in a moment. Your message was: "${message}"`,
    timestamp: new Date().toISOString(),
    error: "backend_unavailable"
  });
});

// Audio endpoints - proxy to Rust backend
app.post('/api/audio/transcribe', async (req, res) => {
  try {
    const fetch = (await import('node-fetch')).default;
    
    const response = await fetch('http://localhost:9999/api/audio/transcribe', {
      method: 'POST',
      headers: {
        ...req.headers,
        'host': undefined // Remove host header to avoid conflicts
      },
      body: req.body
    });
    
    if (response.ok) {
      const data = await response.json();
      return res.json(data);
    } else {
      throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Audio transcription proxy error:', error.message);
    res.status(500).json({ error: 'Transcription service unavailable' });
  }
});

app.post('/api/audio/synthesize', async (req, res) => {
  try {
    const fetch = (await import('node-fetch')).default;
    
    const response = await fetch('http://localhost:9999/api/audio/synthesize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(req.body)
    });
    
    if (response.ok) {
      const audioBuffer = await response.buffer();
      res.set('Content-Type', 'audio/mpeg');
      return res.send(audioBuffer);
    } else {
      throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Audio synthesis proxy error:', error.message);
    res.status(500).json({ error: 'Synthesis service unavailable' });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', server: 'proxy' });
});

// Fallback to index.html for SPA
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'full-system/static/index.html'));
});

app.listen(PORT, () => {
  console.log(`Proxy server running on port ${PORT}`);
  console.log(`Visit: http://localhost:${PORT}`);
});