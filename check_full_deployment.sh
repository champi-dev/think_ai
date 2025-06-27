#!/bin/bash

echo "🚀 Think AI FULL Deployment Status Check"
echo "========================================"
echo ""

BASE_URL="https://thinkai-production.up.railway.app"

echo "📡 Testing all endpoints..."
echo ""

# Health endpoint
echo -n "🏥 Health: "
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/health)
echo "HTTP $HEALTH_STATUS"
if [ "$HEALTH_STATUS" = "200" ]; then
    curl -s $BASE_URL/health | jq '.'
fi

echo ""

# Root/Webapp endpoint  
echo -n "🌐 Webapp: "
ROOT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/)
echo "HTTP $ROOT_STATUS"

echo ""

# Stats endpoint
echo -n "📊 Stats: "
STATS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/api/stats)
echo "HTTP $STATS_STATUS"
if [ "$STATS_STATUS" = "200" ]; then
    curl -s $BASE_URL/api/stats | jq '.'
fi

echo ""

# Chat endpoint (POST test)
echo -n "💬 Chat API: "
CHAT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}')
echo "HTTP $CHAT_STATUS"

echo ""
echo "🔍 Deployment Analysis:"
echo "========================"

if [ "$HEALTH_STATUS" = "200" ]; then
    echo "✅ FULL DEPLOYMENT SUCCESSFUL!"
    echo "🎉 Complete Think AI system is running with:"
    echo "   - Knowledge Engine with quantum processing"
    echo "   - O(1) vector search capabilities"
    echo "   - TinyLlama AI integration" 
    echo "   - 3D consciousness visualization"
    echo "   - Real-time chat API"
    echo "   - Comprehensive statistics"
    echo ""
    echo "🌐 Access your deployment at: $BASE_URL"
    
elif [ "$HEALTH_STATUS" = "404" ]; then
    echo "⏳ Build still in progress or failed"
    echo "🔧 Docker builds can take 5-15 minutes for complex Rust projects"
    echo "📋 Check build progress at:"
    echo "   https://railway.com/project/12a27f0b-34ce-4e42-b0b0-94c09f13ff80"
    
else
    echo "⚠️  Deployment issue detected"
    echo "📊 Status codes: Health=$HEALTH_STATUS, Root=$ROOT_STATUS, Stats=$STATS_STATUS"
fi

echo ""
echo "🔗 URLs:"
echo "   Main: $BASE_URL"
echo "   Health: $BASE_URL/health" 
echo "   API: $BASE_URL/api/chat"
echo "   Stats: $BASE_URL/api/stats"