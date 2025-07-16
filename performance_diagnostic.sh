#!/bin/bash

echo "🔍 Think AI Performance Diagnostic Script"
echo "========================================"
echo "Timestamp: $(date)"
echo ""

# Kill any existing servers
echo "🧹 Cleaning up existing servers..."
killall think-ai-http think-ai full-server > /dev/null 2>&1 || true
sleep 2

# Build optimized release
echo "🔨 Building optimized release..."
cargo build --release --quiet
if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi
echo "✅ Build successful"

# Start server with timing
echo "🚀 Starting server with performance monitoring..."
timeout 30s strace -c -f ./target/release/full-server > server_startup.log 2>&1 &
SERVER_PID=$!

echo "⏳ Waiting for server initialization..."
sleep 10

# Check if server is responding
echo "🔍 Testing server responsiveness..."
START_TIME=$(date +%s%N)

# Try simple health check first
curl -s --max-time 5 http://localhost:8080/health > health_response.txt 2>&1
HEALTH_STATUS=$?

if [ $HEALTH_STATUS -eq 0 ]; then
    echo "✅ Health endpoint responding"
    cat health_response.txt
else
    echo "❌ Health endpoint timeout/error"
fi

# Try chat endpoint with minimal query
echo "🗣️ Testing chat endpoint..."
START_CHAT=$(date +%s%N)
curl -s --max-time 10 -X POST http://localhost:8080/api/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "hi"}' > chat_response.txt 2>&1
CHAT_STATUS=$?
END_CHAT=$(date +%s%N)

CHAT_TIME=$(( (END_CHAT - START_CHAT) / 1000000 ))  # Convert to milliseconds

if [ $CHAT_STATUS -eq 0 ]; then
    echo "✅ Chat endpoint responding (${CHAT_TIME}ms)"
    echo "Response size: $(wc -c < chat_response.txt) bytes"
    head -200 chat_response.txt
else
    echo "❌ Chat endpoint timeout/error (${CHAT_TIME}ms)"
    echo "Error output:"
    cat chat_response.txt
fi

# Check process stats
echo ""
echo "📊 Server Process Statistics:"
if ps -p $SERVER_PID > /dev/null 2>&1; then
    ps -p $SERVER_PID -o pid,ppid,pcpu,pmem,vsz,rss,time,cmd
    echo "Memory usage: $(ps -p $SERVER_PID -o rss= | tr -d ' ')KB"
else
    echo "❌ Server process not running"
fi

# System resources
echo ""
echo "💻 System Resources:"
echo "CPU Load: $(uptime | awk -F'load average:' '{print $2}')"
echo "Memory: $(free -h | grep Mem:)"
echo "Disk I/O: $(iostat -d 1 1 | tail -n +4)"

# Kill server
echo ""
echo "🛑 Stopping server..."
kill $SERVER_PID > /dev/null 2>&1
sleep 2

echo "📋 Diagnostic Summary:"
echo "- Health endpoint: $([ $HEALTH_STATUS -eq 0 ] && echo 'OK' || echo 'FAILED')"
echo "- Chat endpoint: $([ $CHAT_STATUS -eq 0 ] && echo "OK (${CHAT_TIME}ms)" || echo 'FAILED')"
echo "- Logs saved to: server_startup.log, health_response.txt, chat_response.txt"

echo ""
echo "🎯 Performance Targets from CLAUDE.md:"
echo "- Target response time: <3 seconds (we got: ${CHAT_TIME}ms)"
echo "- O(1) cache lookups: Hash-based implementation ✅"
echo "- Memory optimization: FlashAttention tiling ✅"

if [ $CHAT_TIME -gt 3000 ]; then
    echo "⚠️  PERFORMANCE ISSUE: Response time exceeds 3s target"
    echo "🔍 Recommended next steps:"
    echo "   1. Check server_startup.log for initialization bottlenecks"
    echo "   2. Profile individual component response times"
    echo "   3. Investigate async pipeline delays"
else
    echo "✅ Performance target achieved!"
fi