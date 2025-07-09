#!/bin/bash
set -e

echo "🚀 Deployment Checklist for Think AI with Ollama on Railway"
echo "============================================================"

# Check prerequisites
echo "📋 Checking prerequisites..."

# 1. Check if railway.toml exists (should not)
if [ -f "railway.toml" ]; then
    echo "⚠️ railway.toml found - this will prevent Docker usage!"
    echo "   Run: mv railway.toml railway.toml.backup"
    exit 1
else
    echo "✅ No railway.toml - Docker will be used"
fi

# 2. Check Dockerfile
if [ -f "Dockerfile.railway" ]; then
    echo "✅ Dockerfile.railway exists"
elif [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile exists"
else
    echo "❌ No Dockerfile found!"
    exit 1
fi

# 3. Check if .railway/config.json exists
if [ -f ".railway/config.json" ]; then
    echo "✅ Railway config found"
else
    echo "⚠️ No .railway/config.json - using defaults"
fi

echo ""
echo "📝 Deployment Instructions:"
echo "1. Ensure you're logged into Railway CLI: railway login"
echo "2. Select your project: railway link"
echo "3. Deploy with: railway up"
echo ""
echo "🔍 Monitor deployment:"
echo "   - Watch logs: railway logs"
echo "   - Check deployment status in Railway dashboard"
echo ""
echo "⏱️ Expected deployment timeline:"
echo "   - Build: 3-5 minutes"
echo "   - Ollama startup: 1-2 minutes"
echo "   - Qwen model download: 2-3 minutes"
echo "   - Total: ~10 minutes"
echo ""
echo "🧪 After deployment, test with:"
echo '   curl -X POST https://YOUR-APP.railway.app/chat \'
echo '     -H "Content-Type: application/json" \'
echo '     -d '"'"'{"query": "What is the universe?"}'"'"''
echo ""
echo "💡 Tips:"
echo "   - Ensure you have sufficient resources (not on free tier)"
echo "   - Monitor memory usage - Qwen 1.5B needs ~2GB RAM"
echo "   - Check Ollama logs if model fails to load"
echo ""
echo "Ready to deploy? Run: railway up"