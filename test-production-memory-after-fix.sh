#!/bin/bash

echo "🧠 Testing Memory After Fix in Production"
echo "========================================"
echo ""

PROD_URL="https://thinkai.lat"
SESSION_ID="fix-test-$(date +%s)"

echo "Using session ID: $SESSION_ID"
echo ""

# Test 1: Send initial message
echo "1. Sending: 'My name is Alice and I work at Google'"
RESPONSE1=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"My name is Alice and I work at Google\",\"session_id\":\"$SESSION_ID\"}" | jq -r .response)

echo "Response preview: $(echo "$RESPONSE1" | head -50)..."
echo ""

sleep 2

# Test 2: Ask about name
echo "2. Sending: 'What is my name?'"
RESPONSE2=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"What is my name?\",\"session_id\":\"$SESSION_ID\"}" | jq -r .response)

echo "Response: $(echo "$RESPONSE2" | head -100)"
echo ""

# Check if it remembered
if echo "$RESPONSE2" | grep -qi "alice"; then
    echo "✅ SUCCESS: System remembered 'Alice'!"
    MEMORY_WORKS=true
else
    echo "❌ FAILED: System did not remember the name"
    MEMORY_WORKS=false
fi

sleep 2

# Test 3: Ask about workplace
echo ""
echo "3. Sending: 'Where do I work?'"
RESPONSE3=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"Where do I work?\",\"session_id\":\"$SESSION_ID\"}" | jq -r .response)

echo "Response: $(echo "$RESPONSE3" | head -100)"
echo ""

# Check if it remembered
if echo "$RESPONSE3" | grep -qi "google"; then
    echo "✅ SUCCESS: System remembered 'Google'!"
else
    echo "❌ FAILED: System did not remember the workplace"
    MEMORY_WORKS=false
fi

echo ""
echo "========================================"
if [ "$MEMORY_WORKS" = true ]; then
    echo "🎉 MEMORY IS WORKING! The fix was successful!"
else
    echo "⚠️  Memory still not working as expected"
fi