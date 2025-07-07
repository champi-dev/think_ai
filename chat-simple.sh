#!/bin/bash

# Simple Interactive Chat with Think AI

echo "🤖 Think AI Chat (Simple Version)"
echo "================================="

# Kill any existing server
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Build and start server
echo "Building server..."
if cargo build --release --bin full-server > /dev/null 2>&1; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed!"
    exit 1
fi

echo "Starting server..."
./target/release/full-server > server.log 2>&1 &
SERVER_PID=$!

# Wait for server
echo "Waiting for server..."
sleep 5

# Check if server is running
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "❌ Server failed to start. Check server.log"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo "✅ Server ready! Type 'quit' to exit."
echo ""

# Chat loop
while true; do
    echo -n "You: "
    read user_input
    
    if [ "$user_input" = "quit" ] || [ "$user_input" = "exit" ]; then
        break
    fi
    
    if [ -z "$user_input" ]; then
        continue
    fi
    
    # Send request and get response
    response=$(curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$user_input\"}" | jq -r '.response // "Error: No response"')
    
    echo "AI: $response"
    echo ""
done

# Cleanup
echo "Stopping server..."
kill $SERVER_PID 2>/dev/null
echo "Goodbye!"