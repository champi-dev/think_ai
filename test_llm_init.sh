#!/bin/bash
set -e

echo "Testing LLM initialization issue..."

# Build first
echo "Building project..."
cargo build --release

# Test via HTTP API locally
echo -e "\n--- Testing via HTTP API on local port ---"
PORT=7777

# Kill any existing process on port
lsof -ti:$PORT | xargs kill -9 2>/dev/null || true

# Start server in background
RUST_LOG=debug ./target/release/think-ai-http --port $PORT &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Test queries
echo -e "\nTesting simple query..."
curl -X POST http://localhost:$PORT/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}' | jq .

echo -e "\nTesting quantum query..."
curl -X POST http://localhost:$PORT/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "what is consciousness"}' | jq .

echo -e "\nTesting with conversation context..."
SESSION_ID=$(uuidgen)
curl -X POST http://localhost:$PORT/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"hello\", \"session_id\": \"$SESSION_ID\"}" | jq .

curl -X POST http://localhost:$PORT/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"what is AI\", \"session_id\": \"$SESSION_ID\"}" | jq .

# Clean up
kill $SERVER_PID 2>/dev/null || true

echo -e "\nTest complete!"