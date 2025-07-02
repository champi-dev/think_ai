#!/bin/bash

echo "🚂 Testing Railway Deployment Configuration"
echo "=========================================="

# Test 1: Check if PORT environment variable is respected
echo "Test 1: Port Environment Variable Support"
PORT=9999 timeout 10s ./target/release/full-server &
SERVER_PID=$!
sleep 3

if curl -s http://localhost:9999/health > /dev/null; then
    echo "✅ Server responds on custom port 9999"
else
    echo "❌ Server not responding on custom port"
fi

kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

# Test 2: Check health endpoint response time
echo -e "\nTest 2: Health Check Response Time"
./target/release/full-server &
SERVER_PID=$!
sleep 8  # Wait for initialization

START_TIME=$(date +%s%N)
HEALTH_RESPONSE=$(curl -s http://localhost:8080/health)
END_TIME=$(date +%s%N)
RESPONSE_TIME=$(( (END_TIME - START_TIME) / 1000000 ))

echo "Health endpoint response: $HEALTH_RESPONSE"
echo "Response time: ${RESPONSE_TIME}ms"

if [ $RESPONSE_TIME -lt 1000 ]; then
    echo "✅ Health check responds quickly (${RESPONSE_TIME}ms)"
else
    echo "⚠️ Health check is slow (${RESPONSE_TIME}ms) - may timeout on Railway"
fi

kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

# Test 3: Validate Railway configuration
echo -e "\nTest 3: Railway Configuration"
if [ -f "railway.json" ]; then
    echo "✅ railway.json exists"
    if grep -q "healthcheckPath" railway.json; then
        echo "✅ Health check path configured"
    else
        echo "❌ Health check path missing"
    fi
    
    if grep -q "healthcheckTimeout.*300" railway.json; then
        echo "✅ Health check timeout set to 300s"
    else
        echo "❌ Health check timeout not configured"
    fi
else
    echo "❌ railway.json missing"
fi

# Test 4: Docker build validation
echo -e "\nTest 4: Docker Build Test"
if docker build -t think-ai-test . > /dev/null 2>&1; then
    echo "✅ Docker builds successfully"
    
    # Test container startup
    CONTAINER_ID=$(docker run -d -p 9998:8080 -e PORT=8080 think-ai-test)
    sleep 10
    
    if curl -s http://localhost:9998/health > /dev/null; then
        echo "✅ Docker container serves health check"
    else
        echo "❌ Docker container health check failed"
    fi
    
    docker stop $CONTAINER_ID > /dev/null 2>&1
    docker rm $CONTAINER_ID > /dev/null 2>&1
else
    echo "❌ Docker build failed"
fi

echo -e "\n🚂 Railway Deployment Test Complete"
echo "Ready to deploy with: railway up"