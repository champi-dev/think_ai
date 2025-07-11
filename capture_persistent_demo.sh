#!/bin/bash

# Start server on test port
PORT=3456 ./target/release/think-ai-full-persistent > demo_server.log 2>&1 &
SERVER_PID=$!
echo "Demo server started with PID: $SERVER_PID"

# Wait for server
sleep 3

# Create demo conversation
echo "=== DEMO: Persistent Chat Conversation ==="
echo ""

# Message 1
echo ">>> User: Hi, I'm Sarah and I'm a data scientist working on machine learning models for healthcare."
RESP1=$(curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi, I am Sarah and I am a data scientist working on machine learning models for healthcare."}')
SESSION=$(echo $RESP1 | jq -r '.session_id')
echo "<<< AI: $(echo $RESP1 | jq -r '.response' | head -c 150)..."
echo "Session ID: $SESSION"
echo ""
sleep 2

# Message 2
echo ">>> User: What's my name?"
RESP2=$(curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What's my name?\", \"session_id\": \"$SESSION\"}")
echo "<<< AI: $(echo $RESP2 | jq -r '.response' | head -c 150)..."
echo ""
sleep 2

# Message 3
echo ">>> User: What field do I work in?"
RESP3=$(curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What field do I work in?\", \"session_id\": \"$SESSION\"}")
echo "<<< AI: $(echo $RESP3 | jq -r '.response' | head -c 200)..."
echo ""
sleep 2

# Message 4
echo ">>> User: delete my history"
RESP4=$(curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"delete my history\", \"session_id\": \"$SESSION\"}")
NEW_SESSION=$(echo $RESP4 | jq -r '.session_id')
echo "<<< AI: $(echo $RESP4 | jq -r '.response')"
echo "New Session ID: $NEW_SESSION"
echo ""
sleep 2

# Message 5 - Verify deletion
echo ">>> User: Do you remember my name?"
RESP5=$(curl -s -X POST http://localhost:3456/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Do you remember my name?\", \"session_id\": \"$NEW_SESSION\"}")
echo "<<< AI: $(echo $RESP5 | jq -r '.response' | head -c 200)..."
echo ""

echo "=== DEMO COMPLETE ==="
echo ""
echo "Key Features Demonstrated:"
echo "✅ Persistent conversation memory"
echo "✅ Context retention across messages"
echo "✅ History deletion functionality"
echo "✅ Session management"

# Cleanup
kill $SERVER_PID 2>/dev/null || true