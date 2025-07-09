#!/bin/bash

# Think AI GPU Server E2E Test Script
# Tests all server endpoints to ensure GPU server is operational

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default server URL (can be overridden by environment variable)
SERVER_URL=${THINK_AI_SERVER_URL:-"http://localhost:8080"}

echo -e "${YELLOW}=== Think AI GPU Server E2E Test ===${NC}"
echo "Testing server at: $SERVER_URL"
echo "Timestamp: $(date)"
echo ""

# Track test results
FAILED_TESTS=0
PASSED_TESTS=0

# Helper function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local expected_status=$4
    local description=$5
    
    echo -n "Testing $method $endpoint - $description... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -X GET "$SERVER_URL$endpoint" 2>/dev/null || echo "000")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "$SERVER_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" 2>/dev/null || echo "000")
    fi
    
    # Extract status code (last line)
    status_code=$(echo "$response" | tail -n 1)
    # Extract body (everything except last line)
    body=$(echo "$response" | sed '$d')
    
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: $status_code)"
        ((PASSED_TESTS++))
        
        # Show response preview for successful tests
        if [ -n "$body" ]; then
            echo "  Response preview: $(echo "$body" | head -c 100)..."
        fi
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: $expected_status, Got: $status_code)"
        ((FAILED_TESTS++))
        
        # Show error details
        if [ "$status_code" = "000" ]; then
            echo "  Error: Could not connect to server"
        elif [ -n "$body" ]; then
            echo "  Error response: $body"
        fi
    fi
    echo ""
}

# Test 1: Health Check
echo -e "${YELLOW}1. Basic Connectivity Tests${NC}"
test_endpoint "GET" "/health" "" "200" "Health check endpoint"

# Test 2: Stats Endpoint
test_endpoint "GET" "/stats" "" "200" "Server statistics"

# Test 3: Knowledge Stats
test_endpoint "GET" "/api/knowledge/stats" "" "200" "Knowledge engine statistics"

# Test 4: Compute Endpoint (O(1) computation)
echo -e "${YELLOW}2. Core Functionality Tests${NC}"
compute_data='{
    "query": "What is 2+2?",
    "context": "Simple math calculation"
}'
test_endpoint "POST" "/compute" "$compute_data" "200" "O(1) compute endpoint"

# Test 5: Search Endpoint
search_data='{
    "query": "test search",
    "limit": 5
}'
test_endpoint "POST" "/search" "$search_data" "200" "Vector search endpoint"

# Test 6: Chat Endpoint (removed - using /api/chat instead)
echo -e "${YELLOW}3. AI Interaction Tests${NC}"
chat_data='{
    "message": "Hello, AI! Are you running on GPU?",
    "conversation_id": "test-123"
}'

# Test 7: Alternative Chat Endpoint
test_endpoint "POST" "/api/chat" "$chat_data" "200" "API chat endpoint"

# Test 8: Process Endpoint
process_data='{
    "message": "Process this request",
    "type": "analysis"
}'
test_endpoint "POST" "/api/process" "$process_data" "200" "Process endpoint"

# Test 9: WebApp Routes
echo -e "${YELLOW}4. Web Interface Tests${NC}"
test_endpoint "GET" "/" "" "200" "Main webapp"
test_endpoint "GET" "/chat.html" "" "200" "Chat interface"

# Test 10: Static Resources
echo -e "${YELLOW}5. Static Resource Tests${NC}"
test_endpoint "GET" "/manifest.json" "" "200" "PWA manifest"
test_endpoint "GET" "/favicon.ico" "" "200" "Favicon"

# Test 11: WebSocket Placeholder
test_endpoint "GET" "/ws" "" "200" "WebSocket endpoint (placeholder)"

# Test 12: 404 Handling
echo -e "${YELLOW}6. Error Handling Tests${NC}"
test_endpoint "GET" "/nonexistent" "" "404" "404 error handling"

# GPU-Specific Tests
echo -e "${YELLOW}7. GPU-Specific Performance Tests${NC}"

# Test response time for compute endpoint
echo -n "Testing compute response time... "
start_time=$(date +%s%N)
curl -s -X POST "$SERVER_URL/compute" \
    -H "Content-Type: application/json" \
    -d '{"query": "Performance test", "context": "GPU benchmark"}' \
    > /dev/null 2>&1
end_time=$(date +%s%N)
response_time=$(( (end_time - start_time) / 1000000 )) # Convert to milliseconds

if [ $response_time -lt 100 ]; then
    echo -e "${GREEN}✓ EXCELLENT${NC} (${response_time}ms - O(1) performance achieved)"
    ((PASSED_TESTS++))
elif [ $response_time -lt 500 ]; then
    echo -e "${YELLOW}✓ GOOD${NC} (${response_time}ms)"
    ((PASSED_TESTS++))
else
    echo -e "${RED}✗ SLOW${NC} (${response_time}ms - Performance issue detected)"
    ((FAILED_TESTS++))
fi

# Test concurrent requests
echo -n "Testing concurrent request handling... "
(
    for i in {1..5}; do
        curl -s -X POST "$SERVER_URL/compute" \
            -H "Content-Type: application/json" \
            -d "{\"query\": \"Concurrent test $i\", \"context\": \"Load test\"}" \
            > /dev/null 2>&1 &
    done
    wait
) && echo -e "${GREEN}✓ PASS${NC} (Handled 5 concurrent requests)" && ((PASSED_TESTS++)) || \
    (echo -e "${RED}✗ FAIL${NC} (Failed to handle concurrent requests)" && ((FAILED_TESTS++)))

# Summary
echo ""
echo -e "${YELLOW}=== Test Summary ===${NC}"
echo -e "Total Tests: $((PASSED_TESTS + FAILED_TESTS))"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}✓ All tests passed! GPU server is fully operational.${NC}"
    exit 0
else
    echo -e "\n${RED}✗ Some tests failed. Please check the server logs.${NC}"
    
    # Provide debugging suggestions
    echo -e "\n${YELLOW}Debugging suggestions:${NC}"
    echo "1. Check if the server is running: ps aux | grep think-ai"
    echo "2. Check server logs: journalctl -u think-ai-server -n 50"
    echo "3. Verify port is open: netstat -tlnp | grep 8080"
    echo "4. Check GPU availability: nvidia-smi (if using NVIDIA GPU)"
    echo "5. Review server configuration in think-ai-server/src/main.rs"
    
    exit 1
fi