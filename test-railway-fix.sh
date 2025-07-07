#!/bin/bash

echo "🚀 Testing Railway PORT fix..."
echo "================================"

# Build the project
echo "📦 Building full-working-o1..."
cargo build --release --bin full-working-o1

# Test 1: Default behavior (no PORT)
echo -e "\n🧪 Test 1: Running without PORT (should use 8080)"
timeout 5s ./target/release/full-working-o1 &
PID=$!
sleep 2
curl -s http://localhost:8080/health && echo "✅ Server responds on 8080" || echo "❌ No response on 8080"
kill $PID 2>/dev/null
wait $PID 2>/dev/null

# Test 2: Railway simulation (PORT=3000)  
echo -e "\n🧪 Test 2: Running with PORT=3000 (Railway simulation)"
PORT=3000 timeout 5s ./target/release/full-working-o1 &
PID=$!
sleep 2
curl -s http://localhost:3000/health && echo "✅ Server responds on 3000" || echo "❌ No response on 3000"
kill $PID 2>/dev/null
wait $PID 2>/dev/null

echo -e "\n================================"
echo "✨ Tests complete! Deploy with: git add -A && git commit -m 'Fix Railway PORT binding' && git push"