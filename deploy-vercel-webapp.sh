#!/bin/bash

# Deploy Think AI webapp to Vercel (static frontend)
# GPU server handles all computation-intensive tasks

set -euo pipefail

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Configuration - Update this to your GPU server URL
GPU_SERVER_URL="${GPU_SERVER_URL:-http://gpu.databasemart.com:8080}"

# Create Vercel deployment directory
prepare_vercel_deployment() {
    log_info "Preparing webapp for Vercel deployment..."
    
    # Create deployment directory
    rm -rf vercel-deploy
    mkdir -p vercel-deploy
    cd vercel-deploy
    
    # Copy static files
    cp ../think-ai-webapp/static/pwa.html index.html
    cp ../think-ai-webapp/static/offline.html .
    cp ../think-ai-webapp/static/sw.js .
    cp ../think-ai-webapp/static/manifest.json .
    cp ../think-ai-webapp/static/favicon.ico .
    cp -r ../think-ai-webapp/static/icons .
    
    # Update API endpoint in index.html to point to GPU server
    sed -i "s|http://localhost:8080|${GPU_SERVER_URL}|g" index.html
    sed -i "s|https://thinkai-production.up.railway.app|${GPU_SERVER_URL}|g" index.html
    
    # Create vercel.json with GPU server routing
    cat > vercel.json << EOF
{
  "name": "think-ai-webapp",
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "${GPU_SERVER_URL}/api/\$1"
    }
  ],
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

    # Create README for Vercel
    cat > README.md << EOF
# Think AI Webapp - Vercel Deployment

This is the static frontend for Think AI, deployed on Vercel for global CDN distribution.

## Architecture
- **Frontend**: Static PWA on Vercel (this deployment)
- **Backend**: GPU server at ${GPU_SERVER_URL} (handles all computation)

## Features
- O(1) performance algorithms
- PWA with offline support
- Real-time chat interface
- GPU-accelerated AI processing

## API Endpoints
All API calls are proxied to the GPU server:
- \`/api/chat\` → \`${GPU_SERVER_URL}/api/chat\`
- \`/api/process\` → \`${GPU_SERVER_URL}/api/process\`
- \`/health\` → \`${GPU_SERVER_URL}/health\`
EOF

    log_info "Vercel deployment prepared in ./vercel-deploy/"
}

# Deploy to Vercel
deploy_to_vercel() {
    log_info "Deploying to Vercel..."
    
    # Check if vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        log_info "Installing Vercel CLI..."
        npm i -g vercel
    fi
    
    # Deploy
    echo -e "${BLUE}Deploying to Vercel...${NC}"
    echo -e "${YELLOW}When prompted:${NC}"
    echo -e "  - Set up and deploy: ${GREEN}Y${NC}"
    echo -e "  - Which scope: ${GREEN}Select your account${NC}"
    echo -e "  - Link to existing project: ${GREEN}N${NC} (unless you have one)"
    echo -e "  - Project name: ${GREEN}think-ai-webapp${NC}"
    echo -e "  - Directory: ${GREEN}.${NC} (current directory)"
    echo -e "  - Override settings: ${GREEN}N${NC}"
    echo
    
    vercel --prod
    
    cd ..
}

# Update GPU server CORS
update_gpu_cors() {
    log_info "Creating CORS configuration for GPU server..."
    
    cat > enable-cors.sh << 'EOF'
#!/bin/bash
# Run this on the GPU server to enable CORS for Vercel

# Add CORS headers to Think AI HTTP server
# This allows the Vercel frontend to communicate with GPU backend

echo "Enabling CORS for Vercel deployment..."

# Find your Vercel URL after deployment and update this
VERCEL_URL="https://think-ai-webapp.vercel.app"

# Add to your Think AI startup script or environment
export THINK_AI_CORS_ORIGIN="$VERCEL_URL"
export THINK_AI_CORS_ENABLED=true

echo "CORS enabled for: $VERCEL_URL"
echo "Restart Think AI services for changes to take effect"
EOF
    
    chmod +x enable-cors.sh
    
    log_info "Created enable-cors.sh - run this on your GPU server after deployment"
}

# Main execution
main() {
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}    Think AI Vercel Deployment (Frontend Only)${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo
    echo -e "Architecture:"
    echo -e "  ${BLUE}Frontend${NC}: Vercel (Global CDN)"
    echo -e "  ${BLUE}Backend${NC}: GPU Server (${GPU_SERVER_URL})"
    echo
    
    # Prepare and deploy
    prepare_vercel_deployment
    deploy_to_vercel
    update_gpu_cors
    
    echo
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Deployment complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo
    echo -e "Next steps:"
    echo -e "1. Note your Vercel URL (shown above)"
    echo -e "2. On GPU server, run: ${YELLOW}./enable-cors.sh${NC}"
    echo -e "3. Update VERCEL_URL in enable-cors.sh with your actual URL"
    echo -e "4. Restart Think AI services on GPU server"
    echo
    echo -e "${BLUE}Your architecture:${NC}"
    echo -e "┌─────────────┐     ┌──────────────┐"
    echo -e "│   Vercel    │────▶│  GPU Server  │"
    echo -e "│  (Frontend) │     │  (Backend)   │"
    echo -e "│     CDN     │     │ O(1) Engine  │"
    echo -e "└─────────────┘     └──────────────┘"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi