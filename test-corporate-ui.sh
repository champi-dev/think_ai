#!/bin/bash

echo "🚀 Testing Corporate UI with ngrok backend..."
echo ""

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

if [ -z "$NGROK_URL" ]; then
    echo "❌ Error: ngrok is not running or no tunnel found"
    echo "Please run: ngrok http 8080"
    exit 1
fi

echo "✅ ngrok URL: $NGROK_URL"
echo ""

# Test backend
echo "📡 Testing backend API..."
RESPONSE=$(curl -s -X POST "$NGROK_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"message":"Hello from test script"}' \
    | jq -r '.response')

if [ -z "$RESPONSE" ]; then
    echo "❌ Backend test failed"
    exit 1
fi

echo "✅ Backend response: $RESPONSE"
echo ""

# Open in browser
echo "🌐 Opening corporate UI in browser..."
echo "📍 URL: http://localhost:8080/corporate.html"
echo ""

# Check if xdg-open is available (Linux)
if command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:8080/corporate.html"
# Check if open is available (macOS)
elif command -v open &> /dev/null; then
    open "http://localhost:8080/corporate.html"
else
    echo "Please manually open: http://localhost:8080/corporate.html"
fi

echo "✨ Corporate UI Features:"
echo "  - Minimal, professional design"
echo "  - Award-winning CSS animations"
echo "  - Smooth transitions and micro-interactions"
echo "  - Enterprise-grade color scheme"
echo "  - Responsive layout"
echo "  - Connected to ngrok backend: $NGROK_URL"
echo ""
echo "🎯 Key Animations:"
echo "  - Header slide-down animation"
echo "  - Content fade-in with stagger"
echo "  - Message slide animations (left/right)"
echo "  - Typing indicator with dots"
echo "  - Button ripple effect on hover"
echo "  - Smooth skeleton loading states"
echo "  - Status indicator pulsing"
echo ""