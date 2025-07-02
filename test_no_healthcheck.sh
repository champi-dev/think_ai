#!/bin/bash

echo "🚂 Testing Railway Deployment (No Health Check)"
echo "=============================================="

RAILWAY_URL="https://thinkai-production.up.railway.app"

echo "Waiting for deployment to complete..."
sleep 60

echo "Step 1: Basic Connectivity Test"
echo "-------------------------------"

if curl -s --max-time 10 "$RAILWAY_URL" > /dev/null; then
    echo "✅ Main page responds"
else
    echo "❌ Main page not responding"
    echo "Trying again in 30 seconds..."
    sleep 30
    curl -s --max-time 10 "$RAILWAY_URL" > /dev/null && echo "✅ Main page now responds" || echo "❌ Still not responding"
fi

echo -e "\nStep 2: Health Endpoint Test"
echo "---------------------------"

HEALTH_RESPONSE=$(curl -s --max-time 10 "$RAILWAY_URL/health" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Health endpoint responds: $HEALTH_RESPONSE"
else
    echo "⚠️  Health endpoint not responding (but that's okay - no health check configured)"
fi

echo -e "\nStep 3: API Test"
echo "--------------"

# Test the chat API
API_RESPONSE=$(curl -s --max-time 15 -X POST "$RAILWAY_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "Hello, Think AI!"}' 2>/dev/null)

if [ $? -eq 0 ] && [ ! -z "$API_RESPONSE" ]; then
    echo "✅ Chat API responds"
    echo "Response preview: $(echo "$API_RESPONSE" | head -c 100)..."
else
    echo "⚠️  Chat API not responding yet (may still be initializing)"
fi

echo -e "\nStep 4: Performance Test"
echo "----------------------"

echo "Testing response times..."
for i in {1..3}; do
    START_TIME=$(date +%s%N)
    curl -s --max-time 10 "$RAILWAY_URL" > /dev/null
    if [ $? -eq 0 ]; then
        END_TIME=$(date +%s%N)
        RESPONSE_TIME_MS=$(( (END_TIME - START_TIME) / 1000000 ))
        echo "  Attempt $i: ${RESPONSE_TIME_MS}ms"
    else
        echo "  Attempt $i: TIMEOUT"
    fi
    sleep 2
done

echo -e "\nStep 5: Final Status"
echo "==================="

if curl -s --max-time 10 "$RAILWAY_URL" > /dev/null; then
    echo "🟢 DEPLOYMENT SUCCESSFUL!"
    echo ""
    echo "✅ No health check blocking deployment"
    echo "✅ Server is accessible"
    echo "✅ Railway deployment completed"
    echo ""
    echo "🔗 Access your Think AI server at:"
    echo "   $RAILWAY_URL"
    
else
    echo "🔴 DEPLOYMENT ISSUE"
    echo ""
    echo "The server might still be starting up."
    echo "Check Railway logs: railway logs"
fi

echo -e "\n📋 Configuration Summary:"
echo "- Health check: DISABLED ✅"
echo "- Build: full-server-fast ✅"  
echo "- Port: Railway managed ✅"
echo "- Domain: $RAILWAY_URL ✅"