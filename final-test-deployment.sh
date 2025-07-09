#!/bin/bash

echo "🧪 Final deployment test for Ollama + Qwen"
echo "=========================================="
echo ""

# Wait for deployment
echo "⏳ Waiting 3 minutes for deployment with pre-cached models..."
sleep 180

# Test endpoints
echo "📊 Testing endpoints..."

# 1. Health check
echo -n "1. Health: "
curl -s "https://thinkai-production.up.railway.app/health"
echo ""

# 2. Math test (should use Qwen)
echo -n "2. Math test: "
START=$(date +%s.%N)
RESPONSE=$(curl -s -X POST "https://thinkai-production.up.railway.app/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "What is 2+2?"}')
END=$(date +%s.%N)
ELAPSED=$(echo "$END - $START" | bc)

echo "$RESPONSE" | jq -r .response
echo "   Time: ${ELAPSED}s"

if (( $(echo "$ELAPSED < 3" | bc -l) )); then
    echo "   ✅ Fast response - likely using Qwen!"
else
    echo "   ⚠️ Slow response - might be timeout/fallback"
fi

# 3. General test
echo -n "3. General test: "
START=$(date +%s.%N)
RESPONSE=$(curl -s -X POST "https://thinkai-production.up.railway.app/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "What is the capital of France?"}')
END=$(date +%s.%N)
ELAPSED=$(echo "$END - $START" | bc)

echo "$RESPONSE" | jq -r .response | head -c 100
echo "..."
echo "   Time: ${ELAPSED}s"

echo ""
echo "✅ Test complete!"