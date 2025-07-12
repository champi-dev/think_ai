#!/bin/bash

echo "=== Think AI Session Server Testing Script ==="
echo

# Check if server is already running
echo "1. Checking current server status..."
ps aux | grep -E "stable-server|7777" | grep -v grep
echo

# Test the server on port 7777
echo "2. Testing server on port 7777..."
curl -s http://localhost:7777/ > /dev/null && echo "✅ Server is running on port 7777" || echo "❌ Server not responding on port 7777"
echo

# Test session functionality
echo "3. Testing session memory..."
SESSION_ID="test-session-$(date +%s)"

# First message
echo "   Sending: 'Remember my name is TestUser'"
RESPONSE1=$(curl -s -X POST http://localhost:7777/chat \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"Remember my name is TestUser\",\"session_id\":\"$SESSION_ID\"}")
echo "   Response: $RESPONSE1"
echo

# Second message (should remember)
echo "   Sending: 'What is my name?'"
RESPONSE2=$(curl -s -X POST http://localhost:7777/chat \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"What is my name?\",\"session_id\":\"$SESSION_ID\"}")
echo "   Response: $RESPONSE2"
echo

# Check session history
echo "4. Checking session history..."
curl -s http://localhost:7777/session/$SESSION_ID | jq . 2>/dev/null || curl -s http://localhost:7777/session/$SESSION_ID
echo

echo "5. Server access URLs:"
echo "   - Local: http://localhost:7777"
echo "   - SSH Tunnel: ssh -L 7777:localhost:7777 administrator@69.197.178.37"
echo "   - Direct: http://69.197.178.37:7777 (if firewall allows)"
echo

echo "=== Test Complete ==="