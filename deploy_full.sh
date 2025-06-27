#!/bin/bash

echo "🚀 Think AI Full Deployment Strategy"
echo "===================================="

# Strategy 1: Try nixpacks with optimizations
echo "📦 Strategy 1: Optimized nixpacks..."
echo "Current nixpacks.toml includes:"
echo "- Limited build jobs (--jobs 2)"  
echo "- Required system packages"
echo "- Build optimizations"

# Wait for current build
echo ""
echo "⏳ Waiting for current build..."
sleep 30

# Test deployment
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai-production.up.railway.app/health)
echo "Health endpoint status: $HEALTH_STATUS"

if [ "$HEALTH_STATUS" = "200" ]; then
    echo "✅ Deployment successful!"
    curl -s https://thinkai-production.up.railway.app/health | jq '.'
    exit 0
fi

echo ""
echo "🔄 Strategy 2: If nixpacks fails, trying Docker..."
echo "Moving optimized Dockerfile into place..."

if [ -f "Dockerfile.optimized" ]; then
    # Backup current approach
    mv nixpacks.toml nixpacks.toml.backup 2>/dev/null || true
    
    # Use optimized Docker
    mv Dockerfile.optimized Dockerfile
    
    echo "🐳 Deploying with optimized Docker..."
    railway up
    
    echo "⏳ Waiting for Docker build..."
    sleep 60
    
    HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai-production.up.railway.app/health)
    echo "Health endpoint status: $HEALTH_STATUS"
    
    if [ "$HEALTH_STATUS" = "200" ]; then
        echo "✅ Docker deployment successful!"
        curl -s https://thinkai-production.up.railway.app/health | jq '.'
    else
        echo "⚠️  Still building or needs debugging..."
        echo "Check Railway dashboard for detailed build logs."
    fi
fi

echo ""
echo "🌐 Railway URL: https://thinkai-production.up.railway.app"
echo "📊 Dashboard: https://railway.com/project/12a27f0b-34ce-4e42-b0b0-94c09f13ff80"
echo ""
echo "💡 All strategies deploy the FULL Think AI system with:"
echo "   - Complete knowledge engine"
echo "   - O(1) vector search"  
echo "   - TinyLlama integration"
echo "   - 3D consciousness webapp"
echo "   - All API endpoints"