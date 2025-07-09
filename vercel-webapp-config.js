// Configuration for Think AI 3D Webapp on Vercel
// This file configures the webapp to connect to your GPU server

const config = {
  // Production GPU server endpoint
  API_BASE_URL: process.env.THINK_AI_API_URL || 'http://69.197.178.37:8080',
  
  // WebSocket endpoint for real-time updates
  WS_URL: process.env.THINK_AI_WS_URL || 'ws://69.197.178.37:8080/ws',
  
  // Enable debug logging
  DEBUG: process.env.NODE_ENV !== 'production',
  
  // API endpoints
  endpoints: {
    chat: '/api/chat',
    compute: '/compute',
    search: '/search',
    stats: '/stats',
    knowledge: '/api/knowledge/stats'
  }
};

// Helper function to make API calls
async function callAPI(endpoint, data) {
  const url = `${config.API_BASE_URL}${config.endpoints[endpoint] || endpoint}`;
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error(`API call failed: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API call error:', error);
    throw error;
  }
}

// Export for use in the webapp
window.ThinkAIConfig = config;
window.ThinkAI = { callAPI };