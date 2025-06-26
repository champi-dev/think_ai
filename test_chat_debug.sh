#!/bin/bash
# Debug script to test chat endpoint

echo "Starting server..."
./target/release/full-server 2>&1 | tee server_debug.log &
SERVER_PID=$!

echo "Waiting for server to start..."
sleep 5

echo "Testing health endpoint..."
curl -s http://localhost:8080/health
echo ""

echo "Testing chat endpoint with 'hi'..."
timeout 10 curl -X POST http://localhost:8080/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"query": "hi"}' \
  -v 2>&1

echo "Killing server..."
kill $SERVER_PID 2>/dev/null

echo "Server output:"
tail -20 server_debug.log