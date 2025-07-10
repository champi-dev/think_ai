#!/bin/bash

echo "🧪 Testing Think AI Qwen Integration"
echo "===================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Ollama is running
echo -e "${YELLOW}1. Checking if Ollama is running...${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama is running${NC}"
else
    echo -e "${RED}✗ Ollama is not running. Please start Ollama first:${NC}"
    echo "   ollama serve"
    exit 1
fi

# Check if Qwen model is available
echo -e "${YELLOW}2. Checking if Qwen model is available...${NC}"
if ollama list | grep -q "qwen"; then
    echo -e "${GREEN}✓ Qwen model is available${NC}"
else
    echo -e "${RED}✗ Qwen model not found. Please pull it:${NC}"
    echo "   ollama pull qwen2.5:1.5b"
    exit 1
fi

# Build the project
echo -e "${YELLOW}3. Building the Think AI system...${NC}"
cd /home/administrator/think_ai
cargo build --release 2>&1 | tail -n 10

# Kill any existing server on port 8080
echo -e "${YELLOW}4. Killing existing servers on port 8080...${NC}"
pkill -f "think-ai-full" || true
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
sleep 2

# Start the server in background
echo -e "${YELLOW}5. Starting Think AI server...${NC}"
./target/release/think-ai-full &
SERVER_PID=$!
sleep 3

# Function to test endpoint
test_endpoint() {
    local query="$1"
    local description="$2"
    
    echo -e "${YELLOW}Testing: $description${NC}"
    
    response=$(curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d "{\"message\": \"$query\"}" | jq -r '.response')
    
    if [ -z "$response" ] || [[ "$response" == "null" ]]; then
        echo -e "${RED}✗ No response received${NC}"
        return 1
    fi
    
    # Check if it's the generic template response
    if [[ "$response" == *"That's an interesting question about"* ]] && [[ "$response" == *"While exploring this topic"* ]]; then
        echo -e "${RED}✗ Still using generic template response${NC}"
        echo "Response: $response"
        return 1
    fi
    
    echo -e "${GREEN}✓ Got Qwen-generated response${NC}"
    echo "Response preview: ${response:0:100}..."
    return 0
}

# Test various queries
echo -e "\n${YELLOW}6. Testing various queries...${NC}"
echo "================================"

test_endpoint "What is the universe?" "Universe query"
echo ""

test_endpoint "Tell me about quantum mechanics" "Quantum query"
echo ""

test_endpoint "What is consciousness?" "Consciousness query"
echo ""

test_endpoint "How do you work?" "System query"
echo ""

test_endpoint "What is love?" "Philosophy query"
echo ""

# Kill the server
echo -e "\n${YELLOW}7. Cleaning up...${NC}"
kill $SERVER_PID 2>/dev/null || true

echo -e "\n${GREEN}✅ Test complete!${NC}"
echo ""
echo "To run the server permanently:"
echo "  cd /home/administrator/think_ai"
echo "  ./target/release/think-ai-full"
echo ""
echo "To test manually:"
echo "  curl -X POST http://localhost:8080/api/chat \\"
echo "    -H \"Content-Type: application/json\" \\"
echo "    -d '{\"message\": \"Your question here\"}'"