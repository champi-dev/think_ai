#!/bin/bash
set -e

echo "=== Deploy Think AI to GPU Server ==="
echo "This script deploys the full-working-o1 server with all endpoints"
echo

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Build the optimized binary
echo "🏗️  Building optimized release binary..."
cargo build --release --bin full-working-o1

# Create deployment package
echo "📦 Creating deployment package..."
mkdir -p deployment
cp target/release/full-working-o1 deployment/
cp -r static deployment/ 2>/dev/null || mkdir -p deployment/static
cp minimal_3d.html deployment/ 2>/dev/null || true
cp quantum_3d.html deployment/static/ 2>/dev/null || true

# Create startup script
cat > deployment/start-gpu-server.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Think AI on GPU Server..."
echo "✅ All endpoints enabled:"
echo "  - /health"
echo "  - /api/chat"
echo "  - /api/parallel-chat (Quantum Consciousness)"
echo "  - /api/knowledge/stats"
echo "  - /api/benchmark"

# Kill any existing instance
pkill -f full-working-o1 || true
sleep 2

# Start the server
export RUST_LOG=info
./full-working-o1 &
SERVER_PID=$!

echo "Server started with PID: $SERVER_PID"
echo

# Start ngrok if not already running
if ! pgrep -x "ngrok" > /dev/null; then
    echo "🌐 Starting ngrok tunnel..."
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

echo
echo "📋 Available endpoints:"
echo "  $NGROK_URL/health - Health check"
echo "  $NGROK_URL/api/chat - Chat API"
echo "  $NGROK_URL/api/parallel-chat - Quantum consciousness chat"
echo "  $NGROK_URL/api/knowledge/stats - Knowledge statistics"
echo "  $NGROK_URL/api/benchmark - Performance benchmark"
echo
echo "Server is running. Press Ctrl+C to stop."

# Keep script running
trap "kill $SERVER_PID 2>/dev/null; exit" INT
wait
EOF

chmod +x deployment/start-gpu-server.sh

# Create systemd service (optional)
cat > deployment/think-ai.service << EOF
[Unit]
Description=Think AI Quantum Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/administrator/think_ai/deployment
ExecStart=/home/administrator/think_ai/deployment/start-gpu-server.sh
Restart=always
RestartSec=10
User=administrator
Environment="RUST_LOG=info"

[Install]
WantedBy=multi-user.target
EOF

echo
echo -e "${GREEN}✅ Deployment package created in ./deployment/${NC}"
echo
echo "📋 Next steps:"
echo "1. Copy deployment folder to GPU server:"
echo "   scp -r deployment/ user@gpu-server:/path/to/think-ai/"
echo
echo "2. On GPU server, run:"
echo "   cd /path/to/think-ai/deployment"
echo "   ./start-gpu-server.sh"
echo
echo "3. Or install as systemd service:"
echo "   sudo cp think-ai.service /etc/systemd/system/"
echo "   sudo systemctl enable think-ai"
echo "   sudo systemctl start think-ai"
echo
echo "4. Update Vercel webapp to use ngrok URL"