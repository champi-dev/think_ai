#\!/bin/bash

# Kill any existing server
lsof -ti:8080  < /dev/null |  xargs kill -9 2>/dev/null || true

echo "Starting server..."
./target/release/full-server > server.log 2>&1 &
SERVER_PID=$\!

sleep 3

echo -e "\n🧪 Testing Stoics query...\n"

echo "=== Query: 'what are those stoics about' ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "what are those stoics about"}' | jq '.'

echo -e "\n=== Query: 'tell me about stoicism' ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "tell me about stoicism"}' | jq '.'

kill $SERVER_PID 2>/dev/null

echo -e "\nDone\!"
