#\!/bin/bash

# Kill any existing server
lsof -ti:8080  < /dev/null |  xargs kill -9 2>/dev/null || true

echo "Starting server..."
./target/release/full-server > server.log 2>&1 &
SERVER_PID=$\!

sleep 3

echo -e "\n🧪 Testing physics query...\n"

echo "=== Query: 'what is physics' ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "what is physics"}' | jq '.'

echo -e "\n=== Query: 'tell me about quantum mechanics' ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "tell me about quantum mechanics"}' | jq '.'

kill $SERVER_PID 2>/dev/null

echo -e "\nDone\!"
