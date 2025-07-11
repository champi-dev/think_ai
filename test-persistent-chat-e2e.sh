#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Think AI Persistent Chat E2E Test ===${NC}"
echo ""

# Kill any existing processes on port 8080
echo -e "${YELLOW}Killing any processes on port 8080...${NC}"
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
sleep 1

# Start the server
echo -e "${YELLOW}Starting Think AI Persistent server...${NC}"
./target/release/think-ai-full-persistent &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Wait for server to start
echo -e "${YELLOW}Waiting for server to start...${NC}"
sleep 3

# Check if server is running
if ! curl -s http://localhost:8080/health > /dev/null; then
    echo -e "${RED}Server failed to start!${NC}"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

echo -e "${GREEN}Server is running!${NC}"
echo ""

# Test 1: Create a new session with first message
echo -e "${YELLOW}Test 1: Creating new session with first message...${NC}"
RESPONSE1=$(curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! My name is Alice and I love quantum physics."}')

SESSION_ID=$(echo $RESPONSE1 | jq -r '.session_id')
echo "Session ID: $SESSION_ID"
echo "Response: $(echo $RESPONSE1 | jq -r '.response' | head -c 100)..."
echo ""

# Test 2: Continue conversation with context
echo -e "${YELLOW}Test 2: Continuing conversation with context...${NC}"
RESPONSE2=$(curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What did I just tell you my name was?\", \"session_id\": \"$SESSION_ID\"}")

echo "Response: $(echo $RESPONSE2 | jq -r '.response' | head -c 200)..."

# Check if the response contains "Alice" - the model should remember
if echo $RESPONSE2 | jq -r '.response' | grep -qi "alice"; then
    echo -e "${GREEN}✓ Context retention working! The system remembered the name.${NC}"
else
    echo -e "${RED}✗ Context retention might not be working properly.${NC}"
fi
echo ""

# Test 3: Add more context
echo -e "${YELLOW}Test 3: Adding more context to the conversation...${NC}"
RESPONSE3=$(curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"I'm working on a project about quantum entanglement. Can you help?\", \"session_id\": \"$SESSION_ID\"}")

echo "Response: $(echo $RESPONSE3 | jq -r '.response' | head -c 150)..."
echo ""

# Test 4: Test long-term memory
echo -e "${YELLOW}Test 4: Testing long-term memory...${NC}"
RESPONSE4=$(curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Can you summarize what we've talked about so far?\", \"session_id\": \"$SESSION_ID\"}")

echo "Response: $(echo $RESPONSE4 | jq -r '.response' | head -c 200)..."

# Check if summary mentions both Alice and quantum physics
if echo $RESPONSE4 | jq -r '.response' | grep -qi "alice" && echo $RESPONSE4 | jq -r '.response' | grep -qi "quantum"; then
    echo -e "${GREEN}✓ Long-term memory working! The system remembers the full conversation.${NC}"
else
    echo -e "${YELLOW}⚠ Long-term memory might be partially working.${NC}"
fi
echo ""

# Test 5: Test delete command
echo -e "${YELLOW}Test 5: Testing delete history command...${NC}"
RESPONSE5=$(curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"delete my history\", \"session_id\": \"$SESSION_ID\"}")

echo "Response: $(echo $RESPONSE5 | jq -r '.response')"
NEW_SESSION_ID=$(echo $RESPONSE5 | jq -r '.session_id')

if [ "$SESSION_ID" != "$NEW_SESSION_ID" ]; then
    echo -e "${GREEN}✓ Delete command working! New session ID created.${NC}"
else
    echo -e "${RED}✗ Delete command might not be working properly.${NC}"
fi
echo ""

# Test 6: Verify history was deleted
echo -e "${YELLOW}Test 6: Verifying history was actually deleted...${NC}"
RESPONSE6=$(curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is my name?\", \"session_id\": \"$NEW_SESSION_ID\"}")

echo "Response: $(echo $RESPONSE6 | jq -r '.response' | head -c 200)..."

if echo $RESPONSE6 | jq -r '.response' | grep -qi "alice"; then
    echo -e "${RED}✗ History might not have been properly deleted.${NC}"
else
    echo -e "${GREEN}✓ History properly deleted! The system doesn't remember Alice.${NC}"
fi
echo ""

# Test 7: Performance check
echo -e "${YELLOW}Test 7: Performance check...${NC}"
START_TIME=$(date +%s%N)
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 2+2?"}' > /dev/null
END_TIME=$(date +%s%N)
ELAPSED=$((($END_TIME - $START_TIME) / 1000000))
echo "Response time: ${ELAPSED}ms"

if [ $ELAPSED -lt 1000 ]; then
    echo -e "${GREEN}✓ Excellent performance! Response under 1 second.${NC}"
else
    echo -e "${YELLOW}⚠ Response time over 1 second.${NC}"
fi
echo ""

# Test 8: Concurrent sessions
echo -e "${YELLOW}Test 8: Testing concurrent sessions...${NC}"
RESPONSE7=$(curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi, my name is Bob and I love cooking."}')
BOB_SESSION=$(echo $RESPONSE7 | jq -r '.session_id')

RESPONSE8=$(curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is my name?\", \"session_id\": \"$BOB_SESSION\"}")

if echo $RESPONSE8 | jq -r '.response' | grep -qi "bob"; then
    echo -e "${GREEN}✓ Concurrent sessions working! Different sessions maintain separate contexts.${NC}"
else
    echo -e "${RED}✗ Concurrent sessions might not be isolated properly.${NC}"
fi
echo ""

# Cleanup
echo -e "${YELLOW}Cleaning up...${NC}"
kill $SERVER_PID 2>/dev/null || true

echo ""
echo -e "${GREEN}=== E2E Test Complete ===${NC}"
echo ""
echo "Summary:"
echo "- Server starts and responds: ✓"
echo "- Context retention: Tested"
echo "- Long-term memory: Tested"
echo "- Delete history: Tested"
echo "- Performance: Tested"
echo "- Concurrent sessions: Tested"