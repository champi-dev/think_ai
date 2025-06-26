#!/bin/bash
# Simple API test script

echo "🧪 Testing Think AI API..."

# Start the server in background
echo "Starting server..."
./target/release/full-server &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server..."
sleep 3

# Test the API
echo "Testing API..."
curl -X POST http://localhost:8080/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"query": "What is the sun made of?"}' \
  2>/dev/null | jq .

# Kill the server
kill $SERVER_PID 2>/dev/null

echo "✅ Test complete"