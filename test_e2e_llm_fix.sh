#!/bin/bash
set -e

echo "=== End-to-End Test for LLM Initialization Fix ==="

PORT=5555

# Kill any existing process on port
echo "Cleaning up port $PORT..."
lsof -ti:$PORT | xargs kill -9 2>/dev/null || true

# Start server
echo "Starting server on port $PORT..."
RUST_LOG=info ./target/release/think-ai-server --port $PORT &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Function to test a query
test_query() {
    local query="$1"
    local description="$2"
    
    echo -e "\n--- Testing: $description ---"
    echo "Query: $query"
    
    response=$(curl -s -X POST http://localhost:$PORT/api/chat \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\"}" | jq -r '.response')
    
    if [[ "$response" == *"Knowledge engine LLM not initialized"* ]]; then
        echo "❌ FAILED: Got LLM initialization error!"
        echo "Response: $response"
        return 1
    else
        echo "✅ SUCCESS: No LLM error"
        echo "Response preview: ${response:0:100}..."
        return 0
    fi
}

# Run tests
echo -e "\n=== Running Test Queries ==="

failed=0

test_query "hello" "Simple greeting" || ((failed++))
test_query "what is consciousness" "Philosophical query" || ((failed++))
test_query "explain relativity" "Scientific query" || ((failed++))
test_query "how do computers work" "Technical query" || ((failed++))
test_query "what is the meaning of life" "Deep philosophical query" || ((failed++))
test_query "tell me about evolution" "Biology query" || ((failed++))
test_query "xyz123 random gibberish" "Unknown query" || ((failed++))

# Test with session context
SESSION_ID=$(uuidgen)
echo -e "\n--- Testing with conversation context ---"
echo "Session ID: $SESSION_ID"

# First message
curl -s -X POST http://localhost:$PORT/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"hello\", \"session_id\": \"$SESSION_ID\"}" > /dev/null

# Second message with context
response=$(curl -s -X POST http://localhost:$PORT/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"what is AI\", \"session_id\": \"$SESSION_ID\"}" | jq -r '.response')

if [[ "$response" == *"Knowledge engine LLM not initialized"* ]]; then
    echo "❌ FAILED: Got LLM error with conversation context!"
    ((failed++))
else
    echo "✅ SUCCESS: Context handling works without LLM error"
fi

# Clean up
kill $SERVER_PID 2>/dev/null || true

# Summary
echo -e "\n=== Test Summary ==="
if [ $failed -eq 0 ]; then
    echo "✅ ALL TESTS PASSED!"
    echo "The LLM initialization issue has been fixed."
else
    echo "❌ $failed tests failed"
    exit 1
fi