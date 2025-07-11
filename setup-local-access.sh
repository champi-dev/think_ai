#!/bin/bash

# Setup local access to Think AI on cloud GPU server
# Provides multiple methods for secure access

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=== Think AI Local Access Setup ===${NC}"
echo ""

# Method 1: Direct Connection
echo -e "${YELLOW}Method 1: Direct Connection${NC}"
echo "If your cloud server has a public IP and open ports:"
echo -e "${GREEN}./test-from-local.sh <CLOUD_SERVER_IP>${NC}"
echo ""

# Method 2: SSH Tunnel
echo -e "${YELLOW}Method 2: SSH Tunnel (Recommended for security)${NC}"
echo "Create a secure tunnel to your cloud server:"
echo -e "${GREEN}ssh -L 7777:localhost:8080 user@<CLOUD_SERVER_IP>${NC}"
echo "Then access Think AI at: http://localhost:7777"
echo ""

# Method 3: Ngrok
echo -e "${YELLOW}Method 3: Ngrok (For temporary public access)${NC}"
echo "On your cloud server, run:"
echo -e "${GREEN}ngrok http 8080${NC}"
echo "Use the provided ngrok URL to access from anywhere"
echo ""

# Method 4: Tailscale
echo -e "${YELLOW}Method 4: Tailscale (For persistent secure access)${NC}"
echo "Install Tailscale on both machines:"
echo "Cloud server: ${GREEN}curl -fsSL https://tailscale.com/install.sh | sh${NC}"
echo "Local machine: Install from https://tailscale.com/download"
echo "Then access using Tailscale IP"
echo ""

# Create SSH tunnel helper
cat > ssh-tunnel-helper.sh << 'EOF'
#!/bin/bash
# SSH Tunnel Helper for Think AI

CLOUD_USER="${1:-user}"
CLOUD_IP="${2:-}"
LOCAL_PORT="${3:-7777}"
REMOTE_PORT="${4:-8080}"

if [ -z "$CLOUD_IP" ]; then
    echo "Usage: $0 [USER] <CLOUD_IP> [LOCAL_PORT] [REMOTE_PORT]"
    echo "Example: $0 ubuntu 123.45.67.89"
    exit 1
fi

echo "Creating SSH tunnel..."
echo "Local: http://localhost:$LOCAL_PORT"
echo "Remote: $CLOUD_USER@$CLOUD_IP:$REMOTE_PORT"
echo ""
echo "Press Ctrl+C to close tunnel"

ssh -N -L $LOCAL_PORT:localhost:$REMOTE_PORT $CLOUD_USER@$CLOUD_IP
EOF

chmod +x ssh-tunnel-helper.sh

echo -e "${GREEN}✓ Created ssh-tunnel-helper.sh${NC}"
echo ""

# Create local test client
cat > test-client.py << 'EOF'
#!/usr/bin/env python3
"""Think AI Test Client - Test from local machine"""

import requests
import json
import sys
import time
from typing import Optional

class ThinkAIClient:
    def __init__(self, base_url: str = "http://localhost:7777"):
        self.base_url = base_url.rstrip('/')
        
    def health_check(self) -> bool:
        """Check if server is healthy"""
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def chat(self, message: str) -> Optional[str]:
        """Send chat message"""
        try:
            resp = requests.post(
                f"{self.base_url}/api/chat",
                json={"message": message},
                timeout=10
            )
            if resp.status_code == 200:
                return resp.json().get("response", "")
            else:
                print(f"Error: {resp.status_code} - {resp.text}")
                return None
        except Exception as e:
            print(f"Connection error: {e}")
            return None
    
    def benchmark(self, iterations: int = 10):
        """Run performance benchmark"""
        print(f"Running {iterations} requests...")
        times = []
        
        for i in range(iterations):
            start = time.time()
            self.chat(f"Test message {i}")
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        print(f"Average response time: {avg_time*1000:.2f}ms")
        print(f"Min: {min(times)*1000:.2f}ms, Max: {max(times)*1000:.2f}ms")

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:7777"
    
    client = ThinkAIClient(base_url)
    
    print(f"Testing Think AI at: {base_url}")
    
    # Health check
    if client.health_check():
        print("✓ Server is healthy")
    else:
        print("✗ Server is not responding")
        return
    
    # Interactive mode
    print("\nEntering interactive mode (type 'exit' to quit, 'bench' to benchmark)")
    
    while True:
        try:
            message = input("\nYou: ").strip()
            
            if message.lower() == 'exit':
                break
            elif message.lower() == 'bench':
                client.benchmark()
                continue
            
            response = client.chat(message)
            if response:
                print(f"AI: {response}")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
EOF

chmod +x test-client.py

echo -e "${GREEN}✓ Created test-client.py${NC}"
echo ""

echo -e "${BLUE}=== Quick Start Guide ===${NC}"
echo ""
echo "1. First, start Think AI on your cloud server:"
echo "   ${GREEN}cargo run --release --bin think-ai-http${NC}"
echo ""
echo "2. Choose your connection method:"
echo ""
echo "   ${YELLOW}Option A: SSH Tunnel (Recommended)${NC}"
echo "   On your local machine:"
echo "   ${GREEN}./ssh-tunnel-helper.sh ubuntu <CLOUD_IP>${NC}"
echo ""
echo "   ${YELLOW}Option B: Direct Connection${NC}"
echo "   ${GREEN}./test-from-local.sh <CLOUD_IP>${NC}"
echo ""
echo "3. Test with Python client:"
echo "   ${GREEN}python3 test-client.py${NC}"
echo ""
echo "For more options, check the created scripts!"