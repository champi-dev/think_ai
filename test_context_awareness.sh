#\!/bin/bash

# Kill any existing process on port 8080
lsof -ti:8080  < /dev/null |  xargs kill -9 2>/dev/null || true

echo "Starting Think AI Full Server..."
./target/release/full-server > server.log 2>&1 &
SERVER_PID=$\!

# Wait for server to start
sleep 3

echo -e "\n🧪 Testing Context Awareness...\n"

# Test 1: Ask about the sun
echo "=== Test 1: Initial query about sun ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the sun?"}' | jq '.'

echo -e "\n=== Test 2: Context-aware follow-up ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is it made of?"}' | jq '.'

echo -e "\n=== Test 3: Another context query ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How hot is it?"}' | jq '.'

echo -e "\n=== Test 4: Ask about Mars ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about Mars"}' | jq '.'

echo -e "\n=== Test 5: Context switch - asking about 'it' should refer to Mars ==="
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Does it have water?"}' | jq '.'

# Kill the server
echo -e "\nStopping server..."
kill $SERVER_PID

echo "Tests completed\!"
