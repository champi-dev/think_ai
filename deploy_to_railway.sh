#!/bin/bash

echo "🚀 Deploying Think AI to Railway"
echo "================================"

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    curl -fsSL https://railway.app/install.sh | sh
    echo "✅ Railway CLI installed"
fi

echo ""
echo "📋 Pre-deployment Checklist:"
echo "=============================="

# Check if Dockerfile exists
if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile found"
else
    echo "❌ Dockerfile missing"
    exit 1
fi

# Check if railway.toml exists
if [ -f "railway.toml" ]; then
    echo "✅ railway.toml found"
else
    echo "❌ railway.toml missing"
    exit 1
fi

# Check if minimal_3d.html exists
if [ -f "minimal_3d.html" ]; then
    echo "✅ minimal_3d.html found"
else
    echo "❌ minimal_3d.html missing"
    exit 1
fi

# Check if knowledge data exists
if [ -d "think-ai-knowledge/data" ]; then
    echo "✅ Knowledge data directory found"
else
    echo "❌ Knowledge data directory missing"
    exit 1
fi

# Check if we can build locally first
echo ""
echo "🔨 Testing local build:"
echo "======================="
if cargo build --release --bin full-server; then
    echo "✅ Local build successful"
else
    echo "❌ Local build failed"
    exit 1
fi

echo ""
echo "🚀 Deploying to Railway:"
echo "========================"

# Login to Railway (if not already logged in)
echo "📝 Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway:"
    railway login
fi

# Deploy the project
echo "🚀 Starting deployment..."
railway up

echo ""
echo "✅ Deployment initiated!"
echo "========================"
echo ""
echo "📊 Monitor your deployment:"
echo "• Run 'railway status' to check deployment status"
echo "• Run 'railway logs' to view deployment logs"
echo "• Run 'railway domain' to get your app URL"
echo ""
echo "🌐 Your Think AI app will be available at:"
echo "https://your-app-name.railway.app"
echo ""
echo "🔍 Health check endpoint:"
echo "https://your-app-name.railway.app/health"