#!/bin/bash

echo "🧪 Think AI E2E Deployment Test"
echo "==============================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# GPU Server URL
GPU_SERVER="http://69.197.178.37:8080"
VERCEL_APP="https://think-ai-liart.vercel.app"

echo "Testing configuration:"
echo "GPU Server: $GPU_SERVER"
echo "Vercel App: $VERCEL_APP"
echo ""

# Test 1: GPU Server Health Check
echo -e "${YELLOW}Test 1: GPU Server Health Check${NC}"
if curl -s -f "$GPU_SERVER/health" > /dev/null; then
    echo -e "${GREEN}✅ GPU Server is running${NC}"
else
    echo -e "${RED}❌ GPU Server is not accessible${NC}"
    echo "Make sure to run ./deploy-gpu-server.sh on your GPU server"
fi
echo ""

# Test 2: GPU Server API Endpoint
echo -e "${YELLOW}Test 2: GPU Server API Test${NC}"
RESPONSE=$(curl -s -X POST "$GPU_SERVER/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"message":"test"}' 2>/dev/null)

if [ ! -z "$RESPONSE" ]; then
    echo -e "${GREEN}✅ GPU Server API is responding${NC}"
    echo "Response: $RESPONSE" | head -n 2
else
    echo -e "${RED}❌ GPU Server API is not responding${NC}"
fi
echo ""

# Test 3: CORS Headers Check
echo -e "${YELLOW}Test 3: CORS Headers Check${NC}"
CORS_HEADERS=$(curl -s -I -X OPTIONS "$GPU_SERVER/api/chat" \
    -H "Origin: $VERCEL_APP" \
    -H "Access-Control-Request-Method: POST" \
    2>/dev/null | grep -i "access-control")

if [ ! -z "$CORS_HEADERS" ]; then
    echo -e "${GREEN}✅ CORS headers are present${NC}"
    echo "$CORS_HEADERS"
else
    echo -e "${RED}❌ CORS headers missing${NC}"
fi
echo ""

# Test 4: Vercel App Load Test
echo -e "${YELLOW}Test 4: Vercel App Accessibility${NC}"
if curl -s -f "$VERCEL_APP" > /dev/null; then
    echo -e "${GREEN}✅ Vercel app is accessible${NC}"
else
    echo -e "${RED}❌ Vercel app is not accessible${NC}"
fi
echo ""

# Test 5: End-to-End Test from Browser Simulation
echo -e "${YELLOW}Test 5: E2E API Call Simulation${NC}"
echo "Simulating browser request from Vercel to GPU server..."

BROWSER_TEST=$(curl -s -X POST "$GPU_SERVER/api/chat" \
    -H "Content-Type: application/json" \
    -H "Origin: $VERCEL_APP" \
    -H "Referer: $VERCEL_APP/" \
    -d '{"message":"What is O(1) performance?"}' 2>/dev/null)

if [ ! -z "$BROWSER_TEST" ] && [[ "$BROWSER_TEST" == *"response"* ]]; then
    echo -e "${GREEN}✅ E2E test successful${NC}"
    echo "API Response received"
else
    echo -e "${RED}❌ E2E test failed${NC}"
    echo "Check firewall settings on GPU server"
fi
echo ""

# Summary
echo -e "${YELLOW}Summary:${NC}"
echo "1. Run ./deploy-gpu-server.sh on your GPU server (69.197.178.37)"
echo "2. Ensure firewall allows port 8080"
echo "3. Vercel app is deployed at: $VERCEL_APP"
echo ""
echo "If GPU server is not publicly accessible, consider using ngrok:"
echo "  ngrok http 8080"
echo "Then update vercel.json with the ngrok URL"