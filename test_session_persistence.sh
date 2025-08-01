#!/bin/bash

# Test session persistence

SESSION_ID="test-session-$(date +%s)"
BASE_URL="http://localhost:7777"

echo "Testing session persistence with session ID: $SESSION_ID"
echo "==========================================="

# Message 1: Introduction
echo -e "\n1. Sending introduction..."
RESPONSE1=$(curl -s -X POST "$BASE_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"Hello! My name is Alice and I love programming in Python.\",
    \"session_id\": \"$SESSION_ID\"
  }" | jq -r '.response')

echo "Response: $RESPONSE1"

# Wait a bit
sleep 2

# Message 2: Ask about remembered info
echo -e "\n2. Testing memory - asking about name..."
RESPONSE2=$(curl -s -X POST "$BASE_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"What's my name?\",
    \"session_id\": \"$SESSION_ID\"
  }" | jq -r '.response')

echo "Response: $RESPONSE2"

# Check if Alice is mentioned
if echo "$RESPONSE2" | grep -i "alice" > /dev/null; then
  echo "✅ SUCCESS: The AI remembered the name 'Alice'"
else
  echo "❌ FAILED: The AI did not remember the name 'Alice'"
fi

# Wait a bit
sleep 2

# Message 3: Ask about programming language
echo -e "\n3. Testing memory - asking about programming language..."
RESPONSE3=$(curl -s -X POST "$BASE_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"What programming language do I like?\",
    \"session_id\": \"$SESSION_ID\"
  }" | jq -r '.response')

echo "Response: $RESPONSE3"

# Check if Python is mentioned
if echo "$RESPONSE3" | grep -i "python" > /dev/null; then
  echo "✅ SUCCESS: The AI remembered 'Python'"
else
  echo "❌ FAILED: The AI did not remember 'Python'"
fi

# Check session history
echo -e "\n4. Checking session history..."
HISTORY=$(curl -s -X GET "$BASE_URL/api/chat/sessions/$SESSION_ID" | jq '.')

if [ -n "$HISTORY" ] && [ "$HISTORY" != "null" ]; then
  echo "✅ Session history retrieved:"
  echo "$HISTORY" | jq -r '.[] | "User: \(.[0])\nAssistant: \(.[1])\n"'
else
  echo "❌ No session history found"
fi

echo -e "\n==========================================="
echo "Session persistence test complete"