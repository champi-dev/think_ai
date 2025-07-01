#!/bin/bash
# Complete local testing script for Think AI optimizations

echo "🚀 Think AI Local Performance Test"
echo "=================================="

# 1. Kill any existing servers
echo "🔧 Cleaning up existing processes..."
pkill -f "full-server" || true
sleep 2

# 2. Build optimized release
echo "🏗️ Building optimized release version..."
cargo build --release

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"

# 3. Start server in background
echo "🚀 Starting optimized server..."
./target/release/full-server > server.log 2>&1 &
SERVER_PID=$!

# Wait for server to initialize
echo "⏳ Waiting for server initialization..."
sleep 10

# 4. Test server is running
if ! curl -s http://localhost:8080/health > /dev/null; then
    echo "❌ Server failed to start!"
    cat server.log | tail -20
    exit 1
fi

echo "✅ Server is running!"

# 5. Performance tests
echo ""
echo "🧪 PERFORMANCE TESTS"
echo "==================="

echo "Test 1: Greeting (should be ~1ms with O(1) cache)"
time curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}' \
  -s | jq '.response_time_ms'

echo ""
echo "Test 2: Cache hit (same greeting, should be <5ms)"
time curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}' \
  -s | jq '.response_time_ms'

echo ""
echo "Test 3: Simple query (should complete in 5-10s max)"
timeout 15s curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is physics?"}' \
  -s | jq '.response_time_ms // "TIMEOUT"'

echo ""
echo "Test 4: Concurrent requests (should not block each other)"
echo "Running 3 parallel greetings..."
time (
  for i in {1..3}; do
    curl -X POST http://localhost:8080/api/chat \
      -H "Content-Type: application/json" \
      -d '{"query": "hello '$(date +%s)'"}' \
      -s > /tmp/response_$i.json &
  done
  wait
)

echo "Concurrent response times:"
for i in {1..3}; do
  echo "  Request $i: $(cat /tmp/response_$i.json | jq '.response_time_ms // "ERROR"')ms"
done

echo ""
echo "Test 5: Server stats"
curl -s http://localhost:8080/api/stats | jq '{total_nodes, cache_stats: .cache_hit_rate}'

echo ""
echo "📊 OPTIMIZATION VERIFICATION"
echo "============================"

# Check for optimizations in logs
echo "✅ O(1) Cache hits:"
grep -c "Cache hit" server.log || echo "0"

echo "✅ Read-only LLM calls:"
grep -c "Using enhanced knowledge system" server.log || echo "0"

echo "✅ Timeout protection active:"
grep -c "seconds timeout" server.log || echo "0"

echo ""
echo "🎯 EXPECTED PERFORMANCE:"
echo "======================="
echo "✅ Greetings: 0.1-2ms (O(1) cache)"
echo "✅ Cache hits: <5ms (O(1) lookup)"
echo "✅ Simple queries: 5-10s max (with timeout)"
echo "✅ Concurrent requests: No blocking"
echo "✅ Memory usage: Stable (O(1) structures)"

echo ""
echo "📝 To monitor in real-time:"
echo "tail -f server.log"
echo ""
echo "🛑 To stop server:"
echo "kill $SERVER_PID"

echo ""
echo "🎉 Local testing complete! Server PID: $SERVER_PID"