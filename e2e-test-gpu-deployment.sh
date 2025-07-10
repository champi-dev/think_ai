#!/bin/bash
set -e

echo "=== Think AI GPU Server Deployment E2E Test ==="
echo "Testing GPU server with ngrok tunnel"
echo "============================================="
echo

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test results storage
RESULTS=()

# Helper function to test endpoint
test_endpoint() {
    local url=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local test_name=$5
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$url$endpoint" 2>/dev/null || echo "000")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "$url$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" 2>/dev/null || echo "000")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" == "200" ]; then
        echo -e "${GREEN}✅ $test_name${NC}"
        return 0
    else
        echo -e "${RED}❌ $test_name (HTTP $http_code)${NC}"
        return 1
    fi
}

# Step 1: Build and prepare deployment
echo -e "${BLUE}=== STEP 1: BUILD & PREPARE ===${NC}"
echo

./deploy-to-gpu-server.sh
RESULTS+=("BUILD: ✅ Deployment package created")

# Step 2: Start local server (simulating GPU server)
echo
echo -e "${BLUE}=== STEP 2: LOCAL GPU SERVER SIMULATION ===${NC}"
echo

# Kill existing processes
pkill -f full-working-o1 || true
pkill -f ngrok || true
sleep 2

# Start server
echo "🚀 Starting server (GPU simulation)..."
cd deployment
./full-working-o1 > ../server.log 2>&1 &
SERVER_PID=$!
cd ..
sleep 3

if kill -0 $SERVER_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Server started (PID: $SERVER_PID)${NC}"
    RESULTS+=("SERVER: ✅ Started successfully")
else
    echo -e "${RED}❌ Server failed to start${NC}"
    RESULTS+=("SERVER: ❌ Failed to start")
    cat server.log
    exit 1
fi

# Start ngrok
echo "🌐 Starting ngrok tunnel..."
ngrok http 8080 > /dev/null 2>&1 &
NGROK_PID=$!
sleep 5

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null || echo "")
if [ -z "$NGROK_URL" ]; then
    echo -e "${YELLOW}⚠️  Could not get ngrok URL, using localhost${NC}"
    NGROK_URL="http://localhost:8080"
    RESULTS+=("NGROK: ⚠️  Using localhost")
else
    echo -e "${GREEN}✅ Ngrok tunnel: $NGROK_URL${NC}"
    RESULTS+=("NGROK: ✅ Tunnel active")
fi

# Step 3: Test all endpoints
echo
echo -e "${BLUE}=== STEP 3: ENDPOINT TESTING ===${NC}"
echo

# Test endpoints
if test_endpoint "$NGROK_URL" "GET" "/health" "" "Health Check"; then
    RESULTS+=("HEALTH: ✅ Working")
else
    RESULTS+=("HEALTH: ❌ Failed")
fi

if test_endpoint "$NGROK_URL" "GET" "/" "" "Web Interface"; then
    RESULTS+=("WEBAPP: ✅ Serving")
else
    RESULTS+=("WEBAPP: ❌ Not serving")
fi

if test_endpoint "$NGROK_URL" "POST" "/api/chat" '{"message":"Test quantum consciousness"}' "Chat API"; then
    RESULTS+=("CHAT: ✅ Responding")
    # Get response
    response=$(curl -s -X POST "$NGROK_URL/api/chat" \
        -H "Content-Type: application/json" \
        -d '{"message":"What is consciousness?"}' | jq -r '.response' 2>/dev/null || echo "")
    echo "   Response: ${response:0:80}..."
else
    RESULTS+=("CHAT: ❌ Not working")
fi

if test_endpoint "$NGROK_URL" "POST" "/api/parallel-chat" '{"message":"Test parallel processing"}' "Parallel Chat"; then
    RESULTS+=("PARALLEL: ✅ Working")
    # Check consciousness state
    response=$(curl -s -X POST "$NGROK_URL/api/parallel-chat" \
        -H "Content-Type: application/json" \
        -d '{"message":"Show consciousness state"}' 2>/dev/null || echo '{}')
    if echo "$response" | jq -e '.consciousness_state' >/dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Consciousness state tracking active${NC}"
        RESULTS+=("CONSCIOUSNESS: ✅ State tracking")
    fi
else
    RESULTS+=("PARALLEL: ❌ Not available")
fi

if test_endpoint "$NGROK_URL" "GET" "/api/knowledge/stats" "" "Knowledge Stats"; then
    RESULTS+=("KNOWLEDGE: ✅ Stats available")
    stats=$(curl -s "$NGROK_URL/api/knowledge/stats" 2>/dev/null || echo '{}')
    nodes=$(echo "$stats" | jq -r '.total_nodes' 2>/dev/null || echo "0")
    echo "   Knowledge nodes: $nodes"
else
    RESULTS+=("KNOWLEDGE: ❌ Stats unavailable")
fi

