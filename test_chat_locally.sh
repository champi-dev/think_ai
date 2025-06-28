#!/bin/bash

# Test Think AI Chat System Locally
# This script provides multiple ways to test the improved conversation system

echo "🧠 Think AI Local Testing Script"
echo "================================"

# Check if binary exists
if [ ! -f "./target/release/think-ai" ]; then
    echo "❌ Binary not found. Building..."
    cargo build --release --bin think-ai
    if [ $? -ne 0 ]; then
        echo "❌ Build failed!"
        exit 1
    fi
fi

echo ""
echo "🎯 Available Testing Options:"
echo ""
echo "1. 💬 Interactive CLI Chat"
echo "   ./target/release/think-ai chat"
echo ""
echo "2. 🌐 HTTP Server + Web Interface"
echo "   ./target/release/think-ai server"
echo "   Then open: http://localhost:8080"
echo ""
echo "3. 🧪 Quick Conversation Test"
echo "   Test specific conversation patterns"
echo ""
echo "4. 📊 24-Hour Simulation Test"
echo "   Run conversation quality evaluation"
echo ""

read -p "Choose option (1-4): " choice

case $choice in
    1)
        echo "🚀 Starting Interactive CLI Chat..."
        echo "💡 Try these conversation starters:"
        echo "   - Hi there!"
        echo "   - What did we talk about earlier?"
        echo "   - I think AI is fascinating"
        echo "   - Tell me about consciousness"
        echo ""
        ./target/release/think-ai chat
        ;;
    2)
        echo "🚀 Starting HTTP Server..."
        echo "💡 Server will be available at: http://localhost:8080"
        echo "📝 Test with curl:"
        echo '   curl -X POST http://localhost:8080/chat \\'
        echo '        -H "Content-Type: application/json" \\'
        echo '        -d '"'"'{"query": "Hello! How are you today?"}'"'"''
        echo ""
        ./target/release/think-ai server
        ;;
    3)
        echo "🧪 Running Quick Conversation Tests..."
        echo ""
        
        # Test conversational patterns
        echo "Testing context reference..."
        echo '{"query": "Remember what we talked about earlier?"}' | \
        curl -s -X POST http://localhost:8080/chat \
             -H "Content-Type: application/json" \
             -d @- | jq -r '.response' 2>/dev/null || echo "Server not running"
        
        echo ""
        echo "Testing philosophical engagement..."
        echo '{"query": "What do you think about consciousness?"}' | \
        curl -s -X POST http://localhost:8080/chat \
             -H "Content-Type: application/json" \
             -d @- | jq -r '.response' 2>/dev/null || echo "Server not running"
        
        echo ""
        echo "💡 Start server first with option 2, then run option 3"
        ;;
    4)
        echo "📊 Running 24-Hour Conversation Simulation..."
        if [ -f "24hr_conversation_simulator.py" ]; then
            python3 24hr_conversation_simulator.py
        else
            echo "❌ 24hr_conversation_simulator.py not found"
            echo "💡 This tests long-term conversation quality and context retention"
        fi
        ;;
    *)
        echo "❌ Invalid option. Try again."
        exit 1
        ;;
esac

echo ""
echo "✅ Testing completed!"
echo ""
echo "📋 Key Features to Test:"
echo "• Context retention (reference previous topics)"
echo "• Natural conversation flow"
echo "• Philosophical discussions"
echo "• Personal questions and engagement"
echo "• Technical knowledge queries"
echo ""
echo "🎯 Expected Improvements:"
echo "• Better context memory and topic references"
echo "• More engaging responses with questions"
echo "• Coherent responses that address input directly"
echo "• No random knowledge fallbacks for conversational queries"