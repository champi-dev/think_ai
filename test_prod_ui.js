// Test production UI functionality
const https = require('https');

async function testProdUI() {
    console.log('Testing Think AI Production UI...\n');
    
    // Test 1: Check if API endpoint is accessible
    console.log('1. Testing API endpoint:');
    
    const testMessage = JSON.stringify({
        message: "Hello, can you hear me?",
        session_id: "test-ui-" + Date.now()
    });
    
    const options = {
        hostname: 'thinkai.lat',
        port: 443,
        path: '/api/chat',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': testMessage.length,
            'Origin': 'https://thinkai.lat',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    };
    
    return new Promise((resolve) => {
        const req = https.request(options, (res) => {
            console.log(`   Status Code: ${res.statusCode}`);
            console.log(`   Headers: ${JSON.stringify(res.headers, null, 2)}`);
            
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                console.log(`   Response: ${data}\n`);
                
                if (res.statusCode !== 200) {
                    console.log('❌ API returned error status');
                } else {
                    try {
                        const json = JSON.parse(data);
                        if (json.response) {
                            console.log('✅ API is working correctly');
                            console.log(`   AI Response: "${json.response}"`);
                            console.log(`   Response time: ${json.response_time_ms}ms`);
                        }
                    } catch (e) {
                        console.log('❌ Invalid JSON response:', e.message);
                    }
                }
                resolve();
            });
        });
        
        req.on('error', (e) => {
            console.error(`❌ Request failed: ${e.message}`);
            resolve();
        });
        
        req.write(testMessage);
        req.end();
    });
}

// Run the test
testProdUI().then(() => {
    console.log('\nTest complete!');
});