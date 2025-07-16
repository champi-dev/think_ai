#!/bin/bash

echo "🧠 Testing Conversational Memory in Production"
echo "============================================="
echo ""

PROD_URL="https://thinkai.lat"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SESSION_ID="memory-test-$TIMESTAMP"

# Test 1: Basic memory test (exact scenario from user)
echo "Test 1: Name Memory Test"
echo "-----------------------"

# Step 1: Tell the AI your name
echo "1. Sending: 'mi nombre es daniel'"
RESPONSE1=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"mi nombre es daniel\",\"session_id\":\"$SESSION_ID\"}" | jq -r .response)

echo "Response preview: $(echo "$RESPONSE1" | head -100)..."
echo ""

sleep 2

# Step 2: Ask what your name is
echo "2. Sending: 'cual es mi nombre'"
RESPONSE2=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"cual es mi nombre\",\"session_id\":\"$SESSION_ID\"}" | jq -r .response)

echo "Response: $(echo "$RESPONSE2" | head -200)"
echo ""

# Check if it remembered
if echo "$RESPONSE2" | grep -qi "daniel"; then
    echo "✅ Test 1 PASSED: AI remembered the name 'Daniel'"
    TEST1_PASS=true
else
    echo "❌ Test 1 FAILED: AI did not remember the name"
    TEST1_PASS=false
fi

echo ""
echo "Test 2: Multiple Facts Memory"
echo "----------------------------"

SESSION_ID2="memory-test2-$TIMESTAMP"

# Send multiple facts
echo "1. Sending: 'I am 25 years old and I live in Madrid'"
curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"I am 25 years old and I live in Madrid\",\"session_id\":\"$SESSION_ID2\"}" > /dev/null

sleep 1

echo "2. Sending: 'My favorite color is blue'"
curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"My favorite color is blue\",\"session_id\":\"$SESSION_ID2\"}" > /dev/null

sleep 1

echo "3. Sending: 'I work as a software engineer'"
curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"I work as a software engineer\",\"session_id\":\"$SESSION_ID2\"}" > /dev/null

sleep 2

# Test memory of all facts
echo "4. Asking: 'Tell me what you know about me'"
RESPONSE3=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"Tell me what you know about me\",\"session_id\":\"$SESSION_ID2\"}" | jq -r .response)

echo "Response: $(echo "$RESPONSE3" | head -200)"
echo ""

# Check if it remembered all facts
FACTS_REMEMBERED=0
echo "$RESPONSE3" | grep -qi "25" && FACTS_REMEMBERED=$((FACTS_REMEMBERED + 1))
echo "$RESPONSE3" | grep -qi "madrid" && FACTS_REMEMBERED=$((FACTS_REMEMBERED + 1))
echo "$RESPONSE3" | grep -qi "blue" && FACTS_REMEMBERED=$((FACTS_REMEMBERED + 1))
echo "$RESPONSE3" | grep -qi "engineer" && FACTS_REMEMBERED=$((FACTS_REMEMBERED + 1))

if [ $FACTS_REMEMBERED -ge 3 ]; then
    echo "✅ Test 2 PASSED: AI remembered $FACTS_REMEMBERED/4 facts"
    TEST2_PASS=true
else
    echo "❌ Test 2 FAILED: AI only remembered $FACTS_REMEMBERED/4 facts"
    TEST2_PASS=false
fi

echo ""
echo "Test 3: Context Persistence Across Messages"
echo "-----------------------------------------"

SESSION_ID3="memory-test3-$TIMESTAMP"

# Have a conversation
echo "1. Sending: 'Let's talk about Python programming'"
curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"Let's talk about Python programming\",\"session_id\":\"$SESSION_ID3\"}" > /dev/null

sleep 1

echo "2. Sending: 'I prefer using type hints'"
curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"I prefer using type hints\",\"session_id\":\"$SESSION_ID3\"}" > /dev/null

sleep 1

echo "3. Asking: 'What programming language were we discussing?'"
RESPONSE4=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"What programming language were we discussing?\",\"session_id\":\"$SESSION_ID3\"}" | jq -r .response)

echo "Response: $(echo "$RESPONSE4" | head -100)"
echo ""

if echo "$RESPONSE4" | grep -qi "python"; then
    echo "✅ Test 3 PASSED: AI remembered the conversation topic"
    TEST3_PASS=true
else
    echo "❌ Test 3 FAILED: AI forgot the conversation topic"
    TEST3_PASS=false
fi

# Generate report
echo ""
echo "============================================="
echo "📊 MEMORY TEST RESULTS:"
echo ""

TOTAL_TESTS=3
PASSED_TESTS=0
[ "$TEST1_PASS" = true ] && PASSED_TESTS=$((PASSED_TESTS + 1))
[ "$TEST2_PASS" = true ] && PASSED_TESTS=$((PASSED_TESTS + 1))
[ "$TEST3_PASS" = true ] && PASSED_TESTS=$((PASSED_TESTS + 1))

echo "Total Tests: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS"
echo "Failed: $((TOTAL_TESTS - PASSED_TESTS))"
echo "Success Rate: $(echo "scale=2; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc)%"

# Create JSON report
REPORT_FILE="memory-test-report-$TIMESTAMP.json"
cat > $REPORT_FILE <<EOF
{
  "timestamp": "$TIMESTAMP",
  "url": "$PROD_URL",
  "tests": [
    {
      "name": "Name Memory Test",
      "description": "User tells name, then asks what their name is",
      "passed": $TEST1_PASS,
      "critical": true
    },
    {
      "name": "Multiple Facts Memory",
      "description": "Remember multiple facts about user",
      "passed": $TEST2_PASS,
      "facts_remembered": $FACTS_REMEMBERED
    },
    {
      "name": "Context Persistence",
      "description": "Remember conversation topic across messages",
      "passed": $TEST3_PASS
    }
  ],
  "summary": {
    "total": $TOTAL_TESTS,
    "passed": $PASSED_TESTS,
    "failed": $((TOTAL_TESTS - PASSED_TESTS)),
    "success_rate": "$(echo "scale=2; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc)%"
  }
}
EOF

echo ""
echo "Report saved to: $REPORT_FILE"

if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
    echo ""
    echo "🎉 ALL MEMORY TESTS PASSED! (100% Success Rate)"
else
    echo ""
    echo "⚠️  Memory feature needs fixing. Success rate: $(echo "scale=2; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc)%"
fi