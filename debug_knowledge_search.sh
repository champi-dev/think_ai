#\!/bin/bash

# Kill any existing process on port 8080
lsof -ti:8080  < /dev/null |  xargs kill -9 2>/dev/null || true

echo "Starting server with debug logging..."
RUST_LOG=debug ./target/release/full-server 2>&1 | grep -E "(sun|mars|Query|Searching)" &
SERVER_PID=$\!

# Wait for server to start
sleep 3

echo -e "\n=== Testing knowledge search ==="

# Simple query first
echo -e "\n1. Simple 'sun' query:"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "sun"}' | jq '.response' | head -c 100

echo -e "\n\n2. 'What is the sun?' query:"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the sun?"}' | jq '.response' | head -c 100

echo -e "\n\n3. 'mars' query:"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "mars"}' | jq '.response' | head -c 100

echo -e "\n\n4. 'Tell me about mars' query:"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about mars"}' | jq '.response' | head -c 100

echo -e "\n\nKilling server..."
kill $SERVER_PID 2>/dev/null
pkill -f full-server 2>/dev/null

echo -e "\nDone\!"
