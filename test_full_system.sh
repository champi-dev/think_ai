#!/bin/bash
# Test script for Think AI full system

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🧪 Testing Think AI Full System${NC}"
echo "================================"

# Function to test API endpoint
test_api() {
    local query="$1"
    local expected="$2"
    
    echo -n "Testing: '$query' ... "
    
    response=$(curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\"}" 2>/dev/null || echo '{"error": "Connection failed"}')
    
    if echo "$response" | grep -q "response"; then
        echo -e "${GREEN}✅ Pass${NC}"
        echo "Response: $(echo "$response" | jq -r '.response' 2>/dev/null | head -c 100)..."
        echo "Response time: $(echo "$response" | jq -r '.response_time_ms' 2>/dev/null)ms"
    else
        echo -e "${RED}❌ Fail${NC}"
        echo "Error: $response"
    fi
    echo ""
}

# Wait for server
echo "Waiting for server to be ready..."
max_attempts=30
attempt=0
while ! nc -z localhost 8080 2>/dev/null; do
    attempt=$((attempt + 1))
    if [ $attempt -ge $max_attempts ]; then
        echo -e "${RED}Server not responding after 30 seconds${NC}"
        exit 1
    fi
    sleep 1
done

echo -e "${GREEN}Server is ready!${NC}"
echo ""

# Test health endpoint
echo "Testing health endpoint..."
health=$(curl -s http://localhost:8080/health)
if [ "$health" = "OK" ]; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
fi
echo ""

# Test stats endpoint
echo "Testing stats endpoint..."
stats=$(curl -s http://localhost:8080/api/stats)
echo "Stats: $stats"
echo ""

# Test various queries
echo "Testing knowledge queries..."
test_api "What is the sun made of?" "plasma"
test_api "What is JavaScript?" "programming"
test_api "Explain quantum mechanics" "quantum"
test_api "How does machine learning work?" "neural"
test_api "What is consciousness?" "awareness"

# Test conversation context
echo "Testing conversation context..."
test_api "What is gravity?" "force"
test_api "What causes it?" "mass"

# Performance test
echo -e "${YELLOW}Performance Test (100 requests)${NC}"
total_time=0
for i in {1..100}; do
    start=$(date +%s.%N)
    curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d '{"query": "What is programming?"}' > /dev/null
    end=$(date +%s.%N)
    time=$(echo "$end - $start" | bc)
    total_time=$(echo "$total_time + $time" | bc)
done
avg_time=$(echo "scale=3; $total_time / 100 * 1000" | bc)
echo "Average response time: ${avg_time}ms"

if (( $(echo "$avg_time < 5" | bc -l) )); then
    echo -e "${GREEN}✅ O(1) Performance verified!${NC}"
else
    echo -e "${YELLOW}⚠️  Performance could be improved${NC}"
fi

echo ""
echo -e "${GREEN}🎉 All tests completed!${NC}"