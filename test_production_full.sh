#!/bin/bash
set -e

echo "=== Full Production Test for Think AI ==="
echo "Testing site: https://thinkai.lat"
echo "Date: $(date)"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local expected_code=$3
    
    echo -n "Testing $name... "
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    
    if [ "$HTTP_CODE" = "$expected_code" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $HTTP_CODE)"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC} (Expected $expected_code, got $HTTP_CODE)"
        ((TESTS_FAILED++))
    fi
}

# Function to test API endpoint
test_api() {
    local name=$1
    local endpoint=$2
    local data=$3
    
    echo -n "Testing API $name... "
    
    RESPONSE=$(curl -s -X POST "https://thinkai.lat$endpoint" \
        -H "Content-Type: application/json" \
        -d "$data" 2>/dev/null || echo "ERROR")
    
    if [[ "$RESPONSE" == *"ERROR"* ]] || [[ -z "$RESPONSE" ]]; then
        echo -e "${RED}✗ FAIL${NC} (No response or error)"
        ((TESTS_FAILED++))
    else
        echo -e "${GREEN}✓ PASS${NC}"
        ((TESTS_PASSED++))
    fi
}

echo "=== Testing Static Pages ==="
test_endpoint "Homepage" "https://thinkai.lat/" "200"
test_endpoint "404 Page" "https://thinkai.lat/nonexistent" "404"
test_endpoint "Health Check" "https://thinkai.lat/health" "200"

echo ""
echo "=== Testing API Endpoints ==="
test_api "Chat (General)" "/api/chat" '{"message":"Hello","model":"qwen"}'
test_api "Chat (Code)" "/api/chat" '{"message":"Write hello world in Python","model":"codellama"}'
test_api "Chat with Web Search" "/api/chat" '{"message":"Latest AI news","use_web_search":true}'
test_api "Chat with Fact Check" "/api/chat" '{"message":"Is the earth flat?","fact_check":true}'

echo ""
echo "=== Testing WebSocket/Streaming ==="
echo -n "Testing streaming endpoint... "
STREAM_TEST=$(curl -s -X POST "https://thinkai.lat/chat/stream" \
    -H "Content-Type: application/json" \
    -d '{"message":"Hi","model":"qwen"}' \
    --max-time 5 2>&1 | head -1)

if [[ "$STREAM_TEST" == *"event:"* ]] || [[ "$STREAM_TEST" == *"data:"* ]]; then
    echo -e "${GREEN}✓ PASS${NC} (SSE stream working)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC} (No SSE stream detected)"
    ((TESTS_FAILED++))
fi

echo ""
echo "=== Testing UI Features ==="
echo -n "Checking for Web Search toggle... "
if curl -s https://thinkai.lat/ | grep -q "Web Search"; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo -n "Checking for Fact Check toggle... "
if curl -s https://thinkai.lat/ | grep -q "Fact Check"; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "=== System Status ==="
echo -n "Checking local server... "
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${RED}✗ Not responding${NC}"
fi

echo -n "Checking ngrok tunnel... "
if ps aux | grep -v grep | grep -q ngrok; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${RED}✗ Not running${NC}"
fi

echo -n "Checking systemd service... "
if systemctl is-active --quiet stable-server; then
    echo -e "${GREEN}✓ Active${NC}"
else
    SERVICE_STATUS=$(systemctl is-active stable-server)
    echo -e "${YELLOW}⚠ Status: $SERVICE_STATUS${NC}"
fi

echo ""
echo "=== Performance Test ==="
echo -n "Response time test... "
TIME=$(curl -o /dev/null -s -w '%{time_total}' https://thinkai.lat/health)
if (( $(echo "$TIME < 1.0" | bc -l) )); then
    echo -e "${GREEN}✓ PASS${NC} (${TIME}s)"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⚠ SLOW${NC} (${TIME}s)"
fi

echo ""
echo "=== Test Summary ==="
TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
echo "Total Tests: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✅ All tests passed! Production is working correctly.${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed. Please check the issues above.${NC}"
    exit 1
fi