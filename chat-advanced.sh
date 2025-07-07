#!/bin/bash

# Advanced Interactive Chat with Think AI Server

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored text
print_color() {
    echo -e "${1}${2}${NC}"
}

# Function to wrap text
wrap_text() {
    echo "$1" | fold -s -w 80
}

# Banner
clear
print_color "$CYAN" "╔══════════════════════════════════════════════════════════════════════╗"
print_color "$CYAN" "║                    🤖 Think AI Interactive Chat                      ║"
print_color "$CYAN" "║                    O(1) Performance AI Assistant                     ║"
print_color "$CYAN" "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Kill any existing server
print_color "$YELLOW" "🔧 Preparing environment..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Build the stable server
print_color "$YELLOW" "🔨 Building Think AI server..."
if ! cargo build --release --bin stable-server 2>&1 | grep -E "(error|warning)" > build.log; then
    print_color "$GREEN" "✅ Build successful!"
else
    print_color "$RED" "⚠️  Build completed with warnings. See build.log for details."
fi

# Start the server
print_color "$YELLOW" "🚀 Starting server on port 8080..."
./target/release/stable-server > server.log 2>&1 &
SERVER_PID=$!

# Wait for server
sleep 3

# Check if server is running
if ! ps -p $SERVER_PID > /dev/null; then
    print_color "$RED" "❌ Server failed to start!"
    print_color "$RED" "Check server.log for details:"
    tail -20 server.log
    exit 1
fi

print_color "$GREEN" "✅ Server is running!"
echo ""
print_color "$BLUE" "💬 Chat Commands:"
print_color "$BLUE" "  - Type your message and press Enter"
print_color "$BLUE" "  - Type 'help' for example queries"
print_color "$BLUE" "  - Type 'stats' to see server statistics"
print_color "$BLUE" "  - Type 'clear' to clear the screen"
print_color "$BLUE" "  - Type 'quit' or 'exit' to stop"
echo ""
print_color "$CYAN" "════════════════════════════════════════════════════════════════════════"
echo ""

# Conversation counter
TURN=0

# Chat loop
while true; do
    # Prompt
    print_color "$GREEN" -n "You: "
    read -r user_input
    
    # Handle commands
    case "$user_input" in
        "quit"|"exit")
            print_color "$YELLOW" "👋 Ending conversation..."
            break
            ;;
        "clear")
            clear
            print_color "$CYAN" "🧹 Screen cleared. Continue chatting!"
            echo ""
            continue
            ;;
        "help")
            echo ""
            print_color "$BLUE" "📚 Example queries you can try:"
            echo "  • What is O(1) complexity?"
            echo "  • How does Think AI achieve constant time performance?"
            echo "  • Explain hash-based lookups"
            echo "  • What are the key features of Think AI?"
            echo "  • Tell me about linear attention mechanisms"
            echo "  • How does quantization improve performance?"
            echo ""
            continue
            ;;
        "stats")
            echo ""
            print_color "$BLUE" "📊 Server Statistics:"
            curl -s http://localhost:8080/api/stats | jq '.' || echo "Could not fetch stats"
            echo ""
            continue
            ;;
        "")
            continue
            ;;
    esac
    
    # Increment turn counter
    ((TURN++))
    
    # Show thinking indicator
    print_color "$YELLOW" -n "🤔 Thinking"
    
    # Make API call with timeout
    start_time=$(date +%s%3N)
    response=$(timeout 10 curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$user_input\"}" 2>/dev/null)
    end_time=$(date +%s%3N)
    
    # Clear thinking indicator
    echo -e "\r\033[K"
    
    if [ $? -eq 124 ]; then
        print_color "$RED" "⏱️  Request timed out after 10 seconds"
        echo ""
        continue
    fi
    
    # Parse response
    if [ -n "$response" ]; then
        message=$(echo "$response" | jq -r '.response // empty' 2>/dev/null)
        response_time=$(echo "$response" | jq -r '.response_time_ms // empty' 2>/dev/null)
        
        if [ -n "$message" ]; then
            # Display response with formatting
            print_color "$CYAN" "Think AI: "
            wrap_text "$message" | while IFS= read -r line; do
                echo "  $line"
            done
            
            # Show performance metrics
            if [ -n "$response_time" ]; then
                actual_time=$((end_time - start_time))
                print_color "$YELLOW" "  ⚡ Response time: ${response_time}ms (actual: ${actual_time}ms)"
            fi
        else
            print_color "$RED" "❌ Error: Invalid response from server"
        fi
    else
        print_color "$RED" "❌ Error: No response from server"
    fi
    
    echo ""
done

# Cleanup
echo ""
print_color "$YELLOW" "📊 Session Summary:"
echo "  • Total turns: $TURN"
echo "  • Server uptime: $(ps -o etime= -p $SERVER_PID | xargs)"
echo ""

print_color "$YELLOW" "🛑 Stopping server..."
kill $SERVER_PID 2>/dev/null

# Clean up files
rm -f server.log build.log

print_color "$GREEN" "✨ Thanks for chatting with Think AI!"
print_color "$CYAN" "════════════════════════════════════════════════════════════════════════"