#!/bin/bash

echo "🔍 Think AI Railway Deployment Status"
echo "=========================================="
echo ""

echo "📊 Project Status:"
railway status

echo ""
echo "🌐 Domain:"
railway domain

echo ""
echo "📝 Variables:"
railway variables

echo ""
echo "🔍 Testing endpoints:"
echo "Health: $(curl -s -o /dev/null -w "%{http_code}" https://thinkai-production.up.railway.app/health)"
echo "Root:   $(curl -s -o /dev/null -w "%{http_code}" https://thinkai-production.up.railway.app/)"

echo ""
echo "📋 Build logs URL:"
echo "https://railway.com/project/12a27f0b-34ce-4e42-b0b0-94c09f13ff80/service/400d0d36-23ce-48a3-a74a-2e5c80c0eb52"

echo ""
echo "💡 Next steps:"
echo "1. Check build logs in Railway dashboard"
echo "2. Verify nixpacks.toml configuration"
echo "3. Ensure all dependencies compile correctly"