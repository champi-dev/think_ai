#!/bin/bash
set -e

echo "🚀 Testing 3D webapp locally..."

# Kill any existing processes on port 8080
echo "📌 Killing any existing processes on port 8080..."
pkill -f "full-working-o1" || true
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Build the binary
echo "🔨 Building full-working-o1 binary..."
cargo build --release --bin full-working-o1

# Start the server in background
echo "🌐 Starting the server..."
./target/release/full-working-o1 &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Test if server is running
echo "🧪 Testing server endpoints..."
echo "1. Testing root endpoint (3D webapp)..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ || echo "Failed to connect"

echo -e "\n2. Testing health endpoint..."
curl -s http://localhost:8080/health || echo "Failed"

echo -e "\n3. Testing if 3D webapp content is served..."
curl -s http://localhost:8080/ | grep -q "Think AI - Hierarchical Knowledge" && echo "✅ 3D webapp is being served!" || echo "❌ 3D webapp NOT found"

echo -e "\n4. Testing chat endpoint..."
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"Hello, Think AI with Qwen!"}' | jq '.' || echo "Failed"

# Clean up
echo -e "\n🧹 Cleaning up..."
kill $SERVER_PID 2>/dev/null || true

echo -e "\n✨ Test complete!"
echo "To deploy to Railway: git add -A && git commit -m 'Deploy 3D webapp' && git push"