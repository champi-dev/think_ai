#!/bin/bash

echo "🧠 Manual Memory Test - Simple Verification"
echo "========================================="
echo ""

PROD_URL="https://thinkai.lat"
SESSION_ID="manual-test-$(date +%s)"

echo "Using session ID: $SESSION_ID"
echo ""

# Test 1: Send initial message
echo "1. Sending: 'My favorite color is blue and I love pizza'"
RESPONSE1=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"My favorite color is blue and I love pizza\",\"session_id\":\"$SESSION_ID\"}" | jq -r .response)

echo "Response: $(echo "$RESPONSE1" | head -100)..."
echo ""

sleep 2

# Test 2: Ask about color
echo "2. Sending: 'What is my favorite color?'"
RESPONSE2=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"What is my favorite color?\",\"session_id\":\"$SESSION_ID\"}" | jq -r .response)

echo "Response: $(echo "$RESPONSE2" | head -100)..."
echo ""

# Check if it remembered
if echo "$RESPONSE2" | grep -qi "blue"; then
    echo "✅ SUCCESS: System remembered the color 'blue'!"
else
    echo "❌ FAILED: System did not remember the color"
fi

sleep 2

# Test 3: Ask about food
echo ""
echo "3. Sending: 'What food do I love?'"
RESPONSE3=$(curl -s -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"What food do I love?\",\"session_id\":\"$SESSION_ID\"}" | jq -r .response)

echo "Response: $(echo "$RESPONSE3" | head -100)..."
echo ""

# Check if it remembered
if echo "$RESPONSE3" | grep -qi "pizza"; then
    echo "✅ SUCCESS: System remembered 'pizza'!"
else
    echo "❌ FAILED: System did not remember the food"
fi

echo ""
echo "🔍 Manual Browser Test:"
echo "1. Open https://thinkai.lat"
echo "2. Type: 'My name is John and I am 25 years old'"
echo "3. Type: 'What is my name?'"
echo "4. Expected: System should respond with 'John'"