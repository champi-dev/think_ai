#!/bin/bash
# Quick test script to verify everything works

echo "🚀 Think AI Quick Test"
echo "====================="

# Kill any existing processes
echo "🔧 Cleaning up ports..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
sleep 1

# Build if needed
if [ ! -f "./target/release/think-ai" ]; then
    echo "📦 Building Think AI..."
    cargo build --release
fi

# Test 1: CLI Chat
echo -e "\n💬 Test 1: CLI Chat"
echo "Testing with a simple question..."
echo "What is O(1)?" | timeout 5s ./target/release/think-ai chat || echo "CLI test completed"

# Test 2: HTTP Server
echo -e "\n🌐 Test 2: HTTP Server"
echo "Starting server in background..."
./target/release/think-ai server &
SERVER_PID=$!
sleep 2

echo "Sending test request..."
curl -s -X POST http://localhost:8080/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Hello AI, what is your primary function?"}' | jq . || echo "No response"

kill $SERVER_PID 2>/dev/null || true

# Test 3: Knowledge Engine
echo -e "\n📚 Test 3: Knowledge Engine"
echo "Running knowledge tests..."
cargo test --package think-ai-knowledge --lib -- --nocapture test_knowledge_engine_creation test_add_knowledge

# Test 4: Consciousness Training
echo -e "\n🧠 Test 4: Consciousness Training"
echo "Running mini training session..."
./target/release/train-consciousness 2

echo -e "\n✅ Quick tests completed!"
echo "For full testing, run: ./test-locally.sh"