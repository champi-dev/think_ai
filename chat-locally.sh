#!/bin/bash

# Interactive Chat with Think AI Server

echo "🤖 Think AI Interactive Chat"
echo "============================"

# Kill any existing server on port 8080
echo "🔧 Preparing environment..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Build the stable server binary
echo "🔨 Building server..."
cargo build --release --bin stable-server

# Check if build succeeded
if [ $? -ne 0 ]; then
    echo "❌ Build failed. Exiting."
    exit 1
fi

# Start the server in background
echo "🚀 Starting server..."
./target/release/stable-server > server.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Check if server is running
if ! ps -p $SERVER_PID > /dev/null; then
    echo "❌ Server failed to start. Check server.log for details."
    exit 1
fi

echo "✅ Server is running!"
echo ""
echo "💬 Chat Interface Ready"
echo "Type 'quit' or 'exit' to stop"
echo "================================"
echo ""

# Chat loop
while true; do
    # Get user input
    echo -n "You: "
    read -r user_input
    
    # Check for exit commands
    if [[ "$user_input" == "quit" ]] || [[ "$user_input" == "exit" ]]; then
        echo "👋 Goodbye!"
        break
    fi
    
    # Skip empty input
    if [[ -z "$user_input" ]]; then
        continue
    fi
    
    # Send request to server
    echo -n "Think AI: "
    
    # Make the API call and extract just the response field
    response=$(curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$user_input\"}" | jq -r '.response // "Error: Could not get response"')
    
    # Display the response
    echo "$response"
    echo ""
done

# Cleanup
echo "🛑 Stopping server..."
kill $SERVER_PID 2>/dev/null
rm -f server.log

echo "✨ Chat session ended"