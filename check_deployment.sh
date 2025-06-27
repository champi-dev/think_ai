#\!/bin/bash

echo "🔍 Railway Deployment Checker"
echo "============================"

echo ""
echo "📊 Current Status:"
railway status

echo ""
echo "🚀 Getting deployment info:"
railway service

echo ""  
echo "📋 Service variables:"
railway variables

echo ""
echo "🌐 Domain info:"
railway domain

echo ""
echo "💡 If deployment failed, common fixes:"
echo "1. Check Railway dashboard for detailed logs"
echo "2. Verify PORT environment variable is set"
echo "3. Ensure binary starts correctly with ./full-server"
echo "4. Check memory/CPU limits in Railway dashboard"


