#!/bin/bash

echo "🚀 Testing Think AI Server..."

# Kill any existing processes on port 8080
echo "🔧 Cleaning up port 8080..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
sleep 1

# Start server in background
echo "🎯 Starting server..."
./target/release/think-ai server &
SERVER_PID=$!

# Wait for server to initialize
echo "⏳ Waiting for server to start..."
sleep 3

# Test endpoints
echo -e "\n📡 Testing server endpoints:"

echo -e "\n1️⃣ Testing /health endpoint:"
curl -s http://localhost:8080/health | jq . || echo "Health check failed"

echo -e "\n2️⃣ Testing / (webapp) endpoint:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8080/

echo -e "\n3️⃣ Testing /api/chat endpoint:"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"Hello Think AI"}' | jq . || echo "Chat endpoint failed"

echo -e "\n4️⃣ Testing /stats endpoint:"
curl -s http://localhost:8080/stats | jq . || echo "Stats endpoint failed"

# Kill the server
echo -e "\n🛑 Stopping server..."
kill $SERVER_PID 2>/dev/null

echo "✅ Test complete!"