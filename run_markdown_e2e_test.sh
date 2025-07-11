#!/bin/bash

# E2E Markdown Rendering Test for Think AI
# This script tests markdown rendering with screenshots as evidence

echo "==================================================================="
echo "Think AI Markdown Rendering E2E Test"
echo "==================================================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Kill any existing processes on required ports
echo -e "${YELLOW}Cleaning up existing processes...${NC}"
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
lsof -ti:8090 | xargs kill -9 2>/dev/null || true
sleep 2

# Build the project
echo -e "\n${YELLOW}Building Think AI...${NC}"
cargo build --release
if [ $? -ne 0 ]; then
    echo -e "${RED}Build failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Build successful${NC}"

# Start Think AI server
echo -e "\n${YELLOW}Starting Think AI server...${NC}"
./target/release/think-ai server > server_test.log 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Wait for server to start
echo "Waiting for server to start..."
for i in {1..30}; do
    if curl -s http://localhost:8080/health > /dev/null; then
        echo -e "${GREEN}✓ Server is ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}✗ Server failed to start${NC}"
        cat server_test.log
        kill $SERVER_PID 2>/dev/null
        exit 1
    fi
    sleep 1
done

# Run the E2E test
echo -e "\n${YELLOW}Running E2E markdown rendering test...${NC}"
python3 test_markdown_rendering.py

TEST_EXIT_CODE=$?

# Stop the server
echo -e "\n${YELLOW}Stopping server...${NC}"
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

# Check test results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}==================================================================="
    echo -e "✓ E2E TEST PASSED"
    echo -e "===================================================================${NC}"
    echo -e "\nEvidence generated:"
    echo "  - Screenshots: ./screenshots/"
    echo "  - HTML Report: ./markdown_test_report.html"
    echo "  - JSON Report: ./markdown_test_report.json"
    echo "  - Server Log: ./server_test.log"
    
    # List screenshots
    echo -e "\nScreenshots captured:"
    ls -la screenshots/*.png 2>/dev/null | awk '{print "  - " $9}'
    
    # Open HTML report
    if command -v xdg-open > /dev/null; then
        echo -e "\n${YELLOW}Opening HTML report in browser...${NC}"
        xdg-open markdown_test_report.html
    elif command -v open > /dev/null; then
        echo -e "\n${YELLOW}Opening HTML report in browser...${NC}"
        open markdown_test_report.html
    fi
else
    echo -e "\n${RED}==================================================================="
    echo -e "✗ E2E TEST FAILED"
    echo -e "===================================================================${NC}"
    echo -e "\nCheck the following for debugging:"
    echo "  - Server Log: ./server_test.log"
    echo "  - Screenshots: ./screenshots/"
    
    # Show server log tail
    echo -e "\n${YELLOW}Last 20 lines of server log:${NC}"
    tail -20 server_test.log
fi

echo -e "\n${YELLOW}Test complete!${NC}"
exit $TEST_EXIT_CODE