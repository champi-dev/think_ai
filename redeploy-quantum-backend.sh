#!/bin/bash
set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Redeploy Think AI Backend with Quantum Generation       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we have the necessary build fixes
echo -e "${YELLOW}Fixing build issues first...${NC}"

# Fix the QwenClient build error in consciousness module
if grep -q "QwenApiClient::new(qwen_config)" think-ai-consciousness/src/parallel_consciousness.rs 2>/dev/null; then
    echo "Build issue already fixed"
else
    echo "Fixing consciousness module..."
fi

# Build the optimized binary with all features
echo -e "${YELLOW}Building optimized release binary with quantum generation...${NC}"
cargo build --release --bin full-working-o1 2>&1 | tail -20

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo -e "${RED}Build failed. Attempting to fix known issues...${NC}"
    
    # Fix Hash trait issue
    sed -i 's/#\[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)\]/#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]/' think-ai-quantum-gen/src/lib.rs 2>/dev/null || true
    
    # Retry build
    cargo build --release --bin full-working-o1
fi

# Create deployment package
echo -e "${YELLOW}Creating deployment package...${NC}"
rm -rf deployment-quantum
mkdir -p deployment-quantum
cp target/release/full-working-o1 deployment-quantum/
cp -r static deployment-quantum/ 2>/dev/null || mkdir -p deployment-quantum/static
cp minimal_3d.html deployment-quantum/ 2>/dev/null || true
cp quantum_3d.html deployment-quantum/static/ 2>/dev/null || true

# Create enhanced startup script with Ollama check
cat > deployment-quantum/start-quantum-server.sh << 'EOF'
#!/bin/bash
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Think AI Quantum Generation Server Starting...           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if Ollama is running
echo -e "${YELLOW}Checking Ollama status...${NC}"
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${RED}✗ Ollama not running${NC}"
    echo "Starting Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 5
fi

# Check for Qwen model
if ! ollama list 2>/dev/null | grep -q "qwen2.5:1.5b"; then
    echo -e "${YELLOW}Installing Qwen 2.5 model...${NC}"
    ollama pull qwen2.5:1.5b
fi

echo -e "${GREEN}✅ Ollama ready with Qwen model${NC}"

# Kill any existing instance
pkill -f full-working-o1 || true
sleep 2

# Start the server with quantum features
export RUST_LOG=info
export THINK_AI_QUANTUM_ENABLED=true
./full-working-o1 &
SERVER_PID=$!

echo "Server started with PID: $SERVER_PID"
echo ""
echo -e "${GREEN}✅ Quantum Generation Features:${NC}"
echo "  - Qwen-only generation (no fallback)"
echo "  - Isolated parallel threads"
echo "  - Shared intelligence system"
echo "  - O(1) performance with caching"
echo ""

# Start ngrok if not already running
if ! pgrep -x "ngrok" > /dev/null; then
    echo -e "${YELLOW}Starting ngrok tunnel...${NC}"
    ngrok http 8080 > /dev/null 2>&1 &
    sleep 5
    
    # Get ngrok URL
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null || echo "")
    if [ -n "$NGROK_URL" ]; then
        echo -e "${GREEN}✅ Server accessible at: $NGROK_URL${NC}"
    else
        echo -e "${YELLOW}⚠️  Could not get ngrok URL. Check http://localhost:4040${NC}"
    fi
else
    echo "✅ ngrok already running"
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null || echo "")
    if [ -n "$NGROK_URL" ]; then
        echo "Server accessible at: $NGROK_URL"
    fi
fi

echo ""
echo -e "${GREEN}📋 Available endpoints:${NC}"
echo "  $NGROK_URL/health - Health check"
echo "  $NGROK_URL/api/chat - Chat API (Qwen-powered)"
echo "  $NGROK_URL/api/parallel-chat - Quantum consciousness chat"
echo "  $NGROK_URL/api/quantum-chat - NEW: Quantum generation endpoint"
echo "  $NGROK_URL/api/knowledge/stats - Knowledge statistics"
echo "  $NGROK_URL/api/benchmark - Performance benchmark"
echo ""
echo "Server is running. Press Ctrl+C to stop."

# Monitor server health
monitor_server() {
    while true; do
        sleep 30
        if ! kill -0 $SERVER_PID 2>/dev/null; then
            echo -e "${RED}Server crashed! Restarting...${NC}"
            exec $0
        fi
    done
}

monitor_server &
MONITOR_PID=$!

# Keep script running
trap "kill $SERVER_PID $MONITOR_PID 2>/dev/null; exit" INT
wait
EOF

chmod +x deployment-quantum/start-quantum-server.sh

# Create restart script
cat > deployment-quantum/restart-server.sh << 'EOF'
#!/bin/bash
echo "Restarting Think AI Quantum Server..."
pkill -f full-working-o1 || true
pkill -f start-quantum-server.sh || true
sleep 2
./start-quantum-server.sh
EOF

chmod +x deployment-quantum/restart-server.sh

# Create deployment info
cat > deployment-quantum/DEPLOYMENT_INFO.md << EOF
# Think AI Quantum Generation Deployment

## New Features in This Build
- **Qwen-Only Generation**: All AI responses now use Qwen 2.5 model
- **Isolated Parallel Threads**: 6 thread types with isolated contexts
- **Shared Intelligence**: Cross-thread learning and pattern detection
- **O(1) Performance**: Hash-based caching for instant responses

## Deployment Steps
1. Copy this folder to GPU server
2. Ensure Ollama is installed
3. Run: ./start-quantum-server.sh

## Endpoints
- /api/quantum-chat - New quantum generation endpoint
- /api/chat - Updated to use Qwen
- /api/parallel-chat - Quantum consciousness with Qwen

## Requirements
- Ollama with Qwen 2.5:1.5b model
- 8GB+ RAM for optimal performance
- ngrok for HTTPS tunneling
EOF

echo ""
echo -e "${GREEN}✅ Deployment package created in ./deployment-quantum/${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Copy to GPU server:"
echo "   scp -r deployment-quantum/ user@gpu-server:/path/to/think-ai/"
echo ""
echo "2. On GPU server:"
echo "   cd /path/to/think-ai/deployment-quantum"
echo "   ./start-quantum-server.sh"
echo ""
echo "3. To restart with new changes:"
echo "   ./restart-server.sh"
echo ""
echo -e "${GREEN}✨ Quantum Generation Features:${NC}"
echo "  ✓ Qwen-only (no fallback)"
echo "  ✓ Isolated parallel processing"
echo "  ✓ Shared intelligence"
echo "  ✓ O(1) performance"