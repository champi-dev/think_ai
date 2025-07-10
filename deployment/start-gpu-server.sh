#!/bin/bash
echo "🚀 Starting Think AI on GPU Server..."
echo "✅ All endpoints enabled:"
echo "  - /health"
echo "  - /api/chat"
echo "  - /api/parallel-chat (Quantum Consciousness)"
echo "  - /api/knowledge/stats"
echo "  - /api/benchmark"

# Kill any existing instance
pkill -f full-working-o1 || true
sleep 2

# Start the server
export RUST_LOG=info
./full-working-o1 &
SERVER_PID=$!

echo "Server started with PID: $SERVER_PID"
echo

# Start ngrok if not already running
if ! pgrep -x "ngrok" > /dev/null; then
    echo "🌐 Starting ngrok tunnel..."
    ngrok http 8080 > /dev/null 2>&1 &
    sleep 5
    
    # Get ngrok URL
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null || echo "")
    if [ -n "$NGROK_URL" ]; then
        echo -e "${GREEN}✅ Server accessible at: $NGROK_URL${NC}"
    else
        echo -e "${YELLOW}⚠️  Could not get ngrok URL. Check http://localhost:4040${NC}"
    fi
else
    echo "✅ ngrok already running"
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null || echo "")
    if [ -n "$NGROK_URL" ]; then
        echo "Server accessible at: $NGROK_URL"
    fi
fi

echo
echo "📋 Available endpoints:"
echo "  $NGROK_URL/health - Health check"
echo "  $NGROK_URL/api/chat - Chat API"
echo "  $NGROK_URL/api/parallel-chat - Quantum consciousness chat"
echo "  $NGROK_URL/api/knowledge/stats - Knowledge statistics"
echo "  $NGROK_URL/api/benchmark - Performance benchmark"
echo
echo "Server is running. Press Ctrl+C to stop."

# Keep script running
trap "kill $SERVER_PID 2>/dev/null; exit" INT
wait
