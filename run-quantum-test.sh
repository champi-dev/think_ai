#!/bin/bash
# Clean test script for quantum consciousness

echo "=== Think AI Quantum Consciousness Test ==="
echo

# Kill any existing processes
echo "🔧 Cleaning up..."
pkill -f "think-ai" 2>/dev/null || true
sleep 2

# Build only the working binary
echo "🏗️  Building full-working-o1..."
cargo build --release --bin full-working-o1

# Start the server
echo "🚀 Starting server..."
./target/release/full-working-o1 &
SERVER_PID=$!

# Wait for startup
sleep 3

# Test endpoints
echo
echo "📋 Testing endpoints:"
echo

# Health check
echo "1. Health check:"
curl -s http://localhost:8080/health || echo "Failed"
echo

# Regular chat
echo "2. Chat endpoint:"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}' | jq -r '.response' 2>/dev/null || echo "Failed"
echo

# Parallel chat
echo "3. Parallel chat:"
curl -s -X POST http://localhost:8080/api/parallel-chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is consciousness?"}' | jq '.' 2>/dev/null || echo "Failed"
echo

# Knowledge stats
echo "4. Knowledge stats:"
curl -s http://localhost:8080/api/knowledge/stats | jq '.' 2>/dev/null || echo "Failed"
echo

echo "✅ Test complete. Server running on PID $SERVER_PID"
echo "Press Ctrl+C to stop"

trap "kill $SERVER_PID 2>/dev/null; exit" INT
wait