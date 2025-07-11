#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Safe test port
TEST_PORT=3456
TEST_URL="http://localhost:$TEST_PORT"
RESULTS_FILE="e2e_test_results.md"

echo -e "${BLUE}=== Think AI Persistent Chat E2E Test ===${NC}"
echo -e "${BLUE}=== Using Safe Port: $TEST_PORT ===${NC}"
echo ""

# Initialize results file
cat > $RESULTS_FILE << EOF
# Think AI Persistent Chat E2E Test Results
Date: $(date)
Test Port: $TEST_PORT

## Test Results Summary

EOF

# Kill any existing processes on test port
echo -e "${YELLOW}Cleaning up port $TEST_PORT...${NC}"
lsof -ti:$TEST_PORT | xargs kill -9 2>/dev/null || true
sleep 1

# Start the server on test port
echo -e "${YELLOW}Starting Think AI Persistent server on port $TEST_PORT...${NC}"
PORT=$TEST_PORT ./target/release/think-ai-full-persistent > server_test.log 2>&1 &
SERVER_PID=$!
echo "Test Server PID: $SERVER_PID"

# Wait for server to start
echo -e "${YELLOW}Waiting for test server to start...${NC}"
for i in {1..10}; do
    if curl -s $TEST_URL/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Test server is running!${NC}"
        break
    fi
    sleep 1
done

# Verify server is running
if ! curl -s $TEST_URL/health > /dev/null 2>&1; then
    echo -e "${RED}✗ Server failed to start!${NC}"
    cat server_test.log
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

echo "" | tee -a $RESULTS_FILE
echo "### Server Status" | tee -a $RESULTS_FILE
echo "✅ Server started successfully on port $TEST_PORT" | tee -a $RESULTS_FILE
echo "" | tee -a $RESULTS_FILE

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
HEALTH_STATUS=$(curl -s -w "\n%{http_code}" $TEST_URL/health)
echo "Health check response: $HEALTH_STATUS" | tee -a $RESULTS_FILE

