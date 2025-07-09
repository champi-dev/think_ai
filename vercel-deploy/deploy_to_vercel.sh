#!/bin/bash

echo "🚀 Deploying Think AI 3D webapp to Vercel..."
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Please install it first:"
    echo "   npm install -g vercel"
    echo ""
    echo "Or use npx:"
    echo "   npx vercel"
    exit 1
fi

# Change to the deployment directory
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"
echo ""
echo "📋 Files to deploy:"
ls -la
echo ""

echo "🌐 Starting Vercel deployment..."
echo "   - No server dependencies"
echo "   - Pure client-side 3D visualization"
echo "   - Canvas-based particle system"
echo "   - PWA support included"
echo ""

# Deploy to Vercel
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🎉 Your 3D webapp is now live on Vercel!"
echo "   - No 502 errors (no server dependencies)"
echo "   - Instant responses with simulated AI chat"
echo "   - Beautiful 3D quantum particle visualization"