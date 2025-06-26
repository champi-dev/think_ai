#\!/bin/bash

# Kill any existing process on port 8080
lsof -ti:8080  < /dev/null |  xargs kill -9 2>/dev/null || true

echo "Starting Think AI Full Server..."
./target/release/full-server > server.log 2>&1 &
SERVER_PID=$\!

# Wait for server to start
sleep 3

echo -e "\n🧪 Testing Specific Queries...\n"

# Debug the knowledge search
echo "=== DEBUG: Checking knowledge for 'sun' ==="
curl -s http://localhost:8080/api/stats | jq '.'

echo -e "\n=== Test 1: Direct sun query ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "sun"}' | jq '.'

echo -e "\n=== Test 2: What is the sun ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "what is the sun"}' | jq '.'

echo -e "\n=== Test 3: Tell me about mars ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "tell me about mars"}' | jq '.'

echo -e "\n=== Test 4: TinyLlama ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "tinyllama"}' | jq '.'

# Kill the server
echo -e "\nStopping server..."
kill $SERVER_PID

echo -e "\n=== Server log (last 20 lines) ==="
tail -20 server.log

echo "Tests completed\!"
