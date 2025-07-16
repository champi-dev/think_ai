#!/bin/bash

echo "🚀 Railway CLI Alternative Fix"
echo "=============================="

echo ""
echo "🔍 Diagnosing Railway CLI issue..."

# Check Railway CLI version
if command -v railway &> /dev/null; then
    echo "Railway CLI version: $(railway --version)"
else
    echo "❌ Railway CLI not found"
    exit 1
fi

# Check current directory
echo "Current directory: $(pwd)"
echo "Dockerfile exists: $([ -f Dockerfile ] && echo "✅ YES" || echo "❌ NO")"

echo ""
echo "🔧 Trying Railway CLI fixes..."

# Method 1: Specify Dockerfile explicitly
echo "1️⃣ Trying explicit Dockerfile path..."
railway up --dockerfile ./Dockerfile

if [ $? -eq 0 ]; then
    echo "✅ Success with explicit Dockerfile path!"
    exit 0
fi

echo ""
echo "2️⃣ Trying with service creation..."
railway service create --name think-ai-app
railway up

if [ $? -eq 0 ]; then
    echo "✅ Success with service creation!"
    exit 0
fi

echo ""
echo "3️⃣ Trying environment reset..."
railway logout
echo "Please login again:"
railway login
railway up

if [ $? -eq 0 ]; then
    echo "✅ Success after re-authentication!"
    exit 0
fi

echo ""
echo "❌ Railway CLI methods failed."
echo ""
echo "🌐 Try Railway Web Interface instead:"
echo "1. Go to https://railway.app/dashboard"
echo "2. Click 'New Project'"
echo "3. Select 'Deploy from GitHub repo'"
echo "4. Choose your think_ai repository"
echo ""
echo "🚁 Or try Fly.io alternative:"
echo "./try_fly_deploy.sh"