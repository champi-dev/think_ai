#!/bin/bash
set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Redeploy Think AI Full Stack with Quantum Generation    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Check current ngrok URL if available
CURRENT_NGROK_URL=""
if command -v curl &> /dev/null; then
    CURRENT_NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | jq -r '.tunnels[0].public_url' 2>/dev/null || echo "")
fi

if [ -n "$CURRENT_NGROK_URL" ]; then
    echo -e "${GREEN}Current ngrok URL: $CURRENT_NGROK_URL${NC}"
else
    echo -e "${YELLOW}No ngrok URL found. Will use placeholder.${NC}"
    CURRENT_NGROK_URL="https://your-ngrok-url.ngrok.io"
fi

echo ""
echo -e "${BLUE}=== Step 1: Backend Deployment Package ===${NC}"
echo "Backend package is ready in: deployment-quantum/"
echo ""
echo "To deploy backend on GPU server:"
echo "1. Copy files: scp -r deployment-quantum/ user@gpu-server:/path/to/think-ai/"
echo "2. SSH to server and run: ./start-quantum-server.sh"
echo ""

echo -e "${BLUE}=== Step 2: Frontend Deployment to Vercel ===${NC}"

# Update Vercel deployment files
echo -e "${YELLOW}Preparing Vercel deployment...${NC}"
rm -rf vercel-deploy
mkdir -p vercel-deploy

# Copy webapp files
cp think-ai-webapp/static/pwa.html vercel-deploy/index.html
cp think-ai-webapp/static/offline.html vercel-deploy/
cp think-ai-webapp/static/sw.js vercel-deploy/
cp think-ai-webapp/static/manifest.json vercel-deploy/
cp -r think-ai-webapp/static/icons vercel-deploy/
cp think-ai-webapp/static/icons/icon-16.png vercel-deploy/favicon.ico

# Update the index.html to highlight quantum features
sed -i 's|<h1 id="quantum-title">Think AI Quantum Core Active</h1>|<h1 id="quantum-title">Think AI Quantum Generation Active</h1>|g' vercel-deploy/index.html

# Create env config for dynamic backend URL
cat > vercel-deploy/config.js << EOF
// Think AI Configuration
window.THINK_AI_CONFIG = {
    // Update this with your ngrok URL after starting the GPU server
    API_URL: '${CURRENT_NGROK_URL}',
    FEATURES: {
        quantum_generation: true,
        qwen_only: true,
        isolated_threads: true,
        shared_intelligence: true,
        o1_performance: true
    }
};
EOF

# Update index.html to use config
sed -i '/<script>/a\    <script src="config.js"></script>' vercel-deploy/index.html

# Update API calls to use config
sed -i "s|http://localhost:8080|' + window.THINK_AI_CONFIG.API_URL + '|g" vercel-deploy/index.html
sed -i "s|https://thinkai-production.up.railway.app|' + window.THINK_AI_CONFIG.API_URL + '|g" vercel-deploy/index.html

# Create vercel.json
cat > vercel-deploy/vercel.json << EOF
{
  "name": "think-ai-quantum-webapp",
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    },
    {
      "source": "/sw.js",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "no-cache"
        },
        {
          "key": "Service-Worker-Allowed",
          "value": "/"
        }
      ]
    }
  ],
  "buildCommand": "",
  "outputDirectory": ".",
  "framework": null
}
EOF

# Create deployment info
cat > vercel-deploy/README.md << EOF
# Think AI Quantum Generation - Vercel Frontend

## New Quantum Features
- **Qwen-Only Generation**: All responses powered by Qwen 2.5
- **Isolated Parallel Threads**: 6 thread types with context isolation
- **Shared Intelligence**: Cross-thread learning system
- **O(1) Performance**: Hash-based caching for instant responses

## Configuration
Update \`config.js\` with your ngrok URL after starting the GPU server.

## Architecture
- Frontend: Vercel (this deployment)
- Backend: GPU Server with ngrok tunnel
EOF

echo -e "${GREEN}✅ Vercel deployment prepared in ./vercel-deploy/${NC}"
echo ""

# Create quick deployment guide
cat > QUICK_DEPLOY.md << EOF
# Think AI Quantum Generation - Quick Deployment Guide

## Backend (GPU Server)
1. Copy deployment: \`scp -r deployment-quantum/ user@gpu-server:/path/to/\`
2. SSH to server: \`ssh user@gpu-server\`
3. Start server: \`cd deployment-quantum && ./start-quantum-server.sh\`
4. Note the ngrok URL shown in output

## Frontend (Vercel)
1. Update ngrok URL in \`vercel-deploy/config.js\`
2. Deploy: \`cd vercel-deploy && vercel --prod\`
3. Visit your Vercel URL

## Features
✓ Qwen-only generation (no fallback)
✓ Isolated parallel threads
✓ Shared intelligence
✓ O(1) performance

## Testing
- Chat endpoint: \`[ngrok-url]/api/chat\`
- Quantum chat: \`[ngrok-url]/api/quantum-chat\`
- Parallel chat: \`[ngrok-url]/api/parallel-chat\`
EOF

echo -e "${BLUE}=== Deployment Instructions ===${NC}"
echo ""
echo -e "${YELLOW}1. Backend Deployment:${NC}"
echo "   a. Copy: scp -r deployment-quantum/ user@gpu-server:/path/"
echo "   b. SSH and run: ./start-quantum-server.sh"
echo "   c. Note the ngrok URL"
echo ""
echo -e "${YELLOW}2. Frontend Deployment:${NC}"
echo "   a. Update vercel-deploy/config.js with ngrok URL"
echo "   b. Run: cd vercel-deploy && vercel --prod"
echo ""
echo -e "${GREEN}✨ Quantum Features Deployed:${NC}"
echo "  • Qwen-only generation"
echo "  • Isolated parallel threads"
echo "  • Shared intelligence"
echo "  • O(1) performance"
echo ""
echo -e "${BLUE}See QUICK_DEPLOY.md for detailed instructions${NC}"