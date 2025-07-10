#!/bin/bash

echo "=== Debugging Qwen Integration ==="
echo

# Test 1: Check if Ollama is running
echo "1. Testing Ollama connectivity..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama is not running"
    exit 1
fi

# Test 2: Test Qwen models directly
echo
echo "2. Testing Qwen models directly..."
echo "Testing qwen2.5:1.5b..."
RESULT_1_5B=$(curl -s http://localhost:11434/api/generate -d '{"model": "qwen2.5:1.5b", "prompt": "Say hello", "stream": false}' | jq -r .response 2>/dev/null)
if [ -n "$RESULT_1_5B" ]; then
    echo "✅ qwen2.5:1.5b works"
else
    echo "❌ qwen2.5:1.5b failed"
fi

echo "Testing qwen2.5:3b..."
RESULT_3B=$(curl -s http://localhost:11434/api/generate -d '{"model": "qwen2.5:3b", "prompt": "Say hello", "stream": false}' | jq -r .response 2>/dev/null)
if [ -n "$RESULT_3B" ]; then
    echo "✅ qwen2.5:3b works"
else
    echo "❌ qwen2.5:3b failed"
fi

# Test 3: Check if Think AI server is running
echo
echo "3. Testing Think AI server..."
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Think AI server is running"
else
    echo "❌ Think AI server is not running"
fi

# Test 4: Test Think AI API with detailed response
echo
echo "4. Testing Think AI API endpoint..."
echo "Request: {\"message\": \"What is quantum computing?\"}"
echo
echo "Response:"
RESPONSE=$(curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "What is quantum computing?"}' 2>&1)

echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"

# Test 5: Check server logs for errors
echo
echo "5. Checking for recent errors in server output..."
echo "(Run 'journalctl -u think-ai-full -n 50' if using systemd, or check terminal output)"

# Test 6: Simple Rust test program for Qwen client
echo
echo "6. Creating test program for Qwen client..."
cat > /tmp/test_qwen.rs << 'EOF'
use think_ai_qwen::{QwenClient, QwenRequest};

#[tokio::main]
async fn main() {
    println!("Testing Qwen client...");
    
    let client = QwenClient::new();
    let request = QwenRequest {
        query: "What is 2+2?".to_string(),
        context: None,
        system_prompt: Some("You are a helpful AI assistant.".to_string()),
    };
    
    match client.generate(request).await {
        Ok(response) => {
            println!("✅ Success!");
            println!("Response: {}", response.content);
            println!("Tokens: {:?}", response.usage);
        }
        Err(e) => {
            println!("❌ Error: {}", e);
        }
    }
}
EOF

echo "Test program created at /tmp/test_qwen.rs"
echo "To run it: cd /home/administrator/think_ai && cargo run --bin test_qwen"

echo
echo "=== Summary ==="
echo "If the Qwen models work directly but fail in Think AI:"
echo "1. Check if the QwenClient is configured correctly"
echo "2. Look for timeout issues (3b model takes longer)"
echo "3. Check for JSON parsing errors in the response"
echo "4. Verify the streaming flag is set correctly"