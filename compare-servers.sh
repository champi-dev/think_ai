#!/bin/bash

# Compare stable-server vs full-server responses

echo "🔬 Think AI Server Comparison"
echo "============================="
echo ""

# Test query
QUERY="What is quantum computing?"

# Kill any existing servers
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
lsof -ti:8081 | xargs kill -9 2>/dev/null || true

# Build both servers
echo "🔨 Building servers..."
cargo build --release --bin stable-server --quiet
cargo build --release --bin full-server --quiet

echo ""
echo "1️⃣ Testing STABLE-SERVER (simplified responses):"
echo "================================================"

# Start stable-server on port 8080
PORT=8080 ./target/release/stable-server > stable.log 2>&1 &
STABLE_PID=$!
sleep 2

# Test stable-server
STABLE_RESPONSE=$(curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"$QUERY\"}" | jq -r '.response')

echo "Query: $QUERY"
echo "Response: $STABLE_RESPONSE"
echo ""

# Kill stable-server
kill $STABLE_PID 2>/dev/null

echo "2️⃣ Testing FULL-SERVER (real AI responses):"
echo "==========================================="

# Start full-server on port 8080
./target/release/full-server > full.log 2>&1 &
FULL_PID=$!
sleep 5  # Full server needs more time to initialize

# Test full-server
FULL_RESPONSE=$(curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"$QUERY\"}" | jq -r '.response')

echo "Query: $QUERY"
echo "Response: $FULL_RESPONSE"
echo ""

# Kill full-server
kill $FULL_PID 2>/dev/null

echo "📊 Summary:"
echo "==========="
echo "• stable-server: Returns pre-defined messages (no real AI)"
echo "• full-server: Uses actual AI components for intelligent responses"
echo ""
echo "The Railway deployment appears to be using a simplified cache component."
echo "For real AI responses, the full-server should be deployed instead."

# Cleanup
rm -f stable.log full.log