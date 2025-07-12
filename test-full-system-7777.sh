#!/bin/bash

# Test script for Think AI Full System on port 7777

set -e

echo "🧪 Testing Think AI Full System on Port 7777"
echo "==========================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PORT=7777
BASE_URL="http://localhost:$PORT"

# Function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo -e "\n${YELLOW}Testing: $description${NC}"
    echo "  Method: $method"
    echo "  URL: $BASE_URL$endpoint"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$BASE_URL$endpoint" 2>/dev/null || echo "CURL_ERROR")
    else
        response=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X "$method" \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$BASE_URL$endpoint" 2>/dev/null || echo "CURL_ERROR")
    fi
    
    if [[ "$response" == "CURL_ERROR" ]]; then
        echo -e "  ${RED}✗ Failed: Could not connect to server${NC}"
        return 1
    fi
    
    http_code=$(echo "$response" | grep -oP 'HTTP_CODE:\K\d+' || echo "000")
    body=$(echo "$response" | sed '/HTTP_CODE:/d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "  ${GREEN}✓ Success: HTTP $http_code${NC}"
        if [ -n "$body" ]; then
            echo "  Response preview: $(echo "$body" | head -c 100)..."
        fi
    else
        echo -e "  ${RED}✗ Failed: HTTP $http_code${NC}"
        if [ -n "$body" ]; then
            echo "  Error: $body"
        fi
    fi
}

# Check if server is running
echo -e "\n${YELLOW}Checking if server is running on port $PORT...${NC}"
if ! lsof -ti:$PORT >/dev/null 2>&1; then
    echo -e "${RED}✗ No server found on port $PORT${NC}"
    echo -e "${YELLOW}Please run: ./run-full-system-7777.sh${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Server is running on port $PORT${NC}"

# Run tests
echo -e "\n${YELLOW}Running endpoint tests...${NC}"

# Test 1: Health check
test_endpoint "GET" "/health" "" "Health Check"

# Test 2: Main page
test_endpoint "GET" "/" "" "Main Web Interface"

# Test 3: Stats endpoint
test_endpoint "GET" "/stats" "" "System Statistics"

# Test 4: Chat endpoint
test_endpoint "POST" "/chat" '{"query":"What is O(1) performance?"}' "Chat API"

# Test 5: Alternative chat endpoint
test_endpoint "POST" "/api/chat" '{"query":"Hello Think AI"}' "Alternative Chat API"

# Performance test
echo -e "\n${YELLOW}Running performance test...${NC}"
echo "Sending 10 requests to measure response time..."

total_time=0
success_count=0

for i in {1..10}; do
    start_time=$(date +%s.%N)
    response=$(curl -s -X POST -H "Content-Type: application/json" \
        -d '{"query":"test"}' "$BASE_URL/chat" 2>/dev/null)
    end_time=$(date +%s.%N)
    
    if [ $? -eq 0 ]; then
        elapsed=$(echo "$end_time - $start_time" | bc)
        total_time=$(echo "$total_time + $elapsed" | bc)
        success_count=$((success_count + 1))
        echo -n "."
    else
        echo -n "x"
    fi
done

echo ""

if [ $success_count -gt 0 ]; then
    avg_time=$(echo "scale=3; $total_time / $success_count" | bc)
    echo -e "${GREEN}✓ Performance Test Complete${NC}"
    echo "  Successful requests: $success_count/10"
    echo "  Average response time: ${avg_time}s"
else
    echo -e "${RED}✗ Performance test failed - no successful requests${NC}"
fi

# Summary
echo -e "\n${YELLOW}========================================${NC}"
echo -e "${GREEN}Test Summary:${NC}"
echo -e "${YELLOW}========================================${NC}"
echo "Server URL: $BASE_URL"
echo "To stop the server: Press Ctrl+C in the server terminal"
echo "To view logs: Check backend_*.log and webapp_*.log files"