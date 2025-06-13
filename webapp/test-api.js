#!/usr/bin/env node

const WebSocket = require('ws');

async function testAPI() {
  console.log('Testing Think AI API...\n');
  
  // Test 1: Intelligence endpoint
  console.log('1. Testing /api/v1/intelligence...');
  try {
    const response = await fetch('http://localhost:8080/api/v1/intelligence');
    const data = await response.json();
    console.log('✓ Intelligence data:', data);
  } catch (error) {
    console.log('✗ Intelligence test failed:', error.message);
  }
  
  // Test 2: WebSocket connection
  console.log('\n2. Testing WebSocket connection...');
  const ws = new WebSocket('ws://localhost:8080/api/v1/ws');
  
  ws.on('open', () => {
    console.log('✓ WebSocket connected');
    
    // Test sending a message
    const testMessage = {
      type: 'query',
      data: { query: 'Hello, Think AI!' }
    };
    ws.send(JSON.stringify(testMessage));
    console.log('✓ Sent test message:', testMessage);
  });
  
  ws.on('message', (data) => {
    console.log('✓ Received message:', data.toString());
  });
  
  ws.on('error', (error) => {
    console.log('✗ WebSocket error:', error.message);
  });
  
  ws.on('close', () => {
    console.log('WebSocket closed');
  });
  
  // Test 3: Think endpoint
  console.log('\n3. Testing /api/v1/think...');
  try {
    const response = await fetch('http://localhost:8080/api/v1/think', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: 'What is consciousness?',
        context: {}
      })
    });
    const data = await response.json();
    console.log('✓ Think response:', JSON.stringify(data, null, 2));
  } catch (error) {
    console.log('✗ Think test failed:', error.message);
  }
  
  // Keep WebSocket open for a bit
  setTimeout(() => {
    ws.close();
    console.log('\n✓ All tests completed!');
    process.exit(0);
  }, 5000);
}

testAPI();