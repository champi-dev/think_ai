#!/bin/bash
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Think AI Quantum Generation Server Starting...           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if Ollama is running
echo -e "${YELLOW}Checking Ollama status...${NC}"
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${RED}✗ Ollama not running${NC}"
    echo "Starting Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 5
fi

# Check for Qwen model
if ! ollama list 2>/dev/null | grep -q "qwen2.5:1.5b"; then
    echo -e "${YELLOW}Installing Qwen 2.5 model...${NC}"
    ollama pull qwen2.5:1.5b
fi

echo -e "${GREEN}✅ Ollama ready with Qwen model${NC}"

# Kill any existing instance
pkill -f full-working-o1 || true
sleep 2

# Start the server with quantum features
export RUST_LOG=info
export THINK_AI_QUANTUM_ENABLED=true
./full-working-o1 &
SERVER_PID=$!

echo "Server started with PID: $SERVER_PID"
echo ""
echo -e "${GREEN}✅ Quantum Generation Features:${NC}"
echo "  - Qwen-only generation (no fallback)"
echo "  - Isolated parallel threads"
echo "  - Shared intelligence system"
echo "  - O(1) performance with caching"
echo ""

# Start ngrok if not already running
if ! pgrep -x "ngrok" > /dev/null; then
    echo -e "${YELLOW}Starting ngrok tunnel...${NC}"
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

echo ""
echo -e "${GREEN}📋 Available endpoints:${NC}"
echo "  $NGROK_URL/health - Health check"
echo "  $NGROK_URL/api/chat - Chat API (Qwen-powered)"
echo "  $NGROK_URL/api/parallel-chat - Quantum consciousness chat"
echo "  $NGROK_URL/api/quantum-chat - NEW: Quantum generation endpoint"
echo "  $NGROK_URL/api/knowledge/stats - Knowledge statistics"
echo "  $NGROK_URL/api/benchmark - Performance benchmark"
echo ""
echo "Server is running. Press Ctrl+C to stop."

# Monitor server health
monitor_server() {
    while true; do
        sleep 30
        if ! kill -0 $SERVER_PID 2>/dev/null; then
            echo -e "${RED}Server crashed! Restarting...${NC}"
            exec $0
        fi
    done
}

monitor_server &
MONITOR_PID=$!

# Keep script running
trap "kill $SERVER_PID $MONITOR_PID 2>/dev/null; exit" INT
wait
