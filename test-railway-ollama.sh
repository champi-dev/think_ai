#!/bin/bash

echo "🧪 Testing Railway Deployment with Ollama/Qwen"
echo "============================================"

# Get service URL
SERVICE_URL=$(railway status 2>/dev/null | grep -oP 'https://[^ ]+' | head -1)

if [ -z "$SERVICE_URL" ]; then
    echo "❌ No Railway service URL found. Is the deployment running?"
    echo "Run: railway status"
    exit 1
fi

echo "🌐 Service URL: $SERVICE_URL"
echo ""

# Test health endpoint
echo "1️⃣ Testing /health endpoint..."
HEALTH=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$SERVICE_URL/health")
echo "Response: $HEALTH"
echo ""

# Test chat with simple query
echo "2️⃣ Testing /chat endpoint with 'hi'..."
CHAT_RESPONSE=$(curl -s -X POST "$SERVICE_URL/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "hi"}' \
    -w "\nHTTP_CODE:%{http_code}")
echo "Response: $CHAT_RESPONSE"
echo ""

# Test with longer timeout
echo "3️⃣ Testing /chat with longer timeout (30s)..."
CHAT_LONG=$(curl -s -X POST "$SERVICE_URL/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "What is 2+2?"}' \
    --max-time 30 \
    -w "\nHTTP_CODE:%{http_code}")
echo "Response: $CHAT_LONG"
echo ""

# Check logs for Ollama status
echo "4️⃣ Recent deployment logs mentioning Ollama/Qwen:"
railway logs -d 2>/dev/null | grep -E "(Ollama|Qwen|qwen2.5|11434)" | tail -20

echo ""
echo "✅ Test complete!"