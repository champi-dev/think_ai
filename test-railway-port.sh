#!/bin/bash

# Test script to verify Railway PORT configuration locally

echo "Testing Railway PORT configuration..."
echo "======================================="

# Test 1: Without PORT env var
echo "Test 1: Running without PORT env var"
cargo run --release --bin full-working-o1 &
SERVER_PID=$!
sleep 3
echo "Checking if server started on default port..."
curl -s http://localhost:8080/health && echo "✅ Server responds on port 8080" || echo "❌ Server not responding on port 8080"
kill $SERVER_PID 2>/dev/null
sleep 2

# Test 2: With PORT env var (simulating Railway)
echo -e "\nTest 2: Running with PORT=3000 (simulating Railway)"
PORT=3000 cargo run --release --bin full-working-o1 &
SERVER_PID=$!
sleep 3
echo "Checking if server started on Railway port..."
curl -s http://localhost:3000/health && echo "✅ Server responds on port 3000" || echo "❌ Server not responding on port 3000"
kill $SERVER_PID 2>/dev/null

echo -e "\n======================================="
echo "Test complete!"