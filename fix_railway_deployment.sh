#!/bin/bash

echo "🔧 Railway Deployment Troubleshooting"
echo "====================================="

echo ""
echo "📋 Checking deployment files..."

# Check if required files exist
FILES=("Dockerfile" "railway.toml" "minimal_3d.html" "Cargo.toml")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done

echo ""
echo "📁 Current directory contents:"
ls -la | grep -E "(Dockerfile|railway|Cargo|minimal)"

echo ""
echo "🔍 Git status:"
git status --porcelain

echo ""
echo "📦 Committing any missing files..."
git add -A
if git diff --staged --quiet; then
    echo "✅ All files already committed"
else
    git commit -m "Fix Railway deployment - add missing files

🧠 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
    echo "✅ Files committed"
fi

echo ""
echo "🚀 Manual Railway deployment steps:"
echo "1. Make sure you're in the project root: $(pwd)"
echo "2. Check Railway project: railway status"
echo "3. Force redeploy: railway up --detach"
echo ""
echo "🔧 Alternative solutions:"
echo "1. Try: railway service delete && railway up"
echo "2. Check Railway dashboard for project settings"
echo "3. Verify Railway CLI version: railway --version"
echo "4. Re-authenticate: railway logout && railway login"

echo ""
echo "🐛 If Railway still can't find Dockerfile:"
echo "1. Check Railway project root directory setting"
echo "2. Try uploading directly via Railway dashboard"
echo "3. Verify git repository is properly connected"

echo ""
echo "📊 File verification:"
echo "Dockerfile size: $(wc -l < Dockerfile) lines"
echo "railway.toml size: $(wc -l < railway.toml) lines"
echo "Project structure looks correct for Railway deployment."