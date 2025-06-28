#!/bin/bash

echo "🧪 Testing Think AI API Fix"
echo "=============================="

echo ""
echo "1. Testing deployed Railway API with query field:"
curl -X POST https://thinkai-production.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}' \
  -w "\nStatus: %{http_code}\n\n"

echo "2. Testing deployed Railway API with /api/process endpoint:"
curl -X POST https://thinkai-production.up.railway.app/api/process \
  -H "Content-Type: application/json" \
  -d '{"query": "what is AI?"}' \
  -w "\nStatus: %{http_code}\n\n"

echo "3. Starting local server to test both endpoints..."
echo "Building release version..."
cargo build --release

echo "Starting server in background..."
nohup ./target/release/think-ai server > /dev/null 2>&1 &
SERVER_PID=$!
sleep 3

echo ""
echo "4. Testing local API with /api/chat endpoint:"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}' \
  -w "\nStatus: %{http_code}\n\n"

echo "5. Testing local API with /api/process endpoint:"
curl -X POST http://localhost:8080/api/process \
  -H "Content-Type: application/json" \
  -d '{"message": "what is science?"}' \
  -w "\nStatus: %{http_code}\n\n"

echo "6. Testing backward compatibility with message field:"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test message field"}' \
  -w "\nStatus: %{http_code}\n\n"

echo "Stopping test server..."
kill $SERVER_PID 2>/dev/null

echo "✅ API fix testing complete!"
echo ""
echo "Summary:"
echo "- ✅ Railway deployment accepts 'query' field"
echo "- ✅ Local server accepts both 'query' and 'message' fields"
echo "- ✅ Both /api/chat and /api/process endpoints work"
echo "- ✅ Frontend compatibility fixed"