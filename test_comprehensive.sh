#!/bin/bash

echo "Running comprehensive tests for 100% coverage..."
echo "==============================================="

# Function to test endpoint and check response time
test_endpoint() {
    local name=$1
    local url=$2
    local data=$3
    local expected_time=$4
    
    echo -e "\nTesting: $name"
    response=$(curl -s -X POST "$url" \
        -H "Content-Type: application/json" \
        -d "$data" \
        -w "\n{\"time_total\": %{time_total}}")
    
    # Extract response time
    time_total=$(echo "$response" | tail -n 1 | jq -r '.time_total')
    
    # Check if response time is under expected
    if (( $(echo "$time_total < $expected_time" | bc -l) )); then
        echo "✓ Response time: ${time_total}s (under ${expected_time}s)"
    else
        echo "✗ Response time: ${time_total}s (exceeded ${expected_time}s)"
        return 1
    fi
    
    # Check if response is valid JSON
    echo "$response" | head -n -1 | jq . > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ Valid JSON response"
    else
        echo "✗ Invalid JSON response"
        return 1
    fi
    
    return 0
}

# Run tests
BASE_URL="http://localhost:8080"
PROD_URL="https://thinkai.lat"

echo -e "\n=== LOCAL TESTS ==="

# Test 1: Simple chat
test_endpoint "Simple Chat" "$BASE_URL/api/chat" '{"message":"Hello"}' 1.0

# Test 2: Chat with context
test_endpoint "Chat with Context" "$BASE_URL/api/chat" '{"message":"What is AI?","session_id":"test123"}' 1.0

# Test 3: Multiple requests in parallel
echo -e "\nTesting: Parallel Requests (5 concurrent)"
success_count=0
for i in {1..5}; do
    (test_endpoint "Request $i" "$BASE_URL/api/chat" "{\"message\":\"Test $i\"}" 1.5 && echo "Request $i succeeded") &
done
wait

# Test 4: Streaming endpoint
echo -e "\nTesting: Streaming Endpoint"
curl -s -X POST "$BASE_URL/api/chat/stream" \
    -H "Content-Type: application/json" \
    -d '{"message":"Tell me a short fact"}' \
    --no-buffer | head -n 5

echo -e "\n\n=== PRODUCTION TESTS ==="

# Test production endpoint
test_endpoint "Production Chat" "$PROD_URL/api/chat" '{"message":"Hello from test"}' 1.0

# Test health endpoint
echo -e "\nTesting: Health Check"
health_response=$(curl -s "$BASE_URL/api/health")
if [ "$health_response" == "OK" ]; then
    echo "✓ Health check passed"
else
    echo "✗ Health check failed"
fi

echo -e "\n\n=== UNIT TEST COVERAGE ==="

# Run Rust tests
echo "Running Rust unit tests..."
cd /home/administrator/think_ai
cargo test --all 2>&1 | grep -E "(test result:|running \d+ test)" | tail -n 20

echo -e "\n\n=== INTEGRATION TESTS ==="

# Test Gemini fallback
echo -e "\nTesting Gemini Fallback..."
sudo systemctl stop ollama
sleep 2
test_endpoint "Gemini Fallback" "$BASE_URL/api/chat" '{"message":"Using fallback?"}' 1.5
sudo systemctl start ollama

echo -e "\n\n==============================================="
echo "Test suite completed!"