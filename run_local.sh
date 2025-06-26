#!/bin/bash

# Think AI - Local Development Runner
# Run the full system with terminal chat and web interface

set -e

echo "🧠 Think AI - Starting Full System"
echo "=================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Kill any existing processes
echo -e "${YELLOW}Cleaning up existing processes...${NC}"
pkill -f "think-ai server" || true
pkill -f "think-ai-webapp" || true
sleep 1

# Build if needed
if [ ! -f "./target/release/think-ai" ]; then
    echo -e "${YELLOW}Building Think AI...${NC}"
    cargo build --release
fi

# Start HTTP server in background
echo -e "\n${BLUE}Starting HTTP Server...${NC}"
./target/release/think-ai server &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"
sleep 2

# Check if webapp binary exists
if [ -f "./target/release/think-ai-webapp" ]; then
    echo -e "\n${BLUE}Starting WebApp...${NC}"
    ./target/release/think-ai-webapp &
    WEBAPP_PID=$!
    echo "WebApp PID: $WEBAPP_PID"
else
    echo -e "${YELLOW}WebApp binary not found. The webapp is served by the HTTP server.${NC}"
fi

# Wait for services to start
sleep 2

echo -e "\n${GREEN}✅ System Started Successfully!${NC}"
echo -e "=================================="
echo -e "${GREEN}Available Services:${NC}"
echo -e "• ${BLUE}Web Interface:${NC} http://localhost:8080"
echo -e "• ${BLUE}Health Check:${NC} http://localhost:8080/health"
echo -e "• ${BLUE}API Endpoint:${NC} http://localhost:8080/api/process"
echo -e "\n${GREEN}Terminal Chat:${NC}"
echo -e "In a new terminal, run: ${YELLOW}./target/release/think-ai chat${NC}"
echo -e "\n${YELLOW}Press Ctrl+C to stop all services${NC}"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down...${NC}"
    kill $SERVER_PID 2>/dev/null || true
    [ ! -z "$WEBAPP_PID" ] && kill $WEBAPP_PID 2>/dev/null || true
    echo -e "${GREEN}Stopped all services${NC}"
    exit 0
}

# Set trap for cleanup
trap cleanup INT TERM

# Keep script running
while true; do
    sleep 1
done