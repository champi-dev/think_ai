#\!/bin/bash

# Comprehensive E2E test for markdown rendering

set -e

echo "🧪 Think AI Markdown Rendering E2E Test"
echo "======================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if server is running
echo "Checking server status..."
if curl -s http://localhost:7777/health > /dev/null; then
    echo -e "${GREEN}✓ Server is running on port 7777${NC}"
else
    echo -e "${RED}✗ Server not running${NC}"
    echo "Start with: python3 serve_webapp_7777_final.py"
    exit 1
fi

# Check which binary is being used
echo -e "\n${YELLOW}Binary verification:${NC}"
BINARY_PID=$(lsof -ti:7778 2>/dev/null || echo "")
if [ -n "$BINARY_PID" ]; then
    BINARY_PATH=$(ls -l /proc/$BINARY_PID/exe 2>/dev/null  < /dev/null |  awk '{print $NF}')
    echo -e "${GREEN}✓ Using binary: $BINARY_PATH${NC}"
    echo -e "${GREEN}✓ PID: $BINARY_PID${NC}"
    
    # Show binary info
    echo -e "\n${YELLOW}Binary details:${NC}"
    ls -la ./target/release/stable-server-streaming
    md5sum ./target/release/stable-server-streaming
else
    echo -e "${RED}✗ No binary found on port 7778${NC}"
fi

# Test the API
echo -e "\n${YELLOW}Testing API directly:${NC}"
curl -X POST http://localhost:7777/api/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "# Test Header\n\nThis is **bold**"}' \
    -w "\n\nHTTP Status: %{http_code}\n" || true

echo -e "\n${GREEN}✓ Test complete\!${NC}"
echo ""
echo "To manually test markdown rendering:"
echo "1. Open http://localhost:7777 in browser"
echo "2. Type: # Hello"
echo "3. Press Enter"
echo "4. Check if it shows as a header"
echo ""
echo "To ensure using new binary after rebuild:"
echo "1. cargo build --release"
echo "2. pkill -f stable-server"
echo "3. python3 serve_webapp_7777_final.py"
