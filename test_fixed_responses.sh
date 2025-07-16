#!/bin/bash

echo "=== Testing Fixed Response Components ==="
echo

# Start server
echo "Starting server..."
./target/release/think-ai-server > test_server.log 2>&1 &
SERVER_PID=$!
sleep 3

# Function to test a query
test_query() {
    local query="$1"
    local expected_keyword="$2"
    
    echo "Query: $query"
    response=$(curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\"}" | jq -r '.response')
    
    if [[ "$response" == *"$expected_keyword"* ]]; then
        echo "✓ SUCCESS: Response contains '$expected_keyword'"
        echo "Response preview: ${response:0:100}..."
    else
        echo "✗ FAIL: Response does not contain '$expected_keyword'"
        echo "Response: $response"
    fi
    echo
}

# Test cases
echo "=== Running Tests ==="
echo

test_query "explain the theory of relativity" "Einstein"
test_query "what is quantum mechanics" "quantum"
test_query "what is consciousness" "consciousness"
test_query "how do computers work" "CPU"
test_query "what is the meaning of life" "philosophy"
test_query "what is coding like" "comparison"

# Check for the error message
echo "=== Checking for Error Message ==="
if grep -q "Knowledge engine LLM not initialized" test_server.log; then
    echo "✗ FAIL: Error message still appears in logs"
    grep "Knowledge engine LLM not initialized" test_server.log
else
    echo "✓ SUCCESS: No 'Knowledge engine LLM not initialized' errors found"
fi

# Cleanup
echo
echo "Cleaning up..."
kill $SERVER_PID 2>/dev/null
rm -f test_server.log

echo
echo "=== Test Complete ===
"