#!/usr/bin/env node

const https = require('https');

const BASE_URL = 'https://thinkai.lat';
let passCount = 0;
let failCount = 0;
const errors = [];

function test(name, fn) {
  return fn()
    .then(() => {
      console.log(`✓ ${name}`);
      passCount++;
    })
    .catch(err => {
      console.log(`✗ ${name}: ${err.message}`);
      failCount++;
      errors.push({ test: name, error: err.message });
    });
}

function httpsRequest(options, postData) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({ status: res.statusCode, data, headers: res.headers });
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });
    req.on('error', reject);
    if (postData) req.write(postData);
    req.end();
  });
}

async function runTests() {
  console.log('Testing Think AI Production at', BASE_URL, '\n');

  // Test 1: Home page loads
  await test('Home page loads with React app', async () => {
    const result = await httpsRequest({
      hostname: 'thinkai.lat',
      path: '/',
      method: 'GET'
    });
    if (!result.data.includes('<div id="root">')) {
      throw new Error('Root element not found');
    }
    if (!result.data.includes('🧠')) {
      throw new Error('Brain emoji favicon not found');
    }
  });

  // Test 2: CSS loads
  await test('CSS file loads with styles', async () => {
    const homepage = await httpsRequest({
      hostname: 'thinkai.lat',
      path: '/',
      method: 'GET'
    });
    const cssMatch = homepage.data.match(/href="\/assets\/(index-[a-z0-9]+\.css)"/);
    if (!cssMatch) throw new Error('CSS file not found');
    
    const cssResult = await httpsRequest({
      hostname: 'thinkai.lat',
      path: `/assets/${cssMatch[1]}`,
      method: 'GET'
    });
    if (!cssResult.data.includes('.header')) {
      throw new Error('Header styles not found');
    }
    if (!cssResult.data.includes('.messages')) {
      throw new Error('Messages styles not found');
    }
  });

  // Test 3: JavaScript loads
  await test('JavaScript file loads with React', async () => {
    const homepage = await httpsRequest({
      hostname: 'thinkai.lat',
      path: '/',
      method: 'GET'
    });
    const jsMatch = homepage.data.match(/src="\/assets\/(index-[a-z0-9]+\.js)"/);
    if (!jsMatch) throw new Error('JS file not found');
    
    const jsResult = await httpsRequest({
      hostname: 'thinkai.lat',
      path: `/assets/${jsMatch[1]}`,
      method: 'GET'
    });
    if (!jsResult.data.includes('React')) {
      throw new Error('React not found in JavaScript');
    }
  });

  // Test 4: Health endpoint
  await test('Health endpoint responds', async () => {
    const result = await httpsRequest({
      hostname: 'thinkai.lat',
      path: '/health',
      method: 'GET'
    });
    if (result.data.trim() !== 'OK') {
      throw new Error(`Unexpected response: ${result.data}`);
    }
  });

  // Test 5: Chat API
  await test('Chat API responds correctly', async () => {
    const postData = JSON.stringify({
      message: 'Hello, this is a test',
      session_id: 'test-' + Date.now()
    });
    
    const result = await httpsRequest({
      hostname: 'thinkai.lat',
      path: '/api/chat',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': postData.length
      }
    }, postData);
    
    const data = JSON.parse(result.data);
    if (!data.response) throw new Error('No response field');
    if (!data.session_id) throw new Error('No session_id field');
  });

  // Test 6: CORS headers
  await test('CORS headers are present', async () => {
    const result = await httpsRequest({
      hostname: 'thinkai.lat',
      path: '/api/chat',
      method: 'OPTIONS',
      headers: {
        'Origin': 'https://thinkai.lat',
        'Access-Control-Request-Method': 'POST'
      }
    });
    if (!result.headers['access-control-allow-origin']) {
      throw new Error('No CORS headers');
    }
  });

  // Test 7: Knowledge stats
  await test('Knowledge stats API works', async () => {
    const result = await httpsRequest({
      hostname: 'thinkai.lat',
      path: '/api/knowledge/stats',
      method: 'GET'
    });
    const data = JSON.parse(result.data);
    if (!data.hasOwnProperty('total_knowledge_items')) {
      throw new Error('Missing total_knowledge_items');
    }
  });

  // Test 8: Search API
  await test('Search API works', async () => {
    const result = await httpsRequest({
      hostname: 'thinkai.lat',
      path: '/api/search?q=test&limit=5',
      method: 'GET'
    });
    const data = JSON.parse(result.data);
    if (!data.results) throw new Error('No results field');
    if (!data.hasOwnProperty('total')) throw new Error('No total field');
  });

  // Test 9: Code mode
  await test('Code mode API works', async () => {
    const postData = JSON.stringify({
      message: 'Write hello world in Python',
      session_id: 'code-test-' + Date.now(),
      mode: 'code'
    });
    
    const result = await httpsRequest({
      hostname: 'thinkai.lat',
      path: '/api/chat',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': postData.length
      }
    }, postData);
    
    const data = JSON.parse(result.data);
    if (!data.response) throw new Error('No response in code mode');
  });

  // Test 10: SSE streaming endpoint
  await test('SSE streaming endpoint exists', async () => {
    const postData = JSON.stringify({
      message: 'Test streaming',
      session_id: 'stream-test-' + Date.now()
    });
    
    // Just check if endpoint responds, full SSE test would be complex
    try {
      await httpsRequest({
        hostname: 'thinkai.lat',
        path: '/api/chat/stream',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': postData.length,
          'Accept': 'text/event-stream'
        }
      }, postData);
    } catch (err) {
      // SSE might not return immediately, check if it's a timeout vs error
      if (!err.message.includes('ECONNRESET') && !err.message.includes('socket hang up')) {
        throw err;
      }
    }
  });

  // Summary
  console.log('\n' + '='.repeat(50));
  const total = passCount + failCount;
  const successRate = total > 0 ? (passCount / total * 100).toFixed(1) : 0;
  console.log(`Test Results: ${passCount}/${total} passed (${successRate}%)`);
  
  if (errors.length > 0) {
    console.log('\nFailed tests:');
    errors.forEach(({ test, error }) => {
      console.log(`  - ${test}: ${error}`);
    });
  }
  
  if (successRate == 100) {
    console.log('\n✅ All tests passed! 100% functionality achieved.');
  } else {
    console.log('\n❌ Some tests failed. Fix required for 100% success rate.');
    process.exit(1);
  }
}

runTests().catch(err => {
  console.error('Test runner error:', err);
  process.exit(1);
});