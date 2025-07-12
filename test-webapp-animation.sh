#!/bin/bash

# Test webapp with new animation locally
echo "🚀 Testing Think AI webapp with enhanced streaming animation..."

# Kill any existing processes on port 5555
echo "Cleaning up port 5555..."
lsof -ti:5555 | xargs kill -9 2>/dev/null || true

# Build the server if needed
echo "Building server..."
cd /home/administrator/think_ai
cargo build --release --bin stable-server

# Start the server on port 5555
echo "Starting server on port 5555..."
PORT=5555 RUST_LOG=info ./target/release/stable-server &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Check if server is running
if ! curl -s http://localhost:5555/health > /dev/null; then
    echo "❌ Server failed to start"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo "✅ Server started successfully on port 5555"
echo ""
echo "🌐 Open http://localhost:5555 in your browser to test the new animation"
echo ""
echo "📝 What to test:"
echo "  1. Type a message and click 'Send' or press Enter"
echo "  2. You should see:"
echo "     - Neural network spinning animation"
echo "     - 'Thinking' text with animated dots"
echo "     - Response text streaming in character by character"
echo ""
echo "Press Ctrl+C to stop the server"

# Wait for user to stop
trap "echo 'Stopping server...'; kill $SERVER_PID 2>/dev/null; exit 0" INT
wait $SERVER_PID