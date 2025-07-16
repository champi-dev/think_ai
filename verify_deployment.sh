#!/bin/bash

echo "🔍 Verifying Think AI Deployment"
echo "================================"

if [ -z "$1" ]; then
    echo "Usage: ./verify_deployment.sh <your-railway-url>"
    echo "Example: ./verify_deployment.sh https://think-ai-api-production.up.railway.app"
    exit 1
fi

URL=$1

echo "Checking: $URL"
echo ""

# Check health endpoint
echo "1. Health check..."
curl -s "$URL/health" || echo "❌ Health check failed"
echo ""

# Check stats endpoint
echo "2. Stats endpoint..."
curl -s "$URL/api/stats" | jq '.' || echo "❌ Stats endpoint failed"
echo ""

# Check if Next.js (wrong deployment)
echo "3. Checking for Next.js (should fail)..."
if curl -s "$URL/_next/static/" | grep -q "404"; then
    echo "✅ Good: No Next.js files found"
else
    echo "❌ ERROR: Next.js files detected - wrong deployment!"
fi
echo ""

# Test chat endpoint
echo "4. Testing chat endpoint..."
curl -s -X POST "$URL/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello"}' | jq '.' || echo "❌ Chat endpoint failed"
echo ""

# Check webapp
echo "5. Checking webapp..."
if curl -s "$URL/" | grep -q "Think AI"; then
    echo "✅ Webapp loaded successfully"
else
    echo "❌ Webapp not found"
fi

echo ""
echo "Verification complete!"