#!/bin/bash

echo "🔨 Building Think AI with knowledge fix..."
echo "=========================================="

# Kill any existing processes on port 8080
echo "📍 Killing existing processes on port 8080..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Build in release mode
echo "🏗️  Building release version..."
cargo build --release

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"
echo ""

# Start the server
echo "🚀 Starting Think AI server..."
./target/release/think-ai server &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to initialize..."
sleep 5

# Test the API
echo ""
echo "🧪 Testing API endpoints..."
echo "=========================================="

# Test greeting
echo "Test 1: Greeting"
curl -s -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}' | jq '.'

echo ""
echo "Test 2: JavaScript query"
curl -s -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is JavaScript?"}' | jq '.'

echo ""
echo "Test 3: Python query"
curl -s -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Python"}' | jq '.'

echo ""
echo "Test 4: Quantum mechanics query"
curl -s -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain quantum mechanics"}' | jq '.'

echo ""
echo "Test 5: Unknown topic"
curl -s -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "random gibberish xyz123"}' | jq '.'

echo ""
echo "=========================================="
echo "✅ Tests completed!"
echo ""
echo "Server is running on PID: $SERVER_PID"
echo "To stop the server: kill $SERVER_PID"
echo ""
echo "You can also test the CLI chat:"
echo "./target/release/think-ai chat"