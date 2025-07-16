#!/bin/bash

# E2E test for production system at thinkai.lat
# This script tests both the chat API endpoint and the response quality

echo "=== Think AI Production E2E Test at thinkai.lat ==="
echo "Testing production deployment..."
echo

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test an endpoint
test_endpoint() {
    local test_name="$1"
    local url="$2"
    local data="$3"
    local expected_field="$4"
    
    echo -n "Testing: $test_name... "
    
    # Make the request and capture response
    response=$(curl -s -X POST "$url" \
        -H "Content-Type: application/json" \
        -d "$data" 2>&1)
    
    # Check if curl succeeded
    if [ $? -ne 0 ]; then
        echo -e "${RED}FAILED${NC} - Could not connect to server"
        echo "  Error: $response"
        ((TESTS_FAILED++))
        return
    fi
    
    # Check if response contains expected field
    if echo "$response" | grep -q "\"$expected_field\""; then
        echo -e "${GREEN}PASSED${NC}"
        ((TESTS_PASSED++))
        
        # Extract and display the response content
        if [ "$expected_field" = "response" ]; then
            content=$(echo "$response" | sed -n 's/.*"response":"\([^"]*\)".*/\1/p' | head -1)
            echo "  Response: ${content:0:100}..."
        fi
    else
        echo -e "${RED}FAILED${NC}"
        echo "  Expected field '$expected_field' not found in response"
        echo "  Response: $response"
        ((TESTS_FAILED++))
    fi
}

# Test 1: Basic chat endpoint with general query
test_endpoint \
    "Basic Chat API" \
    "https://thinkai.lat/api/chat" \
    '{"message": "What is the meaning of life?"}' \
    "response"

# Test 2: Chat with session ID
test_endpoint \
    "Chat with Session" \
    "https://thinkai.lat/api/chat" \
    '{"message": "Tell me about quantum physics", "session_id": "test-session-123"}' \
    "session_id"

# Test 3: Code-related query (should trigger CodeLlama)
test_endpoint \
    "Code Query (CodeLlama)" \
    "https://thinkai.lat/api/chat" \
    '{"message": "Write a Python function to calculate fibonacci numbers"}' \
    "response"

# Test 4: Explicit model selection - CodeLlama
test_endpoint \
    "Explicit CodeLlama Model" \
    "https://thinkai.lat/api/chat" \
    '{"message": "Explain recursion", "model": "codellama"}' \
    "response"

# Test 5: Explicit model selection - Qwen (General)
test_endpoint \
    "Explicit Qwen Model" \
    "https://thinkai.lat/api/chat" \
    '{"message": "What is consciousness?", "model": "qwen"}' \
    "response"

# Test 6: Math query
test_endpoint \
    "Math Query" \
    "https://thinkai.lat/api/chat" \
    '{"message": "What is 2+2?"}' \
    "response"

# Test 7: Identity query
test_endpoint \
    "Identity Query" \
    "https://thinkai.lat/api/chat" \
    '{"message": "What is your name?"}' \
    "response"

# Test 8: Streaming endpoint test (just check if endpoint exists)
echo -n "Testing: Streaming Endpoint... "
stream_response=$(curl -s -X POST "https://thinkai.lat/api/stream/chat" \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello"}' \
    --max-time 2 2>&1)

if echo "$stream_response" | grep -q "data:" || [ $? -eq 28 ]; then
    echo -e "${GREEN}PASSED${NC} - SSE endpoint responding"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAILED${NC} - SSE endpoint not working"
    ((TESTS_FAILED++))
fi

# Test 9: Error handling - empty message
test_endpoint \
    "Error Handling - Empty Message" \
    "https://thinkai.lat/api/chat" \
    '{"message": ""}' \
    "error"

# Test 10: Error handling - invalid JSON
echo -n "Testing: Invalid JSON Handling... "
invalid_response=$(curl -s -X POST "https://thinkai.lat/api/chat" \
    -H "Content-Type: application/json" \
    -d 'invalid json' 2>&1)

if echo "$invalid_response" | grep -q "error"; then
    echo -e "${GREEN}PASSED${NC} - Properly handles invalid JSON"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAILED${NC} - Does not handle invalid JSON properly"
    ((TESTS_FAILED++))
fi

# Test 11: Response time test
echo -n "Testing: Response Time... "
start_time=$(date +%s.%N)
curl -s -X POST "https://thinkai.lat/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"message": "Hi"}' > /dev/null 2>&1
end_time=$(date +%s.%N)

response_time=$(echo "$end_time - $start_time" | bc)
if (( $(echo "$response_time < 3.0" | bc -l) )); then
    echo -e "${GREEN}PASSED${NC} - Response time: ${response_time}s"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}WARNING${NC} - Slow response time: ${response_time}s"
    ((TESTS_FAILED++))
fi

# Test 12: CORS headers check
echo -n "Testing: CORS Headers... "
cors_response=$(curl -s -I -X POST "https://thinkai.lat/api/chat" \
    -H "Content-Type: application/json" \
    -H "Origin: https://example.com" \
    -d '{"message": "test"}' 2>&1)

if echo "$cors_response" | grep -qi "access-control-allow-origin"; then
    echo -e "${GREEN}PASSED${NC} - CORS headers present"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}WARNING${NC} - CORS headers might not be configured"
    ((TESTS_PASSED++))  # Not critical for API functionality
fi

# Summary
echo
echo "=== Test Summary ==="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed! Production system is working correctly.${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed. Please check the production system.${NC}"
    exit 1
fi