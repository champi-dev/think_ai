#!/bin/bash

# Test script for Think AI local tunnel connection

echo "🧪 Testing Think AI Local Tunnel Connection"
echo "=========================================="
echo ""

# The ngrok URL from the previous run
TUNNEL_URL="https://37fdf7867ba2.ngrok.app"
LOCAL_URL="http://localhost:3456"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Testing local connection...${NC}"
echo "------------------------"

# Test local health endpoint
echo -n "Testing local health endpoint: "
if curl -s ${LOCAL_URL}/health | grep -q "healthy"; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ Failed${NC}"
fi

echo ""
echo -e "${BLUE}Testing tunnel connection...${NC}"
echo "-------------------------"

# Test tunnel health endpoint
echo -n "Testing tunnel health endpoint: "
if curl -s ${TUNNEL_URL}/health | grep -q "healthy"; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ Failed${NC}"
fi

echo ""
echo -e "${BLUE}Testing Chat API...${NC}"
echo "----------------"

# Test chat API
echo "Sending test message to chat API..."
RESPONSE=$(curl -s -X POST ${TUNNEL_URL}/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Think AI! What is your O(1) performance capability?"}')

if [ ! -z "$RESPONSE" ]; then
    echo -e "${GREEN}✅ Got response:${NC}"
    echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
else
    echo -e "${RED}❌ No response${NC}"
fi

echo ""
echo -e "${BLUE}Access URLs:${NC}"
echo "------------"
echo "🌐 Local: ${LOCAL_URL}"
echo "🌍 Remote (via ngrok): ${TUNNEL_URL}"
echo ""
echo "You can now access Think AI from anywhere using the ngrok URL!"
echo "Share this URL to access from other devices: ${TUNNEL_URL}"