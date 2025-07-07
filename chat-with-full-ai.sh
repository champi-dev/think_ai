#!/bin/bash

# Chat with Full Think AI Server (with actual AI responses)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

print_color() {
    echo -e "${1}${2}${NC}"
}

clear
print_color "$CYAN" "╔══════════════════════════════════════════════════════════════════════╗"
print_color "$CYAN" "║              🧠 Think AI Full Server - Interactive Chat              ║"
print_color "$CYAN" "║         Real AI Responses with O(1) Performance Optimization         ║"
print_color "$CYAN" "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Kill any existing server
print_color "$YELLOW" "🔧 Preparing environment..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Build the FULL server with actual AI components
print_color "$YELLOW" "🔨 Building Full AI Server (this may take a moment)..."
if ! cargo build --release --bin full-server > build.log 2>&1; then
    print_color "$RED" "❌ Build failed! Check build.log for details"
    tail -20 build.log
    exit 1
fi
print_color "$GREEN" "✅ Build successful!"

# Check if knowledge files exist
if [ -d "./knowledge_files" ]; then
    print_color "$GREEN" "📚 Knowledge files found!"
else
    print_color "$YELLOW" "⚠️  Knowledge files not found - AI will use built-in knowledge only"
fi

# Start the full server
print_color "$YELLOW" "🚀 Starting Full AI Server..."
./target/release/full-server > server.log 2>&1 &
SERVER_PID=$!

# Wait for server with progress indicator
echo -n "⏳ Waiting for AI systems to initialize"
for i in {1..10}; do
    sleep 1
    echo -n "."
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo ""
        break
    fi
done

# Check if server is running
if ! ps -p $SERVER_PID > /dev/null; then
    print_color "$RED" "❌ Server failed to start!"
    echo "Last 20 lines of server.log:"
    tail -20 server.log
    exit 1
fi

# Get server stats
stats=$(curl -s http://localhost:8080/api/stats 2>/dev/null)
if [ -n "$stats" ]; then
    knowledge_count=$(echo "$stats" | jq -r '.knowledge_base.total_knowledge // 0')
    print_color "$GREEN" "✅ AI Server is ready with $knowledge_count knowledge items!"
else
    print_color "$GREEN" "✅ AI Server is ready!"
fi

echo ""
print_color "$BLUE" "💬 You can now chat with the real Think AI system!"
print_color "$BLUE" "Type 'help' for example queries, 'quit' to exit"
echo ""
print_color "$CYAN" "════════════════════════════════════════════════════════════════════════"
echo ""

# Chat loop
while true; do
    echo -ne "${GREEN}You: ${NC}"
    read -r user_input
    
    case "$user_input" in
        "quit"|"exit")
            print_color "$YELLOW" "👋 Ending conversation..."
            break
            ;;
        "help")
            echo ""
            print_color "$BLUE" "📚 Try asking me about:"
            echo "  • Scientific concepts (physics, chemistry, biology)"
            echo "  • Technology and programming"
            echo "  • Philosophy and consciousness"
            echo "  • Mathematics and algorithms"
            echo "  • O(1) performance optimization"
            echo "  • Machine learning and AI"
            echo ""
            continue
            ;;
        "")
            continue
            ;;
    esac
    
    # Show thinking indicator
    echo -ne "${YELLOW}🤔 Thinking${NC}"
    
    # Make API call
    start_time=$(date +%s%3N)
    response=$(curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$user_input\"}" 2>/dev/null)
    end_time=$(date +%s%3N)
    
    # Clear thinking indicator
    echo -e "\r\033[K"
    
    if [ -n "$response" ]; then
        message=$(echo "$response" | jq -r '.response // empty' 2>/dev/null)
        context=$(echo "$response" | jq -r '.context[]? // empty' 2>/dev/null | tr '\n' ', ' | sed 's/,$//')
        response_time=$(echo "$response" | jq -r '.response_time_ms // empty' 2>/dev/null)
        
        if [ -n "$message" ]; then
            # Display response
            print_color "$CYAN" "Think AI:"
            echo "$message" | fold -s -w 72 | while IFS= read -r line; do
                echo "  $line"
            done
            
            # Show metadata
            if [ -n "$context" ] && [ "$context" != "greeting" ]; then
                print_color "$YELLOW" "  📖 Context: $context"
            fi
            if [ -n "$response_time" ]; then
                actual_time=$((end_time - start_time))
                print_color "$YELLOW" "  ⚡ Response: ${response_time}ms (network: ${actual_time}ms)"
            fi
        else
            print_color "$RED" "❌ Error: Could not parse response"
            echo "Raw response: $response"
        fi
    else
        print_color "$RED" "❌ Error: No response from server"
    fi
    
    echo ""
done

# Cleanup
echo ""
print_color "$YELLOW" "🛑 Stopping server..."
kill $SERVER_PID 2>/dev/null
rm -f server.log build.log

print_color "$GREEN" "✨ Thanks for chatting with Think AI!"