#!/bin/bash

echo "🔍 Railway Deployment Status Check"
echo "==================================="

echo ""
echo "📋 Current Status:"
railway status

echo ""
echo "🌐 App URL:"
echo "https://thinkai-production.up.railway.app"

echo ""
echo "🔗 Build Logs:"
echo "https://railway.com/project/12a27f0b-34ce-4e42-b0b0-94c09f13ff80/service/400d0d36-23ce-48a3-a74a-2e5c80c0eb52"

echo ""
echo "🧪 Testing deployment once ready..."
sleep 5

# Test if the deployment is ready
echo "Testing health endpoint..."
if curl -s -o /dev/null -w "%{http_code}" https://thinkai-production.up.railway.app/health | grep -q "200"; then
    echo "✅ Deployment is LIVE and healthy!"
    echo "🎉 Your Think AI app is working at:"
    echo "https://thinkai-production.up.railway.app"
else
    echo "⏳ Deployment still building... check back in a few minutes"
    echo "📊 Monitor progress at:"
    echo "https://railway.app/project/12a27f0b-34ce-4e42-b0b0-94c09f13ff80"
fi

echo ""
echo "🎯 What's deployed:"
echo "• ✨ Clean UI with 3D quantum animation"
echo "• ⚡ O(1) performance optimizations"
echo "• 🧠 Hierarchical knowledge system"
echo "• 📱 Responsive design"

echo ""
echo "🔄 To check deployment logs:"
echo "railway logs"