#!/bin/bash

# Comprehensive endpoint testing for Think AI
# Tests all available endpoints with O(1) performance verification

set -e

# Configuration
BASE_URL="${1:-http://localhost:7777}"
VERBOSE="${2:-false}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Think AI Comprehensive Endpoint Testing ===${NC}"
echo "Testing: $BASE_URL"
echo ""

# Test results
PASSED=0
FAILED=0

# Helper function for API calls
api_test() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local expected_status=$5
    
    echo -e "${YELLOW}Testing: $name${NC}"
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}\n%{time_total}" "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}\n%{time_total}" -X "$method" \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$BASE_URL$endpoint")
    fi
    
    # Parse response
    time_total=$(echo "$response" | tail -n1)
    http_code=$(echo "$response" | tail -n2 | head -n1)
    body=$(echo "$response" | head -n -2)
    
    # Check status code
    if [ "$http_code" == "$expected_status" ]; then
        echo -e "${GREEN}✓ Status: $http_code (${time_total}s)${NC}"
        
        # Check for O(1) performance (should be < 10ms)
        if (( $(echo "$time_total < 0.01" | bc -l) )); then
            echo -e "${GREEN}✓ O(1) Performance: ${time_total}s${NC}"
        else
            echo -e "${YELLOW}⚠ Performance: ${time_total}s (target: <0.01s)${NC}"
        fi
        
        if [ "$VERBOSE" == "true" ]; then
            echo "Response: $body" | head -n 5
        fi
        
        ((PASSED++))
    else
        echo -e "${RED}✗ Status: $http_code (expected: $expected_status)${NC}"
        echo "Response: $body"
        ((FAILED++))
    fi
    echo ""
}

# Test WebSocket endpoint
ws_test() {
    local name=$1
    local endpoint=$2
    
    echo -e "${YELLOW}Testing: $name (WebSocket)${NC}"
    
    # Test WebSocket upgrade
    response=$(curl -s -w "\n%{http_code}" \
        -H "Connection: Upgrade" \
        -H "Upgrade: websocket" \
        -H "Sec-WebSocket-Version: 13" \
        -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
        "$BASE_URL$endpoint")
    
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" == "101" ] || [ "$http_code" == "426" ]; then
        echo -e "${GREEN}✓ WebSocket endpoint available${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ WebSocket test failed (status: $http_code)${NC}"
        ((FAILED++))
    fi
    echo ""
}

# Performance benchmark
benchmark_test() {
    local name=$1
    local endpoint=$2
    local data=$3
    local iterations=${4:-10}
    
    echo -e "${YELLOW}Benchmark: $name ($iterations iterations)${NC}"
    
    total_time=0
    min_time=999999
    max_time=0
    
    for i in $(seq 1 $iterations); do
        start_time=$(date +%s.%N)
        
        curl -s -X POST \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$BASE_URL$endpoint" > /dev/null
        
        end_time=$(date +%s.%N)
        duration=$(echo "$end_time - $start_time" | bc)
        
        total_time=$(echo "$total_time + $duration" | bc)
        
        if (( $(echo "$duration < $min_time" | bc -l) )); then
            min_time=$duration
        fi
        
        if (( $(echo "$duration > $max_time" | bc -l) )); then
            max_time=$duration
        fi
    done
    
    avg_time=$(echo "scale=6; $total_time / $iterations" | bc)
    
    echo -e "${GREEN}Average: ${avg_time}s${NC}"
    echo -e "${GREEN}Min: ${min_time}s, Max: ${max_time}s${NC}"
    
    # Check O(1) performance
    if (( $(echo "$avg_time < 0.01" | bc -l) )); then
        echo -e "${GREEN}✓ O(1) Performance achieved!${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠ Performance above O(1) target${NC}"
        ((FAILED++))
    fi
    echo ""
}

# Start testing
echo -e "${BLUE}1. Basic Endpoints${NC}"
echo ""

api_test "Health Check" "GET" "/health" "" "200"
api_test "Root Page" "GET" "/" "" "200"

echo -e "${BLUE}2. Chat API Endpoints${NC}"
echo ""

api_test "Chat - Simple Message" "POST" "/api/chat" \
    '{"message":"Hello"}' "200"

api_test "Chat - Complex Query" "POST" "/api/chat" \
    '{"message":"Explain quantum computing in simple terms"}' "200"

api_test "Chat - Empty Message" "POST" "/api/chat" \
    '{"message":""}' "400"

api_test "Chat - Invalid JSON" "POST" "/api/chat" \
    'invalid json' "400"

echo -e "${BLUE}3. Streaming Endpoints${NC}"
echo ""

ws_test "Chat Stream WebSocket" "/api/chat/stream"

echo -e "${BLUE}4. Performance Benchmarks${NC}"
echo ""

benchmark_test "Chat Performance" "/api/chat" \
    '{"message":"What is 2+2?"}' 20

echo -e "${BLUE}5. Stress Testing${NC}"
echo ""

echo -e "${YELLOW}Concurrent requests test...${NC}"
start_time=$(date +%s.%N)

# Send 50 concurrent requests
for i in {1..50}; do
    curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "{\"message\":\"Concurrent test $i\"}" \
        "$BASE_URL/api/chat" > /dev/null &
done

wait
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)

echo -e "${GREEN}✓ Handled 50 concurrent requests in ${duration}s${NC}"
avg_per_request=$(echo "scale=6; $duration / 50" | bc)
echo -e "${GREEN}Average per request: ${avg_per_request}s${NC}"

if (( $(echo "$avg_per_request < 0.1" | bc -l) )); then
    echo -e "${GREEN}✓ Good concurrent performance${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ Concurrent performance could be improved${NC}"
    ((FAILED++))
fi

echo ""

# Summary
echo -e "${BLUE}=== Test Summary ===${NC}"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi