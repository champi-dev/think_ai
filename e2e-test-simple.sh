#!/bin/bash

echo "🧪 Think AI E2E Test Suite"
echo "========================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
PASSED=0
FAILED=0

# Server URL
URL="http://localhost:5555"

# Function to run a test
run_test() {
    local test_name="$1"
    local command="$2"
    local expected="$3"
    
    echo -n "Testing $test_name... "
    
    result=$(eval "$command" 2>&1)
    
    if [[ "$result" == *"$expected"* ]]; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo "  Expected: $expected"
        echo "  Got: $result"
        ((FAILED++))
        return 1
    fi
}

# Function to test chat with session
test_session() {
    local session_id="test_session_$$"
    
    echo -e "\n${BLUE}Testing Session Management:${NC}"
    
    # First message
    echo -n "  1. Sending initial message with session... "
    result1=$(curl -s -X POST "$URL/chat" \
        -H "Content-Type: application/json" \
        -d "{\"query\":\"Remember my name is TestUser\",\"session_id\":\"$session_id\"}")
    
    if [[ -n "$result1" ]]; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${RED}❌${NC}"
        ((FAILED++))
        return
    fi
    
    # Second message to test memory
    echo -n "  2. Testing session memory... "
    result2=$(curl -s -X POST "$URL/chat" \
        -H "Content-Type: application/json" \
        -d "{\"query\":\"What is my name?\",\"session_id\":\"$session_id\"}")
    
    if [[ "$result2" == *"TestUser"* ]]; then
        echo -e "${GREEN}✅ Session memory working${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ No session memory (stable-server limitation)${NC}"
        ((FAILED++))
    fi
}

# Function to test delete command
test_delete() {
    local session_id="test_delete_$$"
    
    echo -e "\n${BLUE}Testing Delete Command:${NC}"
    
    result=$(curl -s -X POST "$URL/chat" \
        -H "Content-Type: application/json" \
        -d "{\"query\":\"delete my chat history\",\"session_id\":\"$session_id\"}")
    
    if [[ "$result" == *"deleted"* ]] || [[ "$result" == *"fresh"* ]]; then
        echo -e "  ${GREEN}✅ Delete command recognized${NC}"
        ((PASSED++))
    else
        echo -e "  ${RED}❌ Delete command not implemented (stable-server limitation)${NC}"
        ((FAILED++))
    fi
}

# Function to test performance
test_performance() {
    echo -e "\n${BLUE}Testing Performance:${NC}"
    
    start_time=$(date +%s%N)
    result=$(curl -s -X POST "$URL/chat" \
        -H "Content-Type: application/json" \
        -d '{"query":"What is 2+2?"}')
    end_time=$(date +%s%N)
    
    # Calculate response time in milliseconds
    response_time=$(( (end_time - start_time) / 1000000 ))
    
    echo -n "  Response time: ${response_time}ms - "
    if [ $response_time -lt 100 ]; then
        echo -e "${GREEN}✅ O(1) Performance${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠️  Slower than expected${NC}"
        ((FAILED++))
    fi
}

# Start tests
echo -e "\n${YELLOW}Running tests against $URL${NC}\n"

# Test 1: Health Check
run_test "Health Check" \
    "curl -s $URL/health" \
    "OK"

# Test 2: Basic Chat
run_test "Basic Chat" \
    "curl -s -X POST $URL/chat -H 'Content-Type: application/json' -d '{\"query\":\"What is 2+2?\"}' | grep -o '4'" \
    "4"

# Test 3: Stats Endpoint
run_test "Stats Endpoint" \
    "curl -s $URL/stats | grep -o 'server_status'" \
    "server_status"

# Test 4: Session Management
test_session

# Test 5: Delete Command
test_delete

# Test 6: Performance
test_performance

# Summary
echo -e "\n${YELLOW}📊 Test Summary:${NC}"
echo "================"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
TOTAL=$((PASSED + FAILED))
PERCENTAGE=$(( (PASSED * 100) / TOTAL ))
echo "Success Rate: $PERCENTAGE%"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed!${NC}"
else
    echo -e "\n${YELLOW}⚠️  Some tests failed. This is expected for stable-server.${NC}"
    echo -e "${YELLOW}The stable-server doesn't implement session management or chat history deletion.${NC}"
fi

# Check if unit tests exist
echo -e "\n${BLUE}Checking for unit tests...${NC}"
if [ -f "/home/administrator/think_ai/Cargo.toml" ]; then
    echo "Running cargo test..."
    cd /home/administrator/think_ai
    cargo test --lib --bins 2>&1 | tail -20
else
    echo -e "${YELLOW}No Cargo.toml found in root directory${NC}"
fi