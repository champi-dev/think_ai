#!/bin/bash
set -e

echo "🚀 Deploying Think AI to Railway..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "npm install -g @railway/cli"
    exit 1
fi

# Clean up any previous failed builds
echo "🧹 Cleaning up..."
rm -rf target/release/*.d
rm -rf target/debug

# Create a .railwayignore file to exclude unnecessary files
cat > .railwayignore << EOF
target/debug
target/release/*.d
*.log
*.tmp
docs/
scripts/
knowledge-enhancement/
think-ai-knowledge/
think-ai-image-gen/
EOF

# Update server to use PORT environment variable
echo "📝 Ensuring server uses PORT env var..."
if ! grep -q "PORT" think-ai-cli/src/main.rs; then
    echo "⚠️  Warning: Make sure your server listens on \$PORT environment variable"
fi

# Deploy to Railway
echo "🚂 Deploying to Railway..."
railway up

echo "
✅ Deployment initiated!

Railway will:
1. Build your Rust project
2. Create a Docker container
3. Deploy it with automatic HTTPS
4. Provide you with a URL

Monitor the build at: https://railway.app/dashboard

If deployment fails, try:
1. Check build logs in Railway dashboard
2. Ensure all dependencies compile with Rust 1.82
3. Use 'railway logs' to debug runtime issues
"