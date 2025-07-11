#!/bin/bash

echo "🚀 Testing Think AI Streaming Functionality"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Kill existing processes on test port
echo -e "${BLUE}🛑 Cleaning up port 3456...${NC}"
lsof -ti:3456 | xargs kill -9 2>/dev/null || true
sleep 2

# Start local server with streaming support
echo -e "${BLUE}🚀 Starting local server with streaming...${NC}"
if [ -f "deployment-quantum/full-working-o1" ]; then
    PORT=3456 nohup ./deployment-quantum/full-working-o1 > /tmp/streaming-server.log 2>&1 &
    SERVER_PID=$!
    echo "Server started with PID: $SERVER_PID"
else
    echo -e "${RED}❌ Binary not found${NC}"
    exit 1
fi

# Wait for server to start
echo -e "${BLUE}⏳ Waiting for server to start...${NC}"
sleep 3

# Check if server is running
if ! curl -s http://localhost:3456/health > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Server may not be ready yet${NC}"
fi

echo ""
echo -e "${BLUE}📡 Testing Streaming API...${NC}"
echo "=========================="

# Test 1: Basic streaming test
echo -e "${BLUE}Test 1: Basic SSE streaming${NC}"
echo "Sending request to /api/chat/stream..."
echo ""

# Use curl to test SSE endpoint
curl -N -X POST http://localhost:3456/api/chat/stream \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"message": "Tell me about O(1) performance in 3 sentences"}' \
  2>/dev/null | while IFS= read -r line; do
    if [[ $line == data:* ]]; then
        # Extract JSON from SSE data
        json=${line#data: }
        if [ ! -z "$json" ]; then
            echo "$json" | jq -r '.chunk' 2>/dev/null || echo "$json"
        fi
    fi
done &

STREAM_PID=$!

# Let it stream for a few seconds
sleep 5
kill $STREAM_PID 2>/dev/null || true

echo ""
echo ""
echo -e "${BLUE}Test 2: Regular chat endpoint (for comparison)${NC}"
echo "Sending request to /api/chat..."
curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is O(1)?"}' | jq . 2>/dev/null || echo "Response received"

echo ""
echo ""
echo -e "${BLUE}Test 3: Browser access${NC}"
echo "You can test streaming in your browser:"
echo -e "${GREEN}1. Open: http://localhost:3456/static/chat_streaming.html${NC}"
echo -e "${GREEN}2. Or use SSH tunnel: ssh -L 3456:localhost:3456 administrator@<SERVER-IP>${NC}"

echo ""
echo -e "${BLUE}📊 Streaming endpoints available:${NC}"
echo "  POST /api/chat/stream - SSE streaming endpoint"
echo "  POST /api/chat - Regular endpoint"
echo ""

# Cleanup function
cleanup() {
    echo -e "\n${BLUE}🛑 Cleaning up...${NC}"
    kill $SERVER_PID 2>/dev/null || true
    echo -e "${GREEN}✅ Done${NC}"
}

trap cleanup EXIT

echo "Server is running. Press Ctrl+C to stop..."
echo ""
echo -e "${YELLOW}💡 Note: If streaming endpoint returns 404, the server may need to be rebuilt with streaming support.${NC}"
echo -e "${YELLOW}   In that case, streaming falls back to regular chat which still works fine.${NC}"

# Keep script running
wait $SERVER_PID