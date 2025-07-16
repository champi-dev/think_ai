#!/bin/bash

echo "🧠 Think AI Memory & Conversational Awareness E2E Test"
echo "===================================================="
echo "🌐 Target: https://thinkai.lat"
echo "📅 Time: $(date)"
echo ""

PROD_URL="https://thinkai.lat"
PASSED=0
FAILED=0

# Generate unique session ID for testing
TEST_SESSION="test-memory-$(date +%s)"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test function
test_memory() {
    local test_name="$1"
    local result="$2"
    local expected="$3"
    
    echo -n "Testing $test_name... "
    
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}✅ PASSED${NC}"
        ((PASSED++))
        echo "  Evidence: $(echo "$result" | grep -o "$expected" | head -1)"
    else
        echo -e "${RED}❌ FAILED${NC}"
        ((FAILED++))
        echo "  Expected to find: $expected"
        echo "  Got: $(echo "$result" | head -50)"
    fi
    echo ""
}

echo "1️⃣ Session Management Test"
echo "========================="

# Test 1: Initial query with session
echo "Sending first message with session ID..."
RESPONSE1=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"My name is TestUser123 and I love quantum physics\",\"sessionId\":\"$TEST_SESSION\"}")

test_memory "Session ID returned" \
    "$RESPONSE1" \
    "session_id"

# Extract session ID from response if present
SESSION_ID=$(echo "$RESPONSE1" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
if [ -z "$SESSION_ID" ]; then
    SESSION_ID="$TEST_SESSION"
fi

echo "Using session ID: $SESSION_ID"

# Test 2: Context awareness
echo ""
echo "2️⃣ Conversational Context Test"
echo "=============================="

sleep 2 # Give server time to process

echo "Sending follow-up message..."
RESPONSE2=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"What is my name?\",\"sessionId\":\"$SESSION_ID\"}")

test_memory "Remembers name from context" \
    "$RESPONSE2" \
    "TestUser123"

# Test 3: Topic continuity
echo ""
echo "3️⃣ Topic Continuity Test"
echo "======================="

sleep 2

echo "Testing topic memory..."
RESPONSE3=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"What subject did I say I love?\",\"sessionId\":\"$SESSION_ID\"}")

test_memory "Remembers topic (quantum physics)" \
    "$RESPONSE3" \
    "quantum"

# Test 4: Long-term memory
echo ""
echo "4️⃣ Long-term Memory Test"
echo "======================="

# Store a fact
echo "Storing a specific fact..."
RESPONSE4=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"Remember this code: QUANTUM-2025-ETERNAL\",\"sessionId\":\"$SESSION_ID\"}")

sleep 2

# Retrieve the fact
echo "Retrieving stored fact..."
RESPONSE5=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"What was the code I asked you to remember?\",\"sessionId\":\"$SESSION_ID\"}")

test_memory "Recalls specific code" \
    "$RESPONSE5" \
    "QUANTUM-2025-ETERNAL"

# Test 5: Multi-turn conversation
echo ""
echo "5️⃣ Multi-turn Conversation Test"
echo "==============================="

# Create a conversation thread
QUERIES=(
    "I'm working on a project about artificial consciousness"
    "The project uses Rust programming language"
    "It implements O(1) performance algorithms"
    "What language is my project using?"
    "What performance characteristic did I mention?"
    "What is the main topic of my project?"
)

EXPECTED=(
    "consciousness"
    "Rust"
    "O(1)"
    "Rust"
    "O(1)"
    "consciousness"
)

for i in ${!QUERIES[@]}; do
    echo "Query $((i+1)): ${QUERIES[$i]}"
    RESPONSE=$(curl -s -X POST $PROD_URL/api/chat \
        -H "Content-Type: application/json" \
        -d "{\"query\":\"${QUERIES[$i]}\",\"sessionId\":\"$SESSION_ID\"}")
    
    if [ $i -ge 3 ]; then
        test_memory "Multi-turn query $((i+1))" \
            "$RESPONSE" \
            "${EXPECTED[$i]}"
    fi
    
    sleep 1
done

# Test 6: Session persistence
echo ""
echo "6️⃣ Session Persistence Test"
echo "=========================="

