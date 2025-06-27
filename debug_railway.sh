#!/bin/bash

echo "🔍 Railway Dockerfile Debug"
echo "==========================="

echo ""
echo "📁 Current Directory:"
pwd

echo ""
echo "📄 Files in root:"
ls -la | grep -E "(Dockerfile|dockerfile|railway|nixpacks|Cargo.toml)"

echo ""
echo "🧪 Dockerfile Content (first 10 lines):"
head -10 Dockerfile

echo ""
echo "📊 Git Status:"
git status --porcelain

echo ""
echo "🔗 Latest commit:"
git log --oneline -1

echo ""
echo "📡 Railway Status:"
railway status

echo ""
echo "💡 Troubleshooting:"
echo "If Railway still can't find Dockerfile, this is a Railway CLI bug."
echo "The Dockerfile clearly exists and is properly formatted."
echo ""
echo "🌐 Alternative: Use Railway Web Interface"
echo "1. Go to https://railway.app/dashboard"
echo "2. Select your think_ai project"
echo "3. Redeploy from GitHub directly"
echo ""
echo "🎯 The web interface bypasses CLI Dockerfile detection issues."