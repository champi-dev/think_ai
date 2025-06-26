#!/bin/bash

echo "🚀 Building and running Think AI with chat interface..."

# Kill any existing process on port 8080
echo "Stopping any existing server on port 8080..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Build the project
echo "Building Think AI..."
cargo build --release

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"

# Start the HTTP server
echo "Starting HTTP server on port 8080..."
./target/release/think-ai-server &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Check if server is running
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server is running!"
    echo ""
    echo "📝 Chat interface available at: http://localhost:8080/chat.html"
    echo "🌐 Main webapp available at: http://localhost:8080/"
    echo ""
    echo "Press Ctrl+C to stop the server..."
    
    # Wait for Ctrl+C
    trap "echo ''; echo 'Stopping server...'; kill $SERVER_PID 2>/dev/null; exit" INT
    wait $SERVER_PID
else
    echo "❌ Server failed to start!"
    exit 1
fi