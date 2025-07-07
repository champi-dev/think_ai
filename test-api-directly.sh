#!/bin/bash

# Test the API directly

echo "🧪 Testing Think AI API Directly"
echo "================================"

# Kill any existing server
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Build
echo "Building server..."
cargo build --release --bin full-server > /dev/null 2>&1

# Start server
echo "Starting server..."
./target/release/full-server > server.log 2>&1 &
SERVER_PID=$!

# Wait longer for initialization
echo "Waiting for server to initialize (10 seconds)..."
sleep 10

# Check server status
echo ""
echo "Checking server status..."
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server process is running (PID: $SERVER_PID)"
else
    echo "❌ Server process died! Last 50 lines of log:"
    tail -50 server.log
    exit 1
fi

# Test health endpoint
echo ""
echo "Testing health endpoint..."
HEALTH=$(curl -s -w "\nHTTP_CODE:%{http_code}" http://localhost:8080/health)
echo "Response: $HEALTH"

# Test stats endpoint
echo ""
echo "Testing stats endpoint..."
STATS=$(curl -s http://localhost:8080/api/stats | jq '.' 2>/dev/null || echo "Failed to get stats")
echo "Stats: $STATS"

# Test chat endpoint
echo ""
echo "Testing chat endpoint..."
echo "Query: 'What is quantum computing?'"

CHAT_RESPONSE=$(curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "What is quantum computing?"}' \
    -w "\nHTTP_CODE:%{http_code}")

echo "Full response:"
echo "$CHAT_RESPONSE"

# Parse just the response text
RESPONSE_TEXT=$(echo "$CHAT_RESPONSE" | head -n -1 | jq -r '.response // "No response field"' 2>/dev/null || echo "Failed to parse JSON")
echo ""
echo "Response text: $RESPONSE_TEXT"

# Check server logs
echo ""
echo "Last 20 lines of server log:"
tail -20 server.log

# Cleanup
kill $SERVER_PID 2>/dev/null
echo ""
echo "✅ Test complete"