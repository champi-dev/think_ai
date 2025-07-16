#!/bin/bash

# Restart all Think AI services

echo "🔄 Restarting all Think AI services..."
echo "====================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Step 1: Clean up old processes
echo -e "${BLUE}🧹 Cleaning up old processes...${NC}"

# Kill processes on test ports (but NOT 8080 - that's prod!)
lsof -ti:3456 | xargs kill -9 2>/dev/null || true
lsof -ti:5555 | xargs kill -9 2>/dev/null || true
lsof -ti:7777 | xargs kill -9 2>/dev/null || true

# Kill old ngrok processes
pkill ngrok 2>/dev/null || true

# Kill proxy server
pkill -f "proxy_server.py" 2>/dev/null || true

echo -e "${GREEN}✅ Cleanup complete${NC}"

# Step 2: Start production domain tunnel (ngrok for thinkai.lat)
echo -e "${BLUE}🌐 Starting production domain tunnel...${NC}"

# Check if ngrok is authenticated
if ! ngrok config check >/dev/null 2>&1; then
    echo -e "${RED}❌ ngrok not configured. Please run: ngrok config add-authtoken YOUR_TOKEN${NC}"
    exit 1
fi

# Start ngrok for the production domain
nohup ngrok http 8080 --domain=thinkai.lat > /tmp/ngrok-prod.log 2>&1 &
NGROK_PROD_PID=$!
echo "Production ngrok started with PID: $NGROK_PROD_PID"

# Step 3: Start local test server
echo -e "${BLUE}🚀 Starting local test server on port 3456...${NC}"

if [ -f "deployment-quantum/full-working-o1" ]; then
    PORT=3456 nohup ./deployment-quantum/full-working-o1 > /tmp/think-ai-local.log 2>&1 &
    LOCAL_PID=$!
    echo "Local server started with PID: $LOCAL_PID"
elif [ -f "./target/release/full-server" ]; then
    PORT=3456 nohup ./target/release/full-server > /tmp/think-ai-local.log 2>&1 &
    LOCAL_PID=$!
    echo "Local server started with PID: $LOCAL_PID"
else
    echo -e "${YELLOW}⚠️  No binary found for local server${NC}"
fi

# Step 4: Start ngrok for local access
echo -e "${BLUE}🌐 Starting ngrok tunnel for local server...${NC}"
sleep 3  # Wait for local server to start

nohup ngrok http 3456 --region=us > /tmp/ngrok-local.log 2>&1 &
NGROK_LOCAL_PID=$!
echo "Local ngrok started with PID: $NGROK_LOCAL_PID"

# Wait for services to start
echo -e "${BLUE}⏳ Waiting for services to start...${NC}"
sleep 5

# Step 5: Check status
echo ""
echo -e "${BLUE}📊 Service Status:${NC}"
echo "=================="

# Check production
echo -n "Production server (8080): "
if curl -s http://localhost:8080/health >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Running${NC}"
else
    echo -e "${RED}❌ Not responding${NC}"
fi

# Check production domain
echo -n "Production domain (thinkai.lat): "
if ps -p $NGROK_PROD_PID > /dev/null; then
    echo -e "${GREEN}✅ Tunnel active${NC}"
    echo "   Access at: https://thinkai.lat"
else
    echo -e "${RED}❌ Tunnel failed${NC}"
fi

# Check local server
echo -n "Local server (3456): "
if curl -s http://localhost:3456/health >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Running${NC}"
else
    echo -e "${RED}❌ Not responding${NC}"
fi

# Get local ngrok URL
echo -n "Local ngrok tunnel: "
sleep 2
LOCAL_TUNNEL_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"[^"]*' | grep -o 'http[^"]*' | grep -v "thinkai.lat" | head -1)

if [ ! -z "$LOCAL_TUNNEL_URL" ]; then
    HTTPS_URL=${LOCAL_TUNNEL_URL/http:/https:}
    echo -e "${GREEN}✅ Active${NC}"
    echo "   Access at: $HTTPS_URL"
else
    echo -e "${YELLOW}⚠️  Pending...${NC}"
fi

echo ""
echo -e "${BLUE}📋 Summary:${NC}"
echo "==========="
echo "Production: https://thinkai.lat"
if [ ! -z "$HTTPS_URL" ]; then
    echo "Local test: $HTTPS_URL"
fi
echo "ngrok dashboard: http://localhost:4040"
echo ""
echo -e "${GREEN}✅ All services restarted!${NC}"

# Save PIDs for later cleanup
echo "NGROK_PROD_PID=$NGROK_PROD_PID" > /tmp/think-ai-pids.sh
echo "NGROK_LOCAL_PID=$NGROK_LOCAL_PID" >> /tmp/think-ai-pids.sh
echo "LOCAL_PID=$LOCAL_PID" >> /tmp/think-ai-pids.sh

echo ""
echo "To stop all services later, run:"
echo "source /tmp/think-ai-pids.sh && kill \$NGROK_PROD_PID \$NGROK_LOCAL_PID \$LOCAL_PID"