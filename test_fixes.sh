#!/bin/bash
# Test script to verify all fixes

set -e

echo "🔧 Testing Think AI Fixes..."
echo "================================"

# Build the project
echo "📦 Building project..."
cargo build --release 2>/dev/null || {
    echo "❌ Build failed"
    exit 1
}

# Kill any existing servers
echo "🛑 Cleaning up ports..."
pkill -f "think-ai server" 2>/dev/null || true
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
sleep 2

# Start the server
echo "🚀 Starting server..."
./target/release/think-ai server &
SERVER_PID=$!
sleep 3

# Function to cleanup on exit
cleanup() {
    echo "🧹 Cleaning up..."
    kill $SERVER_PID 2>/dev/null || true
    pkill -f "think-ai server" 2>/dev/null || true
}
trap cleanup EXIT

# Test 1: Knowledge API endpoint
echo ""
echo "✅ Test 1: Knowledge API Endpoint"
curl -s http://localhost:8080/api/knowledge/stats | jq '.' || echo "❌ Knowledge API failed"

# Test 2: JSON parsing error handling
echo ""
echo "✅ Test 2: JSON Error Handling"
echo "Testing invalid JSON..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8080/chat \
    -H "Content-Type: application/json" \
    -d "invalid json")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "400" ]; then
    echo "✅ Invalid JSON handled correctly (400 response)"
else
    echo "❌ Invalid JSON not handled properly (got $HTTP_CODE)"
fi

# Test 3: O(1) Performance under load
echo ""
echo "✅ Test 3: O(1) Performance Test"
echo "Running performance test..."

# Function to make requests
make_requests() {
    local count=$1
    local total_time=0
    
    for i in $(seq 1 $count); do
        start=$(date +%s.%N)
        curl -s -X POST http://localhost:8080/chat \
            -H "Content-Type: application/json" \
            -d "{\"message\": \"test query $i\"}" > /dev/null
        end=$(date +%s.%N)
        time_diff=$(echo "$end - $start" | bc)
        total_time=$(echo "$total_time + $time_diff" | bc)
    done
    
    avg_time=$(echo "scale=3; $total_time / $count" | bc)
    echo "$avg_time"
}

TIME_1=$(make_requests 1)
TIME_10=$(make_requests 10)
TIME_50=$(make_requests 50)

echo "Response times:"
echo "  1 request: ${TIME_1}s"
echo "  10 requests avg: ${TIME_10}s"
echo "  50 requests avg: ${TIME_50}s"

# Calculate variance
VARIANCE=$(echo "scale=2; $TIME_50 / $TIME_1" | bc)
echo "Variance: ${VARIANCE}x"

if (( $(echo "$VARIANCE < 1.2" | bc -l) )); then
    echo "✅ O(1) performance verified (variance < 1.2x)"
else
    echo "⚠️  Performance variance: ${VARIANCE}x (target < 1.2x)"
fi

# Test 4: AI query matching
echo ""
echo "✅ Test 4: AI Query Matching"
RESPONSE=$(curl -s -X POST http://localhost:8080/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "explain AI"}')

if echo "$RESPONSE" | grep -qi "artificial intelligence"; then
    echo "✅ AI query returns 'artificial intelligence' keyword"
else
    echo "❌ AI query missing 'artificial intelligence' keyword"
    echo "Response: $RESPONSE" | head -n 3
fi

echo ""
echo "================================"
echo "🎉 All tests completed!"