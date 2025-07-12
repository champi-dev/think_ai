#!/bin/bash

echo "Testing SSE streaming issue..."
echo "================================"

# Test 1: Send "hi" message
echo -e "\n1. Testing 'hi' message:"
echo "   Sending POST request to /api/chat/stream..."

# Send request and capture first 10 seconds of output
timeout 10 curl -N -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"message": "hi"}' \
  "http://localhost:8080/api/chat/stream" 2>/dev/null | tee /tmp/sse-hi.log

echo -e "\n   Response received. Checking for 'done' markers:"
grep -n "done" /tmp/sse-hi.log

# Test 2: Send "what is love" message
echo -e "\n\n2. Testing 'what is love' message:"
echo "   Sending POST request to /api/chat/stream..."

timeout 10 curl -N -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"message": "what is love"}' \
  "http://localhost:8080/api/chat/stream" 2>/dev/null | tee /tmp/sse-love.log

echo -e "\n   Response received. Checking for 'done' markers:"
grep -n "done" /tmp/sse-love.log

# Analysis
echo -e "\n\n3. Analysis:"
echo "   Counting total events in each response:"
echo "   'hi' events: $(grep -c "data:" /tmp/sse-hi.log)"
echo "   'what is love' events: $(grep -c "data:" /tmp/sse-love.log)"

echo -e "\n   Checking if streams properly close after done=true:"
echo "   Last 5 lines of 'hi' response:"
tail -5 /tmp/sse-hi.log

echo -e "\n   Last 5 lines of 'what is love' response:"
tail -5 /tmp/sse-love.log

echo -e "\n\nThe issue: If the stream continues sending data after done=true,"
echo "the frontend will keep reading indefinitely, causing a hang."