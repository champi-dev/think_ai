const WebSocket = require('ws');

console.log('Testing WebSocket connections...\n');

// Test 1: Direct connection to backend
console.log('1. Testing direct connection to backend WebSocket...');
const backendWs = new WebSocket('ws://localhost:8080/api/v1/ws');

backendWs.on('open', () => {
  console.log('✅ Backend WebSocket connected successfully!');
  backendWs.send(JSON.stringify({ type: 'test', message: 'Hello from test' }));
});

backendWs.on('message', (data) => {
  console.log('✅ Received message from backend:', data.toString());
});

backendWs.on('error', (error) => {
  console.log('❌ Backend WebSocket error:', error.message);
});

backendWs.on('close', () => {
  console.log('Backend WebSocket closed\n');
  
  // Test 2: Connection through proxy
  console.log('2. Testing connection through Next.js proxy...');
  const proxyWs = new WebSocket('ws://localhost:3000/ws');
  
  proxyWs.on('open', () => {
    console.log('✅ Proxy WebSocket connected successfully!');
    proxyWs.send(JSON.stringify({ type: 'test', message: 'Hello through proxy' }));
  });
  
  proxyWs.on('message', (data) => {
    console.log('✅ Received message through proxy:', data.toString());
  });
  
  proxyWs.on('error', (error) => {
    console.log('❌ Proxy WebSocket error:', error.message);
  });
  
  proxyWs.on('close', () => {
    console.log('Proxy WebSocket closed');
    process.exit(0);
  });
});

// Give it 5 seconds to test
setTimeout(() => {
  console.log('\nTest timeout reached');
  process.exit(0);
}, 5000);