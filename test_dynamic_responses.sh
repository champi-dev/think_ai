#\!/bin/bash

# Kill any existing process on port 8080
lsof -ti:8080  < /dev/null |  xargs kill -9 2>/dev/null || true

echo "Starting Think AI Full Server..."
./target/release/full-server &
SERVER_PID=$\!

# Wait for server to start
sleep 3

echo -e "\n🧪 Testing Dynamic Knowledge Responses...\n"

# Test 1: Ask about the sun
echo "Test 1: Sun query"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the sun?"}' | jq '.'

echo -e "\n---\n"

# Test 2: Context-aware follow-up
echo "Test 2: Context-aware follow-up"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is it made of?"}' | jq '.'

echo -e "\n---\n"

# Test 3: Ask about TinyLlama
echo "Test 3: TinyLlama query"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about TinyLlama"}' | jq '.'

echo -e "\n---\n"

# Test 4: Ask about Think AI
echo "Test 4: Think AI query"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Think AI?"}' | jq '.'

echo -e "\n---\n"

# Kill the server
echo "Stopping server..."
kill $SERVER_PID

echo "Tests completed\!"
