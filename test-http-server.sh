#!/bin/bash

# Test Think AI HTTP Server locally

echo "🧪 Testing Think AI HTTP Server"
echo "================================"

# Kill any existing server on port 8080
echo "🔧 Killing any existing process on port 8080..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Build the stable server binary 
echo "🔨 Building stable server..."
cargo build --release --bin stable-server

# Check if build succeeded
if [ $? -ne 0 ]; then
    echo "❌ Build failed. Exiting."
    exit 1
fi

echo "✅ Build successful!"

# Start the server in background
echo "🚀 Starting server on port 8080..."
./target/release/stable-server &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Check if server is running
if ! ps -p $SERVER_PID > /dev/null; then
    echo "❌ Server failed to start"
    exit 1
fi

echo "✅ Server is running with PID: $SERVER_PID"

# Test the chat endpoint
echo ""
echo "📡 Testing chat endpoint..."
echo "================================"

# Test 1: Valid request
echo "Test 1: Valid chat request"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is O(1) complexity?"}' \
  -s | jq '.' || echo "Response: $(curl -X POST http://localhost:8080/api/chat -H "Content-Type: application/json" -d '{"query": "What is O(1) complexity?"}' -s)"

echo ""
echo "Test 2: Empty query (should work with stable-server)"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": ""}' \
  -s | jq '.' || echo "Response: $(curl -X POST http://localhost:8080/api/chat -H "Content-Type: application/json" -d '{"query": ""}' -s)"

echo ""
echo "Test 3: Missing Content-Type header"
curl -X POST http://localhost:8080/api/chat \
  -d '{"query": "Hello"}' \
  -s | jq '.' || echo "Response: $(curl -X POST http://localhost:8080/api/chat -d '{"query": "Hello"}' -s)"

echo ""
echo "Test 4: Long query"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Can you explain how Think AI achieves O(1) performance in detail? I am particularly interested in understanding the hash-based lookup system and how it maintains constant time complexity regardless of the knowledge base size."}' \
  -s | jq '.' || echo "Response: $(curl -X POST http://localhost:8080/api/chat -H "Content-Type: application/json" -d '{"query": "Can you explain how Think AI achieves O(1) performance in detail?"}' -s)"

# Test other endpoints
echo ""
echo "📡 Testing other endpoints..."
echo "================================"

echo "Health check:"
curl -s http://localhost:8080/health | jq '.' || echo "Response: $(curl -s http://localhost:8080/health)"

echo ""
echo "Stats:"
curl -s http://localhost:8080/api/stats | jq '.' || echo "Response: $(curl -s http://localhost:8080/api/stats)"

echo ""
echo "Performance:"
curl -s http://localhost:8080/api/performance | jq '.' || echo "Response: $(curl -s http://localhost:8080/api/performance)"

# Kill the server
echo ""
echo "🛑 Stopping server..."
kill $SERVER_PID

echo "✅ All tests completed!"