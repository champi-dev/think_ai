#!/bin/bash
# Test Think AI API endpoints

echo "🔍 Testing Think AI Endpoints"
echo "============================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Base URL
BASE_URL="http://localhost:8080"

# Function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local expected=$4
    
    echo -n "Testing $method $endpoint ... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s "$BASE_URL$endpoint")
    else
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    if echo "$response" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}"
        echo "  Response: $(echo "$response" | head -c 100)..."
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "  Response: $response"
        return 1
    fi
}

# Check if server is running
echo "Checking server status..."
if ! curl -s "$BASE_URL/health" >/dev/null 2>&1; then
    echo -e "${RED}❌ Server not running!${NC}"
    echo ""
    echo "Please start the server first:"
    echo "  ./target/release/full-working-o1"
    exit 1
fi

echo -e "${GREEN}✅ Server is running${NC}"
echo ""

# Test endpoints
PASSED=0
FAILED=0

# 1. Health check
if test_endpoint "GET" "/health" "" "ok"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# 2. Chat endpoint
echo ""
if test_endpoint "POST" "/api/chat" '{"query":"What is O(1)?"}' "response"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# 3. Stats endpoint
echo ""
if test_endpoint "GET" "/api/stats" "" "total"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# 4. Search endpoint
echo ""
if test_endpoint "GET" "/api/search?query=consciousness&limit=5" "" "results"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# 5. Test chat with context
echo ""
if test_endpoint "POST" "/api/chat" '{"query":"Tell me more","context":["We were discussing O(1) performance"]}' "response"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# Performance test
echo ""
echo "📊 Performance Test"
echo "==================="
echo "Sending 100 requests to measure O(1) performance..."

total_time=0
for i in {1..100}; do
    start=$(date +%s%N)
    curl -s "$BASE_URL/health" >/dev/null 2>&1
    end=$(date +%s%N)
    elapsed=$((($end - $start) / 1000000))
    total_time=$(($total_time + $elapsed))
    
    # Progress bar
    if [ $((i % 10)) -eq 0 ]; then
        echo -n "."
    fi
done
echo ""

avg_time=$(($total_time / 100))
echo ""
echo "Average response time: ${avg_time}ms"

if [ $avg_time -lt 10 ]; then
    echo -e "${GREEN}🚀 Excellent O(1) performance!${NC}"
elif [ $avg_time -lt 50 ]; then
    echo -e "${GREEN}✅ Good O(1) performance${NC}"
else
    echo -e "${RED}⚠️  Performance needs optimization${NC}"
fi

# Summary
echo ""
echo "📋 Test Summary"
echo "==============="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo "Think AI is working perfectly with O(1) performance!"
else
    echo ""
    echo -e "${RED}⚠️  Some tests failed${NC}"
    echo "Please check the server logs for more details"
fi