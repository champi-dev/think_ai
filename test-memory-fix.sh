#!/bin/bash

echo "🧠 Testing Memory Fix Locally"
echo "============================"
echo ""

# Kill any existing local test server
echo "Killing ports 5555 and 7777..."
kill -9 $(lsof -ti:5555) 2>/dev/null || true
kill -9 $(lsof -ti:7777) 2>/dev/null || true
sleep 2

# Start local server
echo "Starting local server on port 5555..."
./target/release/webapp-server --port 5555 > /tmp/local-test-server.log 2>&1 &
SERVER_PID=$!
sleep 3

LOCAL_URL="http://localhost:5555"
SESSION_ID="local-fix-test-$(date +%s)"

echo "Using session ID: $SESSION_ID"
echo ""

# Test 1: Send initial message
echo "1. Sending: 'My favorite animal is a cat and I am 30 years old'"
RESPONSE1=$(curl -s -X POST $LOCAL_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"My favorite animal is a cat and I am 30 years old\",\"session_id\":\"$SESSION_ID\"}" | jq -r .response)

echo "Response: $(echo "$RESPONSE1" | head -100)"
echo ""

sleep 2

# Test 2: Ask about animal
echo "2. Sending: 'What is my favorite animal?'"
RESPONSE2=$(curl -s -X POST $LOCAL_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"What is my favorite animal?\",\"session_id\":\"$SESSION_ID\"}" | jq -r .response)

echo "Response: $(echo "$RESPONSE2" | head -100)"
echo ""

# Check if it remembered
if echo "$RESPONSE2" | grep -qi "cat"; then
    echo "✅ SUCCESS: System remembered 'cat'!"
else
    echo "❌ FAILED: System did not remember the animal"
fi

sleep 2

# Test 3: Ask about age
echo ""
echo "3. Sending: 'How old am I?'"
RESPONSE3=$(curl -s -X POST $LOCAL_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"How old am I?\",\"session_id\":\"$SESSION_ID\"}" | jq -r .response)

echo "Response: $(echo "$RESPONSE3" | head -100)"
echo ""

# Check if it remembered
if echo "$RESPONSE3" | grep -qi "30"; then
    echo "✅ SUCCESS: System remembered age '30'!"
else
    echo "❌ FAILED: System did not remember the age"
fi

# Check server logs for the bug
echo ""
echo "🔍 Checking server logs for context format..."
grep -A5 -B5 "Previous conversation" /tmp/local-test-server.log | tail -20 || true

# Clean up
echo ""
echo "Cleaning up..."
kill $SERVER_PID 2>/dev/null || true

echo ""
echo "Test complete!"