#!/bin/bash

# Deploy the latest Think AI with streaming/CSS updates to GPU server
# This script prepares everything needed for deployment

set -e

echo "=== Deploy Latest Think AI to Production GPU Server ==="
echo
echo "This script will prepare the deployment package with:"
echo "- Latest streaming functionality"
echo "- CSS updates (JetBrains Mono, animations)"
echo "- Enhanced markdown rendering"
echo

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if deployment directory exists and has latest build
if [ ! -f "deployment/full-working-o1" ]; then
    echo -e "${YELLOW}Binary not found in deployment/. Building...${NC}"
    ./deploy-to-gpu-server.sh
fi

# Verify the webapp has latest changes
echo -e "${BLUE}Verifying deployment has latest updates...${NC}"
echo

if grep -q "JetBrains Mono" deployment/minimal_3d.html; then
    echo -e "${GREEN}✓${NC} JetBrains Mono font (CSS update)"
else
    echo -e "${YELLOW}⚠${NC} Missing JetBrains Mono font"
fi

if grep -q "streaming-text" deployment/minimal_3d.html; then
    echo -e "${GREEN}✓${NC} Streaming functionality"
else
    echo -e "${YELLOW}⚠${NC} Missing streaming functionality"
fi

if grep -q "fade-in" deployment/minimal_3d.html; then
    echo -e "${GREEN}✓${NC} Fade-in animations"
else
    echo -e "${YELLOW}⚠${NC} Missing fade-in animations"
fi

echo
echo -e "${GREEN}=== Deployment Package Ready ===${NC}"
echo
echo "The deployment/ directory contains:"
ls -la deployment/
echo

echo -e "${BLUE}To deploy to your GPU server:${NC}"
echo
echo "1. Copy the deployment folder to your GPU server:"
echo -e "   ${YELLOW}scp -r deployment/* user@your-gpu-server:/path/to/think-ai/${NC}"
echo
echo "2. SSH into your GPU server:"
echo -e "   ${YELLOW}ssh user@your-gpu-server${NC}"
echo
echo "3. Stop the current service (if running):"
echo -e "   ${YELLOW}sudo systemctl stop think-ai${NC}"
echo "   or"
echo -e "   ${YELLOW}pkill -f full-working-o1${NC}"
echo
echo "4. Replace the binary and files:"
echo -e "   ${YELLOW}cd /path/to/think-ai/${NC}"
echo -e "   ${YELLOW}cp deployment/full-working-o1 ./${NC}"
echo -e "   ${YELLOW}cp deployment/minimal_3d.html ./${NC}"
echo -e "   ${YELLOW}chmod +x full-working-o1${NC}"
echo
echo "5. Start the service:"
echo -e "   ${YELLOW}sudo systemctl start think-ai${NC}"
echo "   or"
echo -e "   ${YELLOW}./full-working-o1 &${NC}"
echo
echo "6. Verify the deployment:"
echo -e "   ${YELLOW}curl http://localhost:8080/health${NC}"
echo

# Create a verification script
cat > deployment/verify-deployment.sh << 'EOF'
#!/bin/bash

# Verify Think AI deployment
echo "=== Verifying Think AI Deployment ==="

# Check if service is running
if pgrep -f "full-working-o1" > /dev/null; then
    echo "✓ Think AI process is running"
else
    echo "✗ Think AI process is NOT running"
    exit 1
fi

# Check health endpoint
if curl -s http://localhost:8080/health | grep -q "healthy"; then
    echo "✓ Health endpoint responding"
else
    echo "✗ Health endpoint not responding"
fi

# Check for streaming functionality
if curl -s http://localhost:8080/ | grep -q "streaming-text"; then
    echo "✓ Streaming functionality present"
else
    echo "✗ Streaming functionality missing"
fi

# Check for CSS updates
if curl -s http://localhost:8080/ | grep -q "JetBrains Mono"; then
    echo "✓ CSS updates (JetBrains Mono) present"
else
    echo "✗ CSS updates missing"
fi

echo
echo "Deployment verification complete!"
EOF

chmod +x deployment/verify-deployment.sh

echo -e "${GREEN}Created deployment/verify-deployment.sh${NC}"
echo "Run this script on your GPU server after deployment to verify everything is working."
echo