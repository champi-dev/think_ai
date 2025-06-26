#!/bin/bash

echo "🚀 Testing Production Deployment"
echo "================================"

if [ -z "$1" ]; then
    echo "Usage: ./test_production.sh <production-url>"
    echo "Example: ./test_production.sh https://think-ai-api-production.up.railway.app"
    exit 1
fi

PROD_URL=$1
PASSED=0
FAILED=0

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

test_endpoint() {
    local name=$1
    local url=$2
    local expected=$3
    
    echo -n "Testing $name... "
    response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null)
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | head -n -1)
    
    if [[ $http_code == "200" ]] && [[ $body == *"$expected"* ]]; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $http_code)"
        ((FAILED++))
    fi
}

echo "Testing: $PROD_URL"
echo ""

# 1. Health check
test_endpoint "Health Check" "$PROD_URL/health" "OK"

# 2. Stats API
echo -n "Testing Stats API... "
stats=$(curl -s "$PROD_URL/api/stats")
if echo "$stats" | jq -e '.status == "healthy"' >/dev/null 2>&1; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    ((FAILED++))
fi

# 3. Chat API
echo -n "Testing Chat API... "
chat_response=$(curl -s -X POST "$PROD_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "Hello"}')
    
if echo "$chat_response" | jq -e '.response' >/dev/null 2>&1; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    ((FAILED++))
fi

# 4. Response Time
echo -n "Testing Response Time... "
response_time=$(echo "$chat_response" | jq -r '.response_time_ms' 2>/dev/null)
if (( $(echo "$response_time < 10" | bc -l) )); then
    echo -e "${GREEN}✓ PASSED${NC} (${response_time}ms)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (${response_time}ms > 10ms)"
    ((FAILED++))
fi

# 5. Webapp
test_endpoint "Webapp" "$PROD_URL/" "Think AI"

# 6. No Next.js
echo -n "Checking for Next.js (should fail)... "
next_check=$(curl -s -o /dev/null -w "%{http_code}" "$PROD_URL/_next/static/")
if [[ $next_check == "404" ]]; then
    echo -e "${GREEN}✓ PASSED${NC} (No Next.js)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (Next.js detected!)"
    ((FAILED++))
fi

echo ""
echo "======================================"
echo "Production Test Summary"
echo "======================================"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"

if [[ $FAILED -eq 0 ]]; then
    echo -e "\n${GREEN}✅ Production deployment is working correctly!${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Production deployment has issues!${NC}"
    exit 1
fi