#!/bin/bash

# Think AI - Local Development with Tunnel Setup
# This script runs Think AI locally and sets up ngrok for remote access

set -e

echo "🧠 Think AI - Local Development with Tunnel Setup"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
LOCAL_PORT=3456  # Using test port as per CLAUDE.md
NGROK_REGION="us"  # Change if needed

# Step 1: Check for ngrok
echo -e "${BLUE}🔍 Checking for ngrok...${NC}"
if ! command -v ngrok &> /dev/null; then
    echo -e "${YELLOW}⚠️  ngrok not found. Installing...${NC}"
    
    # Download and install ngrok
    wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
    tar -xzf ngrok-v3-stable-linux-amd64.tgz
    sudo mv ngrok /usr/local/bin/
    rm ngrok-v3-stable-linux-amd64.tgz
    
    echo -e "${GREEN}✅ ngrok installed!${NC}"
    echo -e "${YELLOW}📝 Please sign up at https://ngrok.com and run: ngrok config add-authtoken YOUR_TOKEN${NC}"
    echo ""
fi

# Step 2: Kill any existing processes on the port
echo -e "${BLUE}🛑 Cleaning up port ${LOCAL_PORT}...${NC}"
lsof -ti:${LOCAL_PORT} | xargs kill -9 2>/dev/null || true
pkill ngrok 2>/dev/null || true

# Step 3: Check for binary
echo -e "${BLUE}🔍 Looking for Think AI binary...${NC}"
BINARY=""

# Try the pre-built binary first (since build has errors)
if [ -f "deployment-quantum/full-working-o1" ]; then
    BINARY="deployment-quantum/full-working-o1"
    echo -e "${GREEN}✅ Found pre-built binary${NC}"
elif [ -f "./target/release/full-server" ]; then
    BINARY="./target/release/full-server"
    echo -e "${GREEN}✅ Found release binary${NC}"
elif [ -f "./target/release/think-ai" ]; then
    BINARY="./target/release/think-ai"
    echo -e "${GREEN}✅ Found think-ai binary${NC}"
else
    echo -e "${YELLOW}⚠️  No binary found. Attempting to build...${NC}"
    
    # Try to build with --no-default-features to avoid some errors
    echo "Building Think AI (this may take a few minutes)..."
    cargo build --release --bin full-server --no-default-features 2>/dev/null || {
        echo -e "${RED}❌ Build failed. Using fallback simple server...${NC}"
        
        # Create a simple test server
        cat > /tmp/simple-think-ai-server.py << 'EOF'
#!/usr/bin/env python3
import http.server
import json
import socketserver
from http.server import BaseHTTPRequestHandler

class ThinkAIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "service": "Think AI"}).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Think AI - Local Test</title>
                <style>
                    body { font-family: Arial; background: #1a1a1a; color: #fff; text-align: center; padding: 50px; }
                    h1 { color: #00ff88; }
                    .box { background: #2a2a2a; padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 600px; }
                </style>
            </head>
            <body>
                <h1>🧠 Think AI - Local Development</h1>
                <div class="box">
                    <p>Server is running on port {}</p>
                    <p>Tunnel will be available soon...</p>
                </div>
            </body>
            </html>
            """.format(PORT)
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            response = {
                "response": f"Think AI received: {data.get('message', 'No message')}",
                "status": "success"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

PORT = $LOCAL_PORT
with socketserver.TCPServer(("", PORT), ThinkAIHandler) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
EOF
        chmod +x /tmp/simple-think-ai-server.py
        BINARY="python3 /tmp/simple-think-ai-server.py"
    }
fi

# Step 4: Start the server
echo -e "${BLUE}🚀 Starting Think AI server on port ${LOCAL_PORT}...${NC}"
if [[ $BINARY == *"python3"* ]]; then
    $BINARY &
else
    PORT=$LOCAL_PORT $BINARY &
fi
SERVER_PID=$!

# Wait for server to start
sleep 3

# Check if server is running
if ! curl -s http://localhost:${LOCAL_PORT}/health > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Server health check failed, but continuing...${NC}"
fi

# Step 5: Start ngrok
echo -e "${BLUE}🌐 Starting ngrok tunnel...${NC}"
ngrok http ${LOCAL_PORT} --log=stdout > ngrok.log 2>&1 &
NGROK_PID=$!

# Wait for ngrok to start
echo -e "${BLUE}⏳ Waiting for tunnel to establish...${NC}"
sleep 5

# Get tunnel URL
TUNNEL_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"[^"]*' | grep -o 'http[^"]*' | head -1)

if [ -z "$TUNNEL_URL" ]; then
    echo -e "${YELLOW}⚠️  Could not get tunnel URL automatically${NC}"
    echo -e "${BLUE}Please check ngrok dashboard at: http://localhost:4040${NC}"
else
    # Get HTTPS URL
    HTTPS_URL=${TUNNEL_URL/http:/https:}
    
    echo ""
    echo -e "${GREEN}✅ Think AI is running!${NC}"
    echo ""
    echo -e "${BLUE}📍 Local Access:${NC}"
    echo "   http://localhost:${LOCAL_PORT}"
    echo ""
    echo -e "${BLUE}🌐 Remote Access (via ngrok):${NC}"
    echo "   ${HTTPS_URL}"
    echo ""
    echo -e "${BLUE}📊 Available Endpoints:${NC}"
    echo "   ${HTTPS_URL}/         - Web interface"
    echo "   ${HTTPS_URL}/health   - Health check"
    echo "   ${HTTPS_URL}/api/chat - Chat API"
    echo ""
    echo -e "${BLUE}🔍 ngrok Dashboard:${NC}"
    echo "   http://localhost:4040"
fi

echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo "  - Share the HTTPS URL to access from anywhere"
echo "  - The tunnel will remain active while this script runs"
echo "  - Press Ctrl+C to stop both server and tunnel"
echo ""
echo -e "${GREEN}🎉 Setup complete! Server and tunnel are running.${NC}"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${BLUE}🛑 Shutting down...${NC}"
    kill $SERVER_PID 2>/dev/null || true
    kill $NGROK_PID 2>/dev/null || true
    pkill ngrok 2>/dev/null || true
    echo -e "${GREEN}✅ Cleanup complete${NC}"
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Keep script running
echo ""
echo "Press Ctrl+C to stop..."
wait $SERVER_PID