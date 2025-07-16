const { ThinkAI } = require('thinkai-quantum');

async function debugTest() {
    console.log('🔍 Debug Test');
    console.log('=============\n');

    const client = new ThinkAI({
        baseURL: 'https://thinkai.lat',
        debug: true
    });

    // Test 1: Check code generation response
    console.log('Test 1: Code Generation');
    try {
        const response = await client.chat({
            query: 'Write a Python fibonacci function',
            model: 'codellama',
            sessionId: 'debug-code'
        });
        console.log('Response:', JSON.stringify(response, null, 2));
        console.log('\nChecking for code markers:');
        console.log('Contains "def":', response.response.includes('def'));
        console.log('Contains "fibonacci":', response.response.toLowerCase().includes('fibonacci'));
        console.log('Response length:', response.response.length);
    } catch (error) {
        console.error('Error:', error.message);
    }

    // Test 2: Check health endpoint
    console.log('\n\nTest 2: Health Check');
    try {
        const health = await client.getHealth();
        console.log('Health:', JSON.stringify(health, null, 2));
    } catch (error) {
        console.error('Error:', error.message);
        if (error.details) {
            console.error('Details:', error.details);
        }
    }

    // Test 3: Check stats endpoint
    console.log('\n\nTest 3: Stats');
    try {
        const stats = await client.getStats();
        console.log('Stats:', JSON.stringify(stats, null, 2));
    } catch (error) {
        console.error('Error:', error.message);
        if (error.details) {
            console.error('Details:', error.details);
        }
    }
}

debugTest().catch(console.error);