#!/bin/bash

# Think AI Full System Local Deployment Script
# Runs the complete system on 0.0.0.0:7777

set -e

echo "🚀 Think AI Full System - Local Deployment on Port 7777"
echo "======================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
MAIN_PORT=7777
BACKEND_PORT=7778  # Internal backend port
WEBAPP_PORT=7779   # Internal webapp port

# Function to kill processes on specific ports
kill_port() {
    local port=$1
    echo -e "${YELLOW}Cleaning up port $port...${NC}"
    lsof -ti:$port | xargs -r kill -9 2>/dev/null || true
    sleep 1
}

# Function to check if a port is available
check_port() {
    local port=$1
    if lsof -ti:$port >/dev/null 2>&1; then
        return 1
    else
        return 0
    fi
}

# Function to wait for service
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=0
    
    echo -e "${BLUE}Waiting for $service_name to start...${NC}"
    while [ $attempt -lt $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $service_name is ready!${NC}"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 1
    done
    
    echo -e "${RED}✗ $service_name failed to start${NC}"
    return 1
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"
    kill_port $MAIN_PORT
    kill_port $BACKEND_PORT
    kill_port $WEBAPP_PORT
    echo -e "${GREEN}✓ Cleanup complete${NC}"
}

# Set trap for cleanup on exit
trap cleanup EXIT

# Step 1: Clean up ports
echo -e "\n${BLUE}Step 1: Cleaning up ports...${NC}"
kill_port $MAIN_PORT
kill_port $BACKEND_PORT
kill_port $WEBAPP_PORT

# Step 2: Check if binaries exist
echo -e "\n${BLUE}Step 2: Checking binaries...${NC}"
if [ ! -f "./target/release/stable-server" ]; then
    echo -e "${YELLOW}Building Think AI system...${NC}"
    cargo build --release
fi

# Step 3: Start backend server
echo -e "\n${BLUE}Step 3: Starting backend server on port $BACKEND_PORT...${NC}"
PORT=$BACKEND_PORT ./target/release/stable-server > backend_$BACKEND_PORT.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend server started (PID: $BACKEND_PID)${NC}"

# Wait for backend to be ready
wait_for_service "http://localhost:$BACKEND_PORT/health" "Backend Server"

# Step 4: Start webapp server (if available)
echo -e "\n${BLUE}Step 4: Starting webapp server...${NC}"
if [ -f "./target/release/webapp-server" ]; then
    PORT=$WEBAPP_PORT ./target/release/webapp-server > webapp_$WEBAPP_PORT.log 2>&1 &
    WEBAPP_PID=$!
    echo -e "${GREEN}✓ Webapp server started (PID: $WEBAPP_PID)${NC}"
fi

# Step 5: Start main proxy/frontend server
echo -e "\n${BLUE}Step 5: Starting main server on port $MAIN_PORT...${NC}"

# Create a simple Python proxy server that serves both static content and proxies API calls
cat > /tmp/think_ai_proxy_$MAIN_PORT.py << 'EOF'
#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.request
import urllib.parse
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

MAIN_PORT = int(sys.argv[1])
BACKEND_PORT = int(sys.argv[2])
WEBAPP_PORT = int(sys.argv[3]) if len(sys.argv) > 3 else None

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the main page
            self.serve_file('webapp_temp.html', 'text/html')
        elif self.path.startswith('/static/'):
            # Serve static files
            file_path = self.path[1:]  # Remove leading /
            if self.path.endswith('.js'):
                self.serve_file(file_path, 'application/javascript')
            elif self.path.endswith('.css'):
                self.serve_file(file_path, 'text/css')
            else:
                self.serve_file(file_path)
        elif self.path == '/health':
            # Health check
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'OK - Think AI Full System Running on Port ' + str(MAIN_PORT).encode())
        elif self.path.startswith('/api/') or self.path == '/stats' or self.path == '/chat':
            # Proxy to backend - map /api/chat to /chat
            backend_path = self.path
            if self.path == '/api/chat':
                backend_path = '/chat'
            elif self.path == '/api/chat/stream':
                backend_path = '/chat'  # Map streaming to regular chat for now
            self.proxy_request(f'http://localhost:{BACKEND_PORT}{backend_path}')
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/chat' or self.path.startswith('/api/'):
            # Proxy to backend - map /api/chat to /chat
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            backend_path = self.path
            if self.path == '/api/chat':
                backend_path = '/chat'
            elif self.path == '/api/chat/stream':
                backend_path = '/chat'  # Map streaming to regular chat for now
            self.proxy_request(f'http://localhost:{BACKEND_PORT}{backend_path}', post_data)
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def serve_file(self, path, content_type=None):
        try:
            with open(path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            if content_type:
                self.send_header('Content-Type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)
        except Exception as e:
            print(f"Error serving file: {e}")
            self.send_error(500)
    
    def proxy_request(self, url, data=None):
        try:
            req = urllib.request.Request(url)
            if data:
                req.data = data
                req.add_header('Content-Type', self.headers.get('Content-Type', 'application/json'))
            
            with urllib.request.urlopen(req, timeout=30) as response:
                self.send_response(response.getcode())
                for header, value in response.headers.items():
                    if header.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(header, value)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response.read())
        except urllib.error.HTTPError as e:
            self.send_error(e.code)
        except Exception as e:
            print(f"Proxy error: {e}")
            self.send_error(502)
    
    def log_message(self, format, *args):
        # Reduce logging noise
        if '/health' not in self.path:
            super().log_message(format, *args)

# Change to Think AI directory
os.chdir('/home/administrator/think_ai')

# Start server
print(f"🚀 Think AI Full System starting on 0.0.0.0:{MAIN_PORT}")
print(f"   Backend: http://localhost:{BACKEND_PORT}")
if WEBAPP_PORT:
    print(f"   Webapp: http://localhost:{WEBAPP_PORT}")
print(f"\n📍 Access the system at: http://0.0.0.0:{MAIN_PORT}")

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", MAIN_PORT), ProxyHandler) as httpd:
    httpd.serve_forever()
EOF

python3 /tmp/think_ai_proxy_$MAIN_PORT.py $MAIN_PORT $BACKEND_PORT $WEBAPP_PORT &
PROXY_PID=$!

# Step 6: Final status
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Think AI Full System is running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\nServices:"
echo -e "  ${BLUE}Main Interface:${NC} http://0.0.0.0:$MAIN_PORT"
echo -e "  ${BLUE}Backend API:${NC}    http://localhost:$BACKEND_PORT"
if [ -n "$WEBAPP_PID" ]; then
    echo -e "  ${BLUE}Webapp Server:${NC}  http://localhost:$WEBAPP_PORT"
fi
echo -e "\nEndpoints:"
echo -e "  ${YELLOW}GET${NC}  / - Main web interface"
echo -e "  ${YELLOW}GET${NC}  /health - Health check"
echo -e "  ${YELLOW}GET${NC}  /stats - System statistics"
echo -e "  ${YELLOW}POST${NC} /chat - Chat API"
echo -e "  ${YELLOW}POST${NC} /api/chat - Alternative chat endpoint"
echo -e "\nLogs:"
echo -e "  Backend: ./backend_$BACKEND_PORT.log"
echo -e "  Webapp:  ./webapp_$WEBAPP_PORT.log"
echo -e "\n${YELLOW}Press Ctrl+C to stop all services${NC}"

# Keep script running
wait