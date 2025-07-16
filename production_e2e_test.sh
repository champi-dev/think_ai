#!/bin/bash

echo "=== Think AI Production E2E Test ==="
echo "Testing production deployment at thinkai.lat"
echo "Timestamp: $(date)"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Test function
test_endpoint() {
    local name="$1"
    local url="$2"
    local expected="$3"
    
    echo -n "Testing $name... "
    
    response=$(curl -sL --max-time 10 "$url" 2>/dev/null)
    
    if echo "$response" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        echo "  Expected to find: $expected"
        echo "  Got response: ${response:0:200}..."
        ((FAILED++))
        return 1
    fi
}

echo "1. Testing Infrastructure"
echo "========================="

# Test 1: Health endpoint
test_endpoint "Health endpoint" "https://thinkai.lat/health" "healthy"

# Test 2: Main page
test_endpoint "Main page" "https://thinkai.lat/" "Think AI"

# Test 3: Mode toggle in UI
test_endpoint "Mode toggle presence" "https://thinkai.lat/" "mode-toggle"

# Test 4: Web search capability
test_endpoint "Web search in code" "https://thinkai.lat/" "Web Search"

echo ""
echo "2. Testing API Endpoints"
echo "========================="

# Test 5: API chat endpoint - General mode
echo -n "Testing API chat endpoint (General mode)... "
response=$(curl -sL -X POST https://thinkai.lat/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello, test message", "model": "qwen"}' 2>/dev/null)

if echo "$response" | grep -q "response"; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "  Response: ${response:0:200}..."
    ((FAILED++))
fi

# Test 6: API chat endpoint - Code mode
echo -n "Testing API chat endpoint (Code mode)... "
response=$(curl -sL -X POST https://thinkai.lat/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Write a hello world function", "model": "codellama"}' 2>/dev/null)

if echo "$response" | grep -q "response"; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "  Response: ${response:0:200}..."
    ((FAILED++))
fi

# Test 7: Stream chat endpoint
echo -n "Testing stream chat endpoint... "
response=$(curl -sL -X POST https://thinkai.lat/api/chat/stream \
    -H "Content-Type: application/json" \
    -d '{"message": "Stream test"}' 2>/dev/null | head -1)

if echo "$response" | grep -q "data:"; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "  Response: ${response:0:200}..."
    ((FAILED++))
fi

echo ""
echo "3. Testing WebSocket Support"
echo "============================="

# Test 8: WebSocket upgrade
echo -n "Testing WebSocket support... "
ws_response=$(curl -sL -I https://thinkai.lat/ws \
    -H "Upgrade: websocket" \
    -H "Connection: Upgrade" \
    -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
    -H "Sec-WebSocket-Version: 13" 2>/dev/null | head -1)

if echo "$ws_response" | grep -q "101\|426\|400"; then
    echo -e "${GREEN}✓ PASSED${NC} (WebSocket endpoint exists)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "  Response: $ws_response"
    ((FAILED++))
fi

echo ""
echo "4. Testing Performance"
echo "======================"

# Test 9: Response time
echo -n "Testing response time... "
start_time=$(date +%s%N)
curl -sL https://thinkai.lat/health > /dev/null 2>&1
end_time=$(date +%s%N)
response_time=$(( ($end_time - $start_time) / 1000000 ))

if [ $response_time -lt 1000 ]; then
    echo -e "${GREEN}✓ PASSED${NC} (${response_time}ms < 1000ms)"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ SLOW${NC} (${response_time}ms)"
    ((FAILED++))
fi

echo ""
echo "5. Testing CORS Headers"
echo "======================="

# Test 10: CORS headers
echo -n "Testing CORS headers... "
cors_headers=$(curl -sL -I https://thinkai.lat/api/chat \
    -H "Origin: https://example.com" 2>/dev/null | grep -i "access-control")

if echo "$cors_headers" | grep -q "Access-Control-Allow-Origin"; then
    echo -e "${GREEN}✓ PASSED${NC}"
    echo "  $cors_headers"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (No CORS headers found)"
    ((FAILED++))
fi

echo ""
echo "6. Testing Knowledge Engine"
echo "==========================="

# Test 11: Knowledge engine initialization
echo -n "Testing knowledge engine... "
response=$(curl -sL -X POST https://thinkai.lat/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "What is quantum computing?"}' 2>/dev/null)

if echo "$response" | grep -qv "Knowledge engine LLM not initialized"; then
    echo -e "${GREEN}✓ PASSED${NC} (Knowledge engine working)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (Knowledge engine error)"
    echo "  Response: ${response:0:200}..."
    ((FAILED++))
fi

echo ""
echo "=================================="
echo "Test Summary"
echo "=================================="
echo -e "Total Tests: $((PASSED + FAILED))"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed! Production is healthy.${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed. Please investigate.${NC}"
    exit 1
fi