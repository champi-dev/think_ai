#!/bin/bash

echo "=== Testing Fix for 'Knowledge engine LLM not initialized' Error ==="
echo

# Build the project
echo "1. Building the project..."
cd /home/administrator/think_ai
cargo build --release 2>&1 | tail -n 20

echo
echo "2. Starting test server on port 3456..."
# Kill any existing process on port 3456
pkill -f "think-ai-server" 2>/dev/null
sleep 1

# Start the server in the background
RUST_LOG=think_ai=debug ./target/release/think-ai-server > test_server.log 2>&1 &
SERVER_PID=$!
echo "Server started with PID: $SERVER_PID"

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Test various queries that previously returned the error
echo
echo "3. Testing scientific queries..."
echo "Query: explain the theory of relativity"
curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "explain the theory of relativity"}' | jq -r '.response' | head -n 3

echo
echo "Query: what is quantum mechanics"
curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "what is quantum mechanics"}' | jq -r '.response' | head -n 3

echo
echo "4. Testing philosophical queries..."
echo "Query: what is the meaning of life"
curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "what is the meaning of life"}' | jq -r '.response' | head -n 3

echo
echo "Query: what is consciousness"
curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "what is consciousness"}' | jq -r '.response' | head -n 3

echo
echo "5. Testing technical queries..."
echo "Query: how do computers work"
curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "how do computers work"}' | jq -r '.response' | head -n 3

echo
echo "Query: what is an algorithm"
curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "what is an algorithm"}' | jq -r '.response' | head -n 3

echo
echo "6. Testing analogy queries..."
echo "Query: what is coding like"
curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "what is coding like"}' | jq -r '.response' | head -n 3

echo
echo "7. Testing unknown query..."
echo "Query: xyzabc123 gibberish"
curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "xyzabc123 gibberish"}' | jq -r '.response' | head -n 3

echo
echo "8. Checking server logs for errors..."
grep -i "error\|llm not initialized" test_server.log | tail -n 5

echo
echo "Cleanup: Stopping test server..."
kill $SERVER_PID 2>/dev/null
rm -f test_server.log

echo
echo "=== Test Complete ==="
echo "If you no longer see 'Knowledge engine LLM not initialized' messages,"
echo "then the fix has been successfully applied!"