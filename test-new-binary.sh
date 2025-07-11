#!/bin/bash

echo "🚀 Testing new Think AI binary..."
echo ""

# Kill any test servers on port 7777
echo "Cleaning up test port 7777..."
lsof -ti:7777 | xargs kill -9 2>/dev/null || true

# Start the new binary on test port
echo "Starting new binary on test port 7777..."
PORT=7777 ./target/release/think-ai-full &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Test the server
echo ""
echo "✅ Testing server health..."
curl -s http://localhost:7777/health | jq . || echo "Health check failed"

echo ""
echo "✅ Testing chat endpoint..."
curl -X POST http://localhost:7777/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is O(1) performance?", "context": "testing"}' \
  -s | jq . || echo "Chat test failed"

echo ""
echo "✅ Testing knowledge endpoint..."
curl -s http://localhost:7777/knowledge | jq . || echo "Knowledge check failed"

echo ""
echo "📊 Server info:"
echo "  PID: $SERVER_PID"
echo "  URL: http://localhost:7777"
echo ""
echo "To stop the test server, run: kill $SERVER_PID"
echo ""
echo "To deploy to production:"
echo "1. Stop current production server (PID: $(pgrep -f 'think-ai-full server' | head -1))"
echo "2. Start new binary: ./target/release/think-ai-full server"