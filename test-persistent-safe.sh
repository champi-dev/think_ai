#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Think AI Persistent Chat Test (Safe Mode - Port 8081) ===${NC}"
echo ""

# Use a different port for testing
TEST_PORT=8081

# Kill any existing processes on test port
echo -e "${YELLOW}Killing any processes on port $TEST_PORT...${NC}"
lsof -ti:$TEST_PORT | xargs kill -9 2>/dev/null || true
sleep 1

# Start the server on test port
echo -e "${YELLOW}Starting Think AI Persistent server on port $TEST_PORT...${NC}"
PORT=$TEST_PORT ./target/release/think-ai-full-persistent &
SERVER_PID=$!
echo "Test Server PID: $SERVER_PID"

# Wait for server to start
echo -e "${YELLOW}Waiting for test server to start...${NC}"
sleep 3

# Quick health check
if curl -s http://localhost:$TEST_PORT/health > /dev/null 2>&1; then
    echo -e "${GREEN}Test server is running on port $TEST_PORT!${NC}"
else
    echo -e "${RED}Test server failed to start!${NC}"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo -e "${GREEN}You can now test manually on port $TEST_PORT${NC}"
echo "- Web UI: http://localhost:$TEST_PORT"
echo "- API: http://localhost:$TEST_PORT/api/chat"
echo ""
echo "Press Ctrl+C to stop the test server"

# Keep the server running
wait $SERVER_PID