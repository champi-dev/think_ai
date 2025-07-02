#!/bin/bash

echo "🚂 Final Railway Health Check Analysis"
echo "====================================="

RAILWAY_URL="https://thinkai-production.up.railway.app"

echo "Step 1: Testing Debug Server Deployment"
echo "--------------------------------------"

echo "Waiting for deployment to complete..."
sleep 30

echo "Testing basic connectivity..."
if curl -s --max-time 10 "$RAILWAY_URL" > /dev/null; then
    echo "✅ Main page responds"
else
    echo "❌ Main page not responding"
fi

echo -e "\nStep 2: Health Check Analysis"
echo "----------------------------"

echo "Testing /health endpoint..."
HEALTH_RESPONSE=$(curl -s --max-time 10 "$RAILWAY_URL/health" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Health check responds: $HEALTH_RESPONSE"
else
    echo "❌ Health check failed"
fi

echo "Testing /healthz endpoint..."
HEALTHZ_RESPONSE=$(curl -s --max-time 10 "$RAILWAY_URL/healthz" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Alternative health check responds: $HEALTHZ_RESPONSE"
else
    echo "❌ Alternative health check failed"
fi

echo -e "\nStep 3: Environment Variable Analysis"
echo "-----------------------------------"

echo "Testing /api/env endpoint..."
ENV_DATA=$(curl -s --max-time 10 "$RAILWAY_URL/api/env" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Environment data retrieved"
    echo "$ENV_DATA" | python3 -m json.tool 2>/dev/null | head -50
else
    echo "❌ Environment endpoint failed"
fi

echo -e "\nStep 4: Network Diagnostics"
echo "--------------------------"

echo "Testing with different HTTP methods..."
curl -X HEAD -s --max-time 5 "$RAILWAY_URL/health" && echo "✅ HEAD request works" || echo "❌ HEAD request fails"
curl -X GET -s --max-time 5 "$RAILWAY_URL/health" > /dev/null && echo "✅ GET request works" || echo "❌ GET request fails"

echo -e "\nTesting with different user agents..."
curl -H "User-Agent: Railway-HealthCheck" -s --max-time 5 "$RAILWAY_URL/health" > /dev/null && echo "✅ Railway user agent works" || echo "❌ Railway user agent fails"

echo -e "\nStep 5: Timing Analysis"
echo "---------------------"

echo "Measuring response times..."
for i in {1..3}; do
    START_TIME=$(date +%s%N)
    curl -s --max-time 5 "$RAILWAY_URL/health" > /dev/null
    if [ $? -eq 0 ]; then
        END_TIME=$(date +%s%N)
        RESPONSE_TIME_MS=$(( (END_TIME - START_TIME) / 1000000 ))
        echo "  Attempt $i: ${RESPONSE_TIME_MS}ms"
    else
        echo "  Attempt $i: FAILED"
    fi
    sleep 1
done

echo -e "\nStep 6: Summary & Recommendations"
echo "==============================="

# Test if any endpoint works
if curl -s --max-time 10 "$RAILWAY_URL/health" > /dev/null || 
   curl -s --max-time 10 "$RAILWAY_URL/healthz" > /dev/null ||
   curl -s --max-time 10 "$RAILWAY_URL/" > /dev/null; then
    
    echo "🟢 SERVER IS RUNNING - Health check configuration issue"
    echo ""
    echo "Possible solutions:"
    echo "1. Railway may be checking a different endpoint"
    echo "2. Health check timeout might be too short"
    echo "3. Railway may require specific response format"
    echo ""
    echo "Debug steps:"
    echo "- Check Railway dashboard for specific error messages"
    echo "- Review the environment variables at $RAILWAY_URL/api/env"
    echo "- Verify Railway is using the correct health check path"
    
else
    echo "🔴 SERVER NOT RESPONDING - Infrastructure issue"
    echo ""
    echo "Possible solutions:"
    echo "1. Check Railway build logs for compilation errors"
    echo "2. Verify Dockerfile is correct"
    echo "3. Check if Railway service is running"
    echo ""
    echo "Next steps:"
    echo "- Run: railway logs"
    echo "- Check: railway status"
    echo "- Verify: Dockerfile builds locally"
fi

echo -e "\n📊 Configuration Check"
echo "--------------------"

if [ -f "railway.json" ]; then
    echo "✅ railway.json exists"
    cat railway.json | python3 -m json.tool
else
    echo "❌ railway.json missing"
fi

echo -e "\n🔗 Useful Links:"
echo "- Production URL: $RAILWAY_URL"
echo "- Health Check: $RAILWAY_URL/health"
echo "- Environment: $RAILWAY_URL/api/env"
echo "- Railway Dashboard: https://railway.app/dashboard"