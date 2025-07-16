#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🧠 ETERNAL CONTEXT LOCAL SERVER${NC}"
echo "================================"
echo ""

# Get local IP
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo -e "${GREEN}Your local IP: $LOCAL_IP${NC}"
echo ""

# Kill any existing process
lsof -ti:7878 | xargs kill -9 2>/dev/null || true

# Start server
echo -e "${YELLOW}Starting eternal context server...${NC}"
echo "Server will be available at:"
echo -e "${GREEN}  - http://localhost:7878${NC}"
echo -e "${GREEN}  - http://$LOCAL_IP:7878${NC}"
echo ""

# Start the server
PORT=7878 ./target/release/eternal-context-server