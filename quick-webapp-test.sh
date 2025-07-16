#!/bin/bash
set -e

echo "🚀 Quick 3D webapp test..."

# Kill any existing processes on port 8080
pkill -f "full-working-o1" || true
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Check if binary exists, build if not
if [ ! -f "./target/release/full-working-o1" ]; then
    echo "🔨 Building binary (this may take a minute)..."
    cargo build --release --bin full-working-o1
fi

# Start server in background
echo "🌐 Starting server..."
./target/release/full-working-o1 &
SERVER_PID=$!

# Wait for server
sleep 3

# Test if 3D webapp is served
echo "🧪 Testing if 3D webapp is served..."
if curl -s http://localhost:8080/ | grep -q "Think AI - Hierarchical Knowledge"; then
    echo "✅ 3D webapp is being served successfully!"
    echo ""
    echo "📋 Deployment ready! To deploy:"
    echo "   git add -A"
    echo "   git commit -m 'Deploy 3D visualization webapp'"
    echo "   git push"
else
    echo "❌ 3D webapp NOT found - checking what's being served..."
    curl -s http://localhost:8080/ | head -20
fi

# Cleanup
kill $SERVER_PID 2>/dev/null || true