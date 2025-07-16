const { ThinkAI } = require('thinkai-quantum');

async function testAPI() {
    console.log('🧪 Testing ThinkAI npm package v1.0.7');
    console.log('=====================================\n');

    try {
        // Test 1: Create client with production URL
        console.log('Test 1: Creating ThinkAI client...');
        const client = new ThinkAI({
            baseURL: 'https://thinkai.lat'
        });
        console.log('✅ Client created successfully\n');

        // Test 2: Send a simple query
        console.log('Test 2: Sending simple query...');
        const response = await client.chat('What is 2+2?');
        console.log('Response:', response);
        console.log('✅ Simple query successful\n');

        // Test 3: Send a code query
        console.log('Test 3: Sending code query...');
        const codeResponse = await client.chat('Write a simple Python hello world', {
            model: 'codellama'
        });
        console.log('Code Response:', codeResponse);
        console.log('✅ Code query successful\n');

        // Test 4: Test with session
        console.log('Test 4: Testing session continuity...');
        const sessionId = 'test-session-' + Date.now();
        const response1 = await client.chat('My name is Alice', { sessionId });
        console.log('First response:', response1);
        
        const response2 = await client.chat('What is my name?', { sessionId });
        console.log('Second response:', response2);
        console.log('✅ Session continuity test complete\n');

        console.log('🎉 All API tests passed!');

    } catch (error) {
        console.error('❌ Test failed:', error.message);
        if (error.response) {
            console.error('Response status:', error.response.status);
            console.error('Response data:', error.response.data);
        }
        process.exit(1);
    }
}

// Run tests
testAPI();