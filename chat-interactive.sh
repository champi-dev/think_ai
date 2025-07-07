#!/bin/bash

# Interactive Chat with Think AI (Working Version)

echo "🤖 Think AI Interactive Chat"
echo "============================"
echo ""

# Kill any existing server
echo "Preparing..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Build
echo "Building server..."
if cargo build --release --bin full-server > /dev/null 2>&1; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed!"
    exit 1
fi

# Start server
echo "Starting server..."
./target/release/full-server > server.log 2>&1 &
SERVER_PID=$!

# Wait for server
echo "Waiting for AI systems to initialize..."
for i in {1..10}; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

# Verify server is ready
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "❌ Server failed to start"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Get stats
STATS=$(curl -s http://localhost:8080/api/stats)
KNOWLEDGE_COUNT=$(echo "$STATS" | jq -r '.knowledge_base.total_knowledge // 0' 2>/dev/null || echo "0")

echo "✅ Server ready with $KNOWLEDGE_COUNT knowledge items!"
echo ""
echo "💬 Chat Commands:"
echo "  - Type your message and press Enter"
echo "  - Type 'quit' to exit"
echo ""
echo "====================================="
echo ""

# Function to send message
send_message() {
    local query="$1"
    local response=$(curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\"}" 2>/dev/null)
    
    if [ -n "$response" ]; then
        echo "$response" | jq -r '.response // "Error: No response"' 2>/dev/null || echo "Error: Failed to parse response"
    else
        echo "Error: No response from server"
    fi
}

# Interactive loop using a different approach
while true; do
    # Use printf instead of echo -n for better compatibility
    printf "You: "
    
    # Read user input
    IFS= read -r user_input || break
    
    # Check for exit
    if [ "$user_input" = "quit" ] || [ "$user_input" = "exit" ]; then
        echo "Goodbye!"
        break
    fi
    
    # Skip empty input
    if [ -z "$user_input" ]; then
        continue
    fi
    
    # Get and display response
    printf "AI: "
    send_message "$user_input"
    echo ""
done

# Cleanup
kill $SERVER_PID 2>/dev/null
echo "Chat session ended."