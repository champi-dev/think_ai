#!/bin/bash

echo "Testing Think AI Streaming vs Non-Streaming Formatting"
echo "======================================================="
echo ""

# Kill any existing server on 3456
kill -9 $(lsof -t -i:3456) 2>/dev/null
sleep 1

# Start test server
echo "Starting test server on port 3456..."
PORT=3456 ./target/release/think-ai-full server > test_server.log 2>&1 &
SERVER_PID=$!
sleep 3

# Test non-streaming mode
echo "1. Testing NON-STREAMING mode..."
curl -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a short markdown example with **bold**, *italic*, `code`, and a list:\n1. First item\n2. Second item",
    "session_id": "test_formatting_1",
    "streaming": false
  }' | jq -r '.response' > non_streaming_response.txt

echo "Non-streaming response saved to non_streaming_response.txt"
echo ""

# Test streaming mode
echo "2. Testing STREAMING mode..."
# Using curl with event-stream to capture the full streaming response
curl -N -X POST http://localhost:3456/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a short markdown example with **bold**, *italic*, `code`, and a list:\n1. First item\n2. Second item",
    "session_id": "test_formatting_2"
  }' > streaming_response_raw.txt 2>/dev/null &

CURL_PID=$!
sleep 5
kill $CURL_PID 2>/dev/null

echo "Streaming response saved to streaming_response_raw.txt"
echo ""

# Kill test server
kill $SERVER_PID 2>/dev/null

echo "Test complete! Compare the outputs:"
echo "- non_streaming_response.txt"
echo "- streaming_response_raw.txt"
echo ""
echo "To see the formatted results in a browser:"
echo "1. Open http://localhost:3456 in your browser"
echo "2. Turn streaming ON and test"
echo "3. Turn streaming OFF and test"
echo "4. Compare the formatting"