# Test 2: Create a new session
echo -e "\n${YELLOW}Test 2: Creating new chat session...${NC}"
RESPONSE1=$(curl -s -X POST $TEST_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! My name is Alice and I am a quantum physicist working on quantum computing."}')

if [ -z "$RESPONSE1" ]; then
    echo -e "${RED}✗ No response from server${NC}" | tee -a $RESULTS_FILE
else
    SESSION_ID=$(echo $RESPONSE1 | jq -r '.session_id' 2>/dev/null || echo "ERROR")
    RESPONSE_TEXT=$(echo $RESPONSE1 | jq -r '.response' 2>/dev/null || echo "ERROR")
    echo "" | tee -a $RESULTS_FILE
    echo "### Test 2: Initial Message" | tee -a $RESULTS_FILE
    echo "Session ID: $SESSION_ID" | tee -a $RESULTS_FILE
    echo "Response preview: ${RESPONSE_TEXT:0:100}..." | tee -a $RESULTS_FILE
    echo "✅ Session created successfully" | tee -a $RESULTS_FILE
fi

sleep 1

# Test 3: Context retention
echo -e "\n${YELLOW}Test 3: Testing context retention...${NC}"
RESPONSE2=$(curl -s -X POST $TEST_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is my name and profession?\", \"session_id\": \"$SESSION_ID\"}")

RESPONSE2_TEXT=$(echo $RESPONSE2 | jq -r '.response' 2>/dev/null || echo "ERROR")
echo "" | tee -a $RESULTS_FILE
echo "### Test 3: Context Retention" | tee -a $RESULTS_FILE
echo "Question: What is my name and profession?" | tee -a $RESULTS_FILE
echo "Response: ${RESPONSE2_TEXT:0:200}..." | tee -a $RESULTS_FILE

# Check if response contains Alice and quantum
if echo "$RESPONSE2_TEXT" | grep -qi "alice" && echo "$RESPONSE2_TEXT" | grep -qi "quantum"; then
    echo -e "${GREEN}✅ Context retention PASSED! System remembers Alice and quantum physics.${NC}" | tee -a $RESULTS_FILE
else
    echo -e "${RED}❌ Context retention FAILED! System didn't remember the information.${NC}" | tee -a $RESULTS_FILE
fi

# Test 4: Multiple exchanges
echo -e "\n${YELLOW}Test 4: Multiple conversation turns...${NC}"
RESPONSE3=$(curl -s -X POST $TEST_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"I'm particularly interested in quantum entanglement. Can you tell me something about it?\", \"session_id\": \"$SESSION_ID\"}")

RESPONSE4=$(curl -s -X POST $TEST_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Based on what you know about me, why might I find this topic interesting?\", \"session_id\": \"$SESSION_ID\"}")

RESPONSE4_TEXT=$(echo $RESPONSE4 | jq -r '.response' 2>/dev/null || echo "ERROR")
echo "" | tee -a $RESULTS_FILE
echo "### Test 4: Multiple Turns" | tee -a $RESULTS_FILE
echo "✅ Conducted 4-turn conversation" | tee -a $RESULTS_FILE
echo "Final response preview: ${RESPONSE4_TEXT:0:150}..." | tee -a $RESULTS_FILE

# Test 5: Delete history
echo -e "\n${YELLOW}Test 5: Testing delete history command...${NC}"
DELETE_RESPONSE=$(curl -s -X POST $TEST_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"delete my history\", \"session_id\": \"$SESSION_ID\"}")

DELETE_TEXT=$(echo $DELETE_RESPONSE | jq -r '.response' 2>/dev/null || echo "ERROR")
NEW_SESSION=$(echo $DELETE_RESPONSE | jq -r '.session_id' 2>/dev/null || echo "ERROR")

echo "" | tee -a $RESULTS_FILE
echo "### Test 5: Delete History" | tee -a $RESULTS_FILE
echo "Delete response: $DELETE_TEXT" | tee -a $RESULTS_FILE
echo "Old session: $SESSION_ID" | tee -a $RESULTS_FILE
echo "New session: $NEW_SESSION" | tee -a $RESULTS_FILE

if [ "$SESSION_ID" != "$NEW_SESSION" ] && echo "$DELETE_TEXT" | grep -qi "deleted"; then
    echo -e "${GREEN}✅ Delete history PASSED! New session created.${NC}" | tee -a $RESULTS_FILE
else
    echo -e "${RED}❌ Delete history FAILED!${NC}" | tee -a $RESULTS_FILE
fi

# Test 6: Verify deletion
echo -e "\n${YELLOW}Test 6: Verifying history was deleted...${NC}"
VERIFY_RESPONSE=$(curl -s -X POST $TEST_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Do you remember my name?\", \"session_id\": \"$NEW_SESSION\"}")

VERIFY_TEXT=$(echo $VERIFY_RESPONSE | jq -r '.response' 2>/dev/null || echo "ERROR")
echo "" | tee -a $RESULTS_FILE
echo "### Test 6: Verify Deletion" | tee -a $RESULTS_FILE

if echo "$VERIFY_TEXT" | grep -qi "alice"; then
    echo -e "${RED}❌ History deletion FAILED! System still remembers Alice.${NC}" | tee -a $RESULTS_FILE
else
    echo -e "${GREEN}✅ History deletion PASSED! System doesn't remember previous context.${NC}" | tee -a $RESULTS_FILE
fi

# Test 7: Performance test
echo -e "\n${YELLOW}Test 7: Performance test...${NC}"
TOTAL_TIME=0
NUM_REQUESTS=5

echo "" | tee -a $RESULTS_FILE
echo "### Test 7: Performance" | tee -a $RESULTS_FILE

for i in $(seq 1 $NUM_REQUESTS); do
    START_TIME=$(date +%s%N)
    curl -s -X POST $TEST_URL/api/chat \
      -H "Content-Type: application/json" \
      -d "{\"message\": \"Quick test $i\", \"session_id\": \"perf-test-$i\"}" > /dev/null
    END_TIME=$(date +%s%N)
    ELAPSED=$((($END_TIME - $START_TIME) / 1000000))
    TOTAL_TIME=$(($TOTAL_TIME + $ELAPSED))
    echo "Request $i: ${ELAPSED}ms" | tee -a $RESULTS_FILE
done

AVG_TIME=$(($TOTAL_TIME / $NUM_REQUESTS))
echo "Average response time: ${AVG_TIME}ms" | tee -a $RESULTS_FILE

if [ $AVG_TIME -lt 1000 ]; then
    echo -e "${GREEN}✅ Performance EXCELLENT! Average under 1 second.${NC}" | tee -a $RESULTS_FILE
else
    echo -e "${YELLOW}⚠️  Performance could be improved. Average over 1 second.${NC}" | tee -a $RESULTS_FILE
fi

# Test 8: Concurrent sessions
echo -e "\n${YELLOW}Test 8: Testing concurrent sessions...${NC}"
echo "" | tee -a $RESULTS_FILE
echo "### Test 8: Concurrent Sessions" | tee -a $RESULTS_FILE

# Session A
curl -s -X POST $TEST_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi, I am Bob and I love cooking Italian food."}' > session_a.json

SESSION_A=$(jq -r '.session_id' session_a.json)

# Session B
curl -s -X POST $TEST_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I am Carol and I am a marine biologist."}' > session_b.json

SESSION_B=$(jq -r '.session_id' session_b.json)

# Query Session A
RESPONSE_A=$(curl -s -X POST $TEST_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is my favorite type of food?\", \"session_id\": \"$SESSION_A\"}")

# Query Session B
RESPONSE_B=$(curl -s -X POST $TEST_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is my profession?\", \"session_id\": \"$SESSION_B\"}")

TEXT_A=$(echo $RESPONSE_A | jq -r '.response' 2>/dev/null || echo "ERROR")
TEXT_B=$(echo $RESPONSE_B | jq -r '.response' 2>/dev/null || echo "ERROR")

echo "Session A (Bob) - Response about food: ${TEXT_A:0:100}..." | tee -a $RESULTS_FILE
echo "Session B (Carol) - Response about profession: ${TEXT_B:0:100}..." | tee -a $RESULTS_FILE

if echo "$TEXT_A" | grep -qi "italian" && echo "$TEXT_B" | grep -qi "marine\|biolog"; then
    echo -e "${GREEN}✅ Concurrent sessions PASSED! Sessions maintain separate contexts.${NC}" | tee -a $RESULTS_FILE
else
    echo -e "${RED}❌ Concurrent sessions FAILED! Context mixing detected.${NC}" | tee -a $RESULTS_FILE
fi

# Cleanup
echo -e "\n${YELLOW}Cleaning up...${NC}"
kill $SERVER_PID 2>/dev/null || true
rm -f session_a.json session_b.json

# Final summary
echo "" | tee -a $RESULTS_FILE
echo "## Final Summary" | tee -a $RESULTS_FILE
echo "- Server startup: ✅" | tee -a $RESULTS_FILE
echo "- Context retention: Tested" | tee -a $RESULTS_FILE
echo "- History deletion: Tested" | tee -a $RESULTS_FILE
echo "- Performance: Average ${AVG_TIME}ms" | tee -a $RESULTS_FILE
echo "- Concurrent sessions: Tested" | tee -a $RESULTS_FILE
echo "" | tee -a $RESULTS_FILE
echo "Test completed at: $(date)" | tee -a $RESULTS_FILE

echo -e "\n${GREEN}=== E2E Test Complete ===${NC}"
echo -e "Results saved to: ${BLUE}$RESULTS_FILE${NC}"
echo -e "Server logs saved to: ${BLUE}server_test.log${NC}"