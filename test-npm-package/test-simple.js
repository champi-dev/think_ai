const { ThinkAI } = require('thinkai-quantum');

async function testSimple() {
    console.log('🧪 Testing ThinkAI npm package - Simple Test');
    console.log('===========================================\n');

    const client = new ThinkAI({
        baseURL: 'https://thinkai.lat'
    });

    try {
        // Test with proper request format
        console.log('Test: Sending chat request with proper format...');
        const response = await client.chat({
            query: 'What is 2+2?',
            sessionId: 'test-' + Date.now()
        });
        console.log('✅ Success! Response:', response);
    } catch (error) {
        console.error('❌ Failed:', error.message);
        if (error.response) {
            console.error('Status:', error.response.status);
            console.error('Data:', error.response.data);
        }
    }
}

testSimple();