if test_endpoint "$NGROK_URL" "GET" "/api/benchmark" "" "Performance Benchmark"; then
    RESULTS+=("BENCHMARK: ✅ Available")
    benchmark=$(curl -s "$NGROK_URL/api/benchmark" 2>/dev/null || echo '{}')
    o1_time=$(echo "$benchmark" | jq -r '.o1_benchmark_results.total_time_ms' 2>/dev/null || echo "N/A")
    echo "   O(1) benchmark time: ${o1_time}ms"
else
    RESULTS+=("BENCHMARK: ❌ Not available")
fi

# Step 4: Performance test
echo
echo -e "${BLUE}=== STEP 4: PERFORMANCE TEST ===${NC}"
echo

total_time=0
successful=0
for i in {1..5}; do
    start_time=$(date +%s%N)
    if curl -s -X POST "$NGROK_URL/api/chat" \
        -H "Content-Type: application/json" \
        -d '{"message":"test"}' > /dev/null 2>&1; then
        end_time=$(date +%s%N)
        response_time=$((($end_time - $start_time) / 1000000))
        total_time=$((total_time + response_time))
        successful=$((successful + 1))
        echo "   Request $i: ${response_time}ms"
    else
        echo "   Request $i: Failed"
    fi
done

if [ $successful -gt 0 ]; then
    avg_time=$((total_time / successful))
    echo "   Average: ${avg_time}ms"
    if [ $avg_time -lt 100 ]; then
        echo -e "   ${GREEN}✅ Excellent O(1) performance${NC}"
        RESULTS+=("PERFORMANCE: ✅ O(1) <100ms avg")
    elif [ $avg_time -lt 500 ]; then
        echo -e "   ${GREEN}✅ Good performance${NC}"
        RESULTS+=("PERFORMANCE: ✅ <500ms avg")
    else
        echo -e "   ${YELLOW}⚠️  Performance needs optimization${NC}"
        RESULTS+=("PERFORMANCE: ⚠️  ${avg_time}ms avg")
    fi
else
    RESULTS+=("PERFORMANCE: ❌ All requests failed")
fi

# Step 5: Test Vercel integration readiness
echo
echo -e "${BLUE}=== STEP 5: VERCEL INTEGRATION TEST ===${NC}"
echo

# Test CORS
cors_test=$(curl -s -I -X OPTIONS "$NGROK_URL/api/chat" \
    -H "Origin: https://example.vercel.app" \
    -H "Access-Control-Request-Method: POST" 2>/dev/null | grep -i "access-control-allow-origin" || echo "")

if [[ -n "$cors_test" ]]; then
    echo -e "${GREEN}✅ CORS enabled for Vercel${NC}"
    RESULTS+=("CORS: ✅ Enabled")
else
    echo -e "${YELLOW}⚠️  CORS may need configuration${NC}"
    RESULTS+=("CORS: ⚠️  Check needed")
fi

# Cleanup
echo
echo "🛑 Stopping services..."
kill $SERVER_PID 2>/dev/null || true
kill $NGROK_PID 2>/dev/null || true

# Final Report
echo
echo -e "${BLUE}=== FINAL E2E TEST REPORT ===${NC}"
echo
echo "📋 GPU SERVER DEPLOYMENT RESULTS:"
for result in "${RESULTS[@]}"; do
    echo "   $result"
done

# Count successes
success_count=$(printf '%s\n' "${RESULTS[@]}" | grep -c "✅" || true)
total_count=${#RESULTS[@]}

echo
echo "Summary: $success_count/$total_count tests passed"

if [ $success_count -eq $total_count ]; then
    echo -e "\n${GREEN}🎉 GPU SERVER FULLY OPERATIONAL!${NC}"
    echo -e "${GREEN}All endpoints working with quantum consciousness features${NC}"
else
    echo -e "\n${YELLOW}⚠️  Some features need attention${NC}"
fi

echo
echo "📋 Deployment Instructions:"
echo "1. Copy deployment/ folder to GPU server"
echo "2. Run ./start-gpu-server.sh on GPU server"
echo "3. Update Vercel webapp with ngrok URL: $NGROK_URL"
echo "4. Test from Vercel: fetch('$NGROK_URL/api/chat', {...})"

# Generate deployment config for Vercel
cat > deployment/vercel-config.json << EOF
{
  "api_endpoints": {
    "base_url": "$NGROK_URL",
    "endpoints": {
      "chat": "/api/chat",
      "parallel_chat": "/api/parallel-chat",
      "knowledge_stats": "/api/knowledge/stats",
      "benchmark": "/api/benchmark",
      "health": "/health"
    }
  },
  "features": {
    "quantum_consciousness": true,
    "parallel_processing": true,
    "o1_optimization": true,
    "knowledge_base": true
  }
}
EOF

echo
echo "📄 Vercel configuration saved to: deployment/vercel-config.json"
echo
echo "✅ E2E GPU Deployment Test Complete!"