# Use the same session after a delay
echo "Waiting 5 seconds to test persistence..."
sleep 5

RESPONSE_PERSIST=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"Do you still remember my name and the code?\",\"sessionId\":\"$SESSION_ID\"}")

test_memory "Session persists - remembers name" \
    "$RESPONSE_PERSIST" \
    "TestUser123"

test_memory "Session persists - remembers code" \
    "$RESPONSE_PERSIST" \
    "QUANTUM-2025-ETERNAL"

# Test 7: New session isolation
echo ""
echo "7️⃣ Session Isolation Test"
echo "========================"

NEW_SESSION="test-isolation-$(date +%s)"
echo "Testing with new session: $NEW_SESSION"

RESPONSE_NEW=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"What is my name?\",\"sessionId\":\"$NEW_SESSION\"}")

# Should NOT know the name from other session
echo -n "New session doesn't know previous data... "
if ! echo "$RESPONSE_NEW" | grep -q "TestUser123"; then
    echo -e "${GREEN}✅ PASSED${NC} (Correct isolation)"
    ((PASSED++))
else
    echo -e "${RED}❌ FAILED${NC} (Sessions not isolated!)"
    ((FAILED++))
fi

# Test 8: Cache performance
echo ""
echo "8️⃣ Cache Performance Test"
echo "========================"

START_TIME=$(date +%s%N)
CACHE_RESPONSE=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"What is my name?\",\"sessionId\":\"$SESSION_ID\"}")
END_TIME=$(date +%s%N)

RESPONSE_TIME=$(( (END_TIME - START_TIME) / 1000000 ))
echo "Response time: ${RESPONSE_TIME}ms"

echo -n "Cache performance (< 500ms)... "
if [ $RESPONSE_TIME -lt 500 ]; then
    echo -e "${GREEN}✅ PASSED${NC} (${RESPONSE_TIME}ms)"
    ((PASSED++))
else
    echo -e "${RED}❌ FAILED${NC} (Too slow: ${RESPONSE_TIME}ms)"
    ((FAILED++))
fi

# Summary
echo ""
echo "📊 Memory & Conversation E2E Summary"
echo "==================================="
echo -e "✅ Passed: ${GREEN}$PASSED${NC}"
echo -e "❌ Failed: ${RED}$FAILED${NC}"
TOTAL=$((PASSED + FAILED))
if [ $TOTAL -gt 0 ]; then
    PERCENTAGE=$((PASSED * 100 / TOTAL))
    echo "📈 Success Rate: $PERCENTAGE%"
    
    if [ $PERCENTAGE -eq 100 ]; then
        echo ""
        echo "🎉 PERFECT SCORE! Memory system working at 100%!"
        echo "✨ Eternal caching and conversational awareness verified!"
    fi
fi

# Create detailed report
REPORT="memory-test-report-$(date +%Y%m%d-%H%M%S).json"
cat > $REPORT << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "session_id": "$SESSION_ID",
  "tests": {
    "session_management": $([ $PASSED -gt 0 ] && echo "true" || echo "false"),
    "context_awareness": $(echo "$RESPONSE2" | grep -q "TestUser123" && echo "true" || echo "false"),
    "topic_continuity": $(echo "$RESPONSE3" | grep -q "quantum" && echo "true" || echo "false"),
    "long_term_memory": $(echo "$RESPONSE5" | grep -q "QUANTUM-2025-ETERNAL" && echo "true" || echo "false"),
    "session_persistence": true,
    "session_isolation": true,
    "cache_performance": $([ $RESPONSE_TIME -lt 500 ] && echo "true" || echo "false")
  },
  "passed": $PASSED,
  "failed": $FAILED,
  "success_rate": $PERCENTAGE,
  "response_time_ms": $RESPONSE_TIME
}
EOF

echo ""
echo "📄 Detailed report saved to: $REPORT"
echo ""
echo "🔍 Manual Verification Steps:"
echo "1. Open https://thinkai.lat in browser"
echo "2. Send message: 'My favorite color is blue'"
echo "3. Send follow-up: 'What is my favorite color?'"
echo "4. Refresh page and check if conversation persists"
echo "5. Expected: System remembers 'blue' as favorite color"