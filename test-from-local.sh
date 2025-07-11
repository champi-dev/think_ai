#!/bin/bash

# Test Think AI from local machine to cloud GPU server
# Usage: ./test-from-local.sh <CLOUD_SERVER_IP>

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
CLOUD_SERVER_IP="${1:-}"
SERVER_PORT="${2:-8080}"
LOCAL_TEST_PORT="${3:-7777}"

if [ -z "$CLOUD_SERVER_IP" ]; then
    echo -e "${RED}Error: Please provide the cloud server IP address${NC}"
    echo "Usage: $0 <CLOUD_SERVER_IP> [SERVER_PORT] [LOCAL_TEST_PORT]"
    echo "Example: $0 123.45.67.89"
    echo "Example: $0 123.45.67.89 8080 7777"
    exit 1
fi

echo -e "${YELLOW}=== Think AI Cloud Server Testing ===${NC}"
echo "Cloud Server: $CLOUD_SERVER_IP:$SERVER_PORT"
echo "Local Test Port: $LOCAL_TEST_PORT"
echo ""

# Function to test endpoint
test_endpoint() {
    local endpoint=$1
    local method=$2
    local data=$3
    local description=$4
    
    echo -e "${YELLOW}Testing: $description${NC}"
    echo "Endpoint: $method $endpoint"
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "http://$CLOUD_SERVER_IP:$SERVER_PORT$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" \
            -H "Content-Type: application/json" \
            -d "$data" \
            "http://$CLOUD_SERVER_IP:$SERVER_PORT$endpoint")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ Success (HTTP $http_code)${NC}"
        echo "Response: $body" | head -n 3
    else
        echo -e "${RED}✗ Failed (HTTP $http_code)${NC}"
        echo "Response: $body"
    fi
    echo ""
}

# Test connectivity
echo -e "${YELLOW}1. Testing basic connectivity...${NC}"
if ping -c 1 "$CLOUD_SERVER_IP" &> /dev/null; then
    echo -e "${GREEN}✓ Server is reachable${NC}"
else
    echo -e "${RED}✗ Cannot reach server at $CLOUD_SERVER_IP${NC}"
    exit 1
fi
echo ""

# Test if server is running
echo -e "${YELLOW}2. Checking if Think AI server is running...${NC}"
if curl -s --connect-timeout 5 "http://$CLOUD_SERVER_IP:$SERVER_PORT/health" &> /dev/null; then
    echo -e "${GREEN}✓ Think AI server is responding${NC}"
else
    echo -e "${RED}✗ Think AI server is not responding on port $SERVER_PORT${NC}"
    echo "Make sure the server is running with: cargo run --release --bin think-ai-http"
    exit 1
fi
echo ""

# Run endpoint tests
echo -e "${YELLOW}3. Running endpoint tests...${NC}"

# Health check
test_endpoint "/health" "GET" "" "Health Check"

# Chat endpoint
test_endpoint "/api/chat" "POST" '{"message":"Hello from local test"}' "Chat API"

# Streaming chat
echo -e "${YELLOW}Testing: Streaming Chat${NC}"
echo "Testing WebSocket connection..."
timeout 5s curl -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
    "http://$CLOUD_SERVER_IP:$SERVER_PORT/api/chat/stream" 2>&1 | head -n 5 || true
echo ""

# Test web interface
echo -e "${YELLOW}4. Testing web interface...${NC}"
if curl -s "http://$CLOUD_SERVER_IP:$SERVER_PORT/" | grep -q "Think AI"; then
    echo -e "${GREEN}✓ Web interface is accessible${NC}"
    echo "You can open in browser: http://$CLOUD_SERVER_IP:$SERVER_PORT/"
else
    echo -e "${RED}✗ Web interface not found${NC}"
fi
echo ""

# Performance test
echo -e "${YELLOW}5. Running performance test...${NC}"
echo "Sending 10 rapid requests..."
start_time=$(date +%s.%N)
for i in {1..10}; do
    curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"message\":\"Test message $i\"}" \
        "http://$CLOUD_SERVER_IP:$SERVER_PORT/api/chat" > /dev/null &
done
wait
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo -e "${GREEN}✓ Completed 10 requests in ${duration}s${NC}"
echo ""

# SSH tunnel option
echo -e "${YELLOW}6. SSH Tunnel Instructions (Optional)${NC}"
echo "If you need secure access or face firewall issues, use SSH tunnel:"
echo -e "${GREEN}ssh -L $LOCAL_TEST_PORT:localhost:$SERVER_PORT user@$CLOUD_SERVER_IP${NC}"
echo "Then access locally at: http://localhost:$LOCAL_TEST_PORT"
echo ""

echo -e "${GREEN}=== Testing Complete ===${NC}"
echo "Server endpoints:"
echo "- Health: http://$CLOUD_SERVER_IP:$SERVER_PORT/health"
echo "- Chat API: http://$CLOUD_SERVER_IP:$SERVER_PORT/api/chat"
echo "- Web UI: http://$CLOUD_SERVER_IP:$SERVER_PORT/"