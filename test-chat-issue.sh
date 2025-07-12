#!/bin/bash
# Test script to reproduce the chat hanging issue

echo "Testing chat functionality..."

# First question - should work
echo "1. Testing first question..."
curl -X POST http://localhost:8080/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "hi"}' \
  -N --no-buffer > test1.txt 2>&1 &
PID1=$!
sleep 5
kill $PID1 2>/dev/null
echo "First response:"
cat test1.txt | head -10
echo ""

# Wait a bit
sleep 2

# Second question - reportedly hangs
echo "2. Testing second question..."
curl -X POST http://localhost:8080/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "what is love"}' \
  -N --no-buffer > test2.txt 2>&1 &
PID2=$!
sleep 5
kill $PID2 2>/dev/null
echo "Second response:"
cat test2.txt | head -10
echo ""

# Check if server is still responsive
echo "3. Checking server health..."
curl -s http://localhost:8080/health

# Clean up
rm -f test1.txt test2.txt