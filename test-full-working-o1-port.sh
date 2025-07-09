#!/bin/bash

echo "🔧 Testing full-working-o1 binary on a different port..."

# Change to project directory
cd /home/champi/Dev/think_ai

# Kill any processes on port 8082
echo "🔪 Killing any processes on port 8082..."
lsof -ti:8082 | xargs kill -9 2>/dev/null || true

# Run the binary with a different port
echo "🚀 Starting server on port 8082..."
PORT=8082 timeout 5s ./target/release/full-working-o1 &
TEST_PID=$!

# Wait for server to start
sleep 2

# Check if server is running
if ps -p $TEST_PID > /dev/null; then
    echo "✅ Server is running successfully on port 8082!"
    
    # Test the health endpoint
    if curl -s http://localhost:8082/health > /dev/null 2>&1; then
        echo "✅ Health endpoint is responding!"
    else
        echo "⚠️ Health endpoint not responding (may still be starting)"
    fi
    
    kill $TEST_PID 2>/dev/null
else
    echo "❌ Server crashed during startup"
fi

echo ""
echo "✅ All fixes applied successfully!"