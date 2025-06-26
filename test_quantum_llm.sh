#!/bin/bash

# Kill any existing process on port 8080
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

echo "Starting Think AI Full Server with Quantum LLM..."
./target/release/full-server &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo -e "\n🧪 Testing Quantum LLM responses...\n"

# Test 1: Basic greeting
echo "Test 1: Basic greeting"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello, tell me about consciousness"}' | jq '.'

echo -e "\n---\n"

# Test 2: Philosophy question
echo "Test 2: Philosophy question"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is free will?"}' | jq '.'

echo -e "\n---\n"

# Test 3: Science question
echo "Test 3: Science question"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain quantum entanglement"}' | jq '.'

echo -e "\n---\n"

# Test 4: Check stats
echo "Test 4: Server stats"
curl -s http://localhost:8080/api/stats | jq '.'

echo -e "\n---\n"

# Kill the server
echo "Stopping server..."
kill $SERVER_PID

echo "Tests completed!"