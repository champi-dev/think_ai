#!/bin/bash

# Think AI Webapp Runner
# This script runs the Think AI server and provides access to the webapp

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVER_BINARY="./target/release/think-ai-server"
DEFAULT_PORT=8080
WAIT_TIME=3

echo -e "${BLUE}🧠 Think AI Webapp Runner${NC}"
echo "=================================="

# Check if server binary exists
if [[ ! -f "$SERVER_BINARY" ]]; then
    echo -e "${RED}❌ Server binary not found: $SERVER_BINARY${NC}"
    echo -e "${YELLOW}💡 Run 'cargo build --release' first${NC}"
    exit 1
fi

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    echo -e "${YELLOW}🔄 Killing processes on port $port...${NC}"
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
    sleep 1
}

# Function to find available port
find_port() {
    local start_port=${1:-8080}
    for ((port=start_port; port<=start_port+100; port++)); do
        if ! check_port $port; then
            echo $port
            return
        fi
    done
    echo 0
}

# Kill any existing servers
if check_port $DEFAULT_PORT; then
    kill_port $DEFAULT_PORT
fi

# Find available port
AVAILABLE_PORT=$(find_port $DEFAULT_PORT)
if [[ $AVAILABLE_PORT -eq 0 ]]; then
    echo -e "${RED}❌ No available ports found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Using port: $AVAILABLE_PORT${NC}"

# Start server in background
echo -e "${BLUE}🚀 Starting Think AI server...${NC}"
$SERVER_BINARY &
SERVER_PID=$!

# Wait for server to start
echo -e "${YELLOW}⏳ Waiting ${WAIT_TIME}s for server to start...${NC}"
sleep $WAIT_TIME

# Check if server is running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo -e "${RED}❌ Server failed to start${NC}"
    exit 1
fi

# Detect the actual port being used by the server
ACTUAL_PORT=""
for i in {1..10}; do
    SERVER_PORT=$(lsof -Pan -p $SERVER_PID -i 2>/dev/null | grep LISTEN | head -1 | sed 's/.*:\([0-9]*\).*/\1/' || echo "")
    if [[ -n "$SERVER_PORT" ]]; then
        ACTUAL_PORT=$SERVER_PORT
        break
    fi
    sleep 0.5
done

if [[ -z "$ACTUAL_PORT" ]]; then
    echo -e "${RED}❌ Could not detect server port${NC}"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

SERVER_URL="http://127.0.0.1:$ACTUAL_PORT"

echo -e "${GREEN}✅ Server running on port $ACTUAL_PORT${NC}"
echo -e "${BLUE}📡 Server URL: $SERVER_URL${NC}"

# Display available endpoints
echo ""
echo -e "${YELLOW}Available Endpoints:${NC}"
echo "  🩺 Health Check: $SERVER_URL/health"
echo "  🧮 Compute:      $SERVER_URL/compute (POST)"
echo "  🔍 Search:       $SERVER_URL/search (POST)"
echo "  📊 Stats:        $SERVER_URL/stats"

echo ""
echo -e "${YELLOW}⚠️  Note: Webapp UI is not yet integrated into the server${NC}"
echo -e "${BLUE}💡 For now, you can use the API endpoints directly${NC}"

# Test health endpoint
echo ""
echo -e "${BLUE}🔍 Testing server health...${NC}"
if curl -s -f "$SERVER_URL/health" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Server is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Health check failed, but server might still be starting${NC}"
fi

# Example API usage
echo ""
echo -e "${YELLOW}📝 Example API Usage:${NC}"
echo ""
echo "# Test compute endpoint:"
echo "curl -X POST $SERVER_URL/compute \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"query\": \"What is 2+2?\"}'"
echo ""
echo "# Test search endpoint:"
echo "curl -X POST $SERVER_URL/search \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"query\": \"artificial intelligence\", \"limit\": 5}'"

# Option to open browser
echo ""
read -p "$(echo -e ${YELLOW}❓ Open health endpoint in browser? [y/N]: ${NC})" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v xdg-open >/dev/null; then
        xdg-open "$SERVER_URL/health"
    elif command -v open >/dev/null; then
        open "$SERVER_URL/health"
    else
        echo -e "${YELLOW}⚠️  Could not detect browser command${NC}"
        echo -e "${BLUE}💡 Manually open: $SERVER_URL/health${NC}"
    fi
fi

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down server...${NC}"
    kill $SERVER_PID 2>/dev/null || true
    echo -e "${GREEN}✅ Server stopped${NC}"
}

# Set trap for cleanup
trap cleanup EXIT INT TERM

# Keep script running
echo ""
echo -e "${GREEN}🟢 Server is running. Press Ctrl+C to stop.${NC}"
echo -e "${BLUE}📖 Server logs will appear below:${NC}"
echo "=================================="

# Wait for server process
wait $SERVER_PID