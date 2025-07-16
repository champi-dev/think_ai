#!/bin/bash

echo "🔍 Simple Cache Verification Test"
echo "=================================="
echo ""

echo "🚀 Starting Think AI server with detailed logging..."
# Kill any existing server
pkill -f "think-ai server" || true
sleep 1

# Start server in background
./target/release/think-ai server &
SERVER_PID=$!
sleep 3

echo ""
echo "🧪 Testing cache with detailed server logs:"
echo ""

echo "1. Testing 'hello' (should hit full message cache):"
echo "   Look for logs showing:"
echo "   - MultiLevel Cache: Processing query 'hello'" 
echo "   - CACHE HIT! Level: FULL MESSAGE"
echo "   - USING COMPONENT: MultiLevelCache"
echo ""

curl -s -X POST http://localhost:8080/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "hello"}' | jq -r '.response'

echo ""
echo "=================================="
echo ""

echo "2. Testing 'what is love' (should hit full message cache):"
echo ""

curl -s -X POST http://localhost:8080/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "what is love"}' | jq -r '.response'

echo ""
echo "=================================="
echo ""

echo "3. Testing novel query (should generate new patterns):"
echo ""

curl -s -X POST http://localhost:8080/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "what is mathematics"}' | jq -r '.response'

echo ""
echo "=================================="
echo "🔍 VERIFICATION COMPLETE"
echo ""
echo "To verify the multi-level cache is working, check the server logs above for:"
echo "✅ '🧠 MultiLevel Cache: Processing query' messages"
echo "✅ '🎯 ✅ CACHE HIT! Level:' messages (vs CACHE MISS)"
echo "✅ '🎯 USING COMPONENT: MultiLevelCache' messages"
echo "✅ Component scoring showing MultiLevelCache gets highest scores"
echo ""
echo "If you see these logs, the multi-level cache system is working!"
echo "If you see 'CACHE MISS' and other components being used, something is wrong."

# Cleanup
echo ""
kill $SERVER_PID 2>/dev/null || true
sleep 1