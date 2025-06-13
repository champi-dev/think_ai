const WebSocket = require('ws');
const http = require('http');

console.log('=== WEBSOCKET COMPREHENSIVE TEST ===\n');
console.log('Test started at:', new Date().toISOString());
console.log('----------------------------------------\n');

// Test results storage
const results = {
  backendDirect: { status: 'pending', messages: [] },
  proxyConnection: { status: 'pending', messages: [] },
  apiHealth: { status: 'pending' }
};

// Test 1: API Health Check
console.log('1. Testing API Health...');
http.get('http://localhost:8080/api/v1/health', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    results.apiHealth = { status: 'success', data: JSON.parse(data) };
    console.log('✅ API Health Check:', JSON.stringify(results.apiHealth.data, null, 2));
  });
}).on('error', (err) => {
  results.apiHealth = { status: 'failed', error: err.message };
  console.log('❌ API Health Check failed:', err.message);
});

setTimeout(() => {
  // Test 2: Direct Backend WebSocket
  console.log('\n2. Testing Direct Backend WebSocket (ws://localhost:8080/api/v1/ws)...');
  const backendWs = new WebSocket('ws://localhost:8080/api/v1/ws');
  let backendConnected = false;

  backendWs.on('open', () => {
    backendConnected = true;
    results.backendDirect.status = 'connected';
    console.log('✅ Backend WebSocket CONNECTED');
    console.log('   Connection established at:', new Date().toISOString());
    
    // Send a test message
    const testMsg = { type: 'test', timestamp: Date.now() };
    console.log('   Sending test message:', JSON.stringify(testMsg));
    backendWs.send(JSON.stringify(testMsg));
  });

  backendWs.on('message', (data) => {
    const msg = data.toString();
    results.backendDirect.messages.push(msg);
    console.log('✅ Backend message received:', msg.substring(0, 100) + (msg.length > 100 ? '...' : ''));
  });

  backendWs.on('error', (error) => {
    results.backendDirect.status = 'error';
    results.backendDirect.error = error.message;
    console.log('❌ Backend WebSocket error:', error.message);
  });

  backendWs.on('close', (code, reason) => {
    console.log(`   Backend WebSocket closed. Code: ${code}, Reason: ${reason || 'none'}`);
  });

  // Wait for backend test to complete, then test proxy
  setTimeout(() => {
    if (backendConnected) {
      backendWs.close();
    }
    
    // Test 3: Proxy WebSocket
    console.log('\n3. Testing Proxy WebSocket (ws://localhost:3000/ws)...');
    const proxyWs = new WebSocket('ws://localhost:3000/ws');
    let proxyConnected = false;

    proxyWs.on('open', () => {
      proxyConnected = true;
      results.proxyConnection.status = 'connected';
      console.log('✅ Proxy WebSocket CONNECTED');
      console.log('   Connection established at:', new Date().toISOString());
      
      const testMsg = { type: 'test-proxy', timestamp: Date.now() };
      console.log('   Sending test message:', JSON.stringify(testMsg));
      proxyWs.send(JSON.stringify(testMsg));
    });

    proxyWs.on('message', (data) => {
      const msg = data.toString();
      results.proxyConnection.messages.push(msg);
      console.log('✅ Proxy message received:', msg.substring(0, 100) + (msg.length > 100 ? '...' : ''));
    });

    proxyWs.on('error', (error) => {
      results.proxyConnection.status = 'error';
      results.proxyConnection.error = error.message;
      console.log('❌ Proxy WebSocket error:', error.message);
    });

    proxyWs.on('close', (code, reason) => {
      console.log(`   Proxy WebSocket closed. Code: ${code}, Reason: ${reason || 'none'}`);
    });

    // Final results after 5 seconds
    setTimeout(() => {
      if (proxyConnected) {
        proxyWs.close();
      }
      
      console.log('\n========================================');
      console.log('FINAL TEST RESULTS:');
      console.log('========================================');
      console.log('\nAPI Health:', results.apiHealth.status === 'success' ? '✅ WORKING' : '❌ FAILED');
      console.log('Backend WebSocket:', results.backendDirect.status === 'connected' ? '✅ WORKING' : '❌ FAILED');
      console.log('Proxy WebSocket:', results.proxyConnection.status === 'connected' ? '✅ WORKING' : '❌ FAILED');
      
      console.log('\nDetailed Results:');
      console.log(JSON.stringify(results, null, 2));
      
      console.log('\n========================================');
      console.log('Test completed at:', new Date().toISOString());
      process.exit(0);
    }, 5000);
  }, 3000);
}, 1000);