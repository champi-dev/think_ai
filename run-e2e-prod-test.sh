#\!/bin/bash
set -e

echo "🧪 Running E2E Test against Production (thinkai.lat)..."
echo "=================================================="

# Test endpoints
BASE_URL="https://thinkai.lat"

# Function to test endpoint
test_endpoint() {
    local endpoint=$1
    local expected=$2
    echo -n "Testing $endpoint... "
    
    response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint"  < /dev/null |  tail -1)
    
    if [ "$response" == "$expected" ]; then
        echo "✅ PASS (HTTP $response)"
    else
        echo "❌ FAIL (Expected $expected, got $response)"
        return 1
    fi
}

# Function to test API response
test_api() {
    local endpoint=$1
    echo -n "Testing API $endpoint... "
    
    response=$(curl -s -X POST "$BASE_URL$endpoint" \
        -H "Content-Type: application/json" \
        -d '{"prompt":"test","stream":false}' \
        -w "\n%{http_code}")
    
    http_code=$(echo "$response" | tail -1)
    
    if [ "$http_code" == "200" ]; then
        echo "✅ PASS (HTTP 200)"
    else
        echo "❌ FAIL (HTTP $http_code)"
        return 1
    fi
}

# Test homepage
test_endpoint "/" "200"

# Test health endpoint
test_endpoint "/health" "200"

# Test static resources
test_endpoint "/static/index.js" "200"
test_endpoint "/static/style.css" "200"

# Test API endpoints
test_api "/api/chat"
test_api "/api/generate"

# Test webapp routes
test_endpoint "/chat" "200"

# Performance test
echo -n "Testing response time... "
time_taken=$(curl -s -o /dev/null -w "%{time_total}" "$BASE_URL/health")
if (( $(echo "$time_taken < 1.0" | bc -l) )); then
    echo "✅ PASS (${time_taken}s)"
else
    echo "⚠️  SLOW (${time_taken}s)"
fi

# Test SSL
echo -n "Testing SSL certificate... "
if curl -s --head "$BASE_URL" | grep -q "200"; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi

echo ""
echo "=================================================="
echo "✅ E2E Test Complete\!"
echo ""
echo "Production site: $BASE_URL"
echo "Build: ./target/release/railway-server"
echo ""
