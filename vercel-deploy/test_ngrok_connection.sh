#!/bin/bash

echo "Testing ngrok connection..."
echo ""

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

if [ -z "$NGROK_URL" ]; then
    echo "❌ No ngrok tunnel found. Make sure ngrok is running."
    exit 1
fi

echo "✅ Found ngrok URL: $NGROK_URL"
echo ""

# Test health endpoint
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$NGROK_URL/health")

if [ "$HEALTH_RESPONSE" = "200" ]; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed (HTTP $HEALTH_RESPONSE)"
fi

# Test chat endpoint
echo ""
echo "Testing chat endpoint..."
CHAT_RESPONSE=$(curl -s -X POST "$NGROK_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"message": "Test message"}' | jq -r '.response')

if [ -n "$CHAT_RESPONSE" ]; then
    echo "✅ Chat endpoint working"
    echo "Response: $CHAT_RESPONSE"
else
    echo "❌ Chat endpoint failed"
fi

echo ""
echo "Done! Your webapp is configured to use: $NGROK_URL"