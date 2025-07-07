#!/bin/bash
# Redeploy Think AI Libraries (npm and PyPI)

set -e

echo "🚀 Think AI Library Redeployment"
echo "================================"
echo ""

# Check current versions
echo "📊 Current versions:"
if [ -f "think-ai-js/package.json" ]; then
    echo "   npm: v$(node -p "require('./think-ai-js/package.json').version")"
fi
if [ -f "think-ai-py/pyproject.toml" ]; then
    echo "   PyPI: v$(grep "version = " think-ai-py/pyproject.toml | sed 's/version = "\(.*\)"/\1/')"
fi
echo ""

# Check for tokens
if [ -z "$NPM_TOKEN" ]; then
    echo "⚠️  NPM_TOKEN not set. To deploy to npm:"
    echo "   1. Get your token from https://www.npmjs.com/settings/USERNAME/tokens"
    echo "   2. Export it: export NPM_TOKEN=your-token-here"
    echo ""
fi

if [ -z "$PYPI_TOKEN" ]; then
    echo "⚠️  PYPI_TOKEN not set. To deploy to PyPI:"
    echo "   1. Get your token from https://pypi.org/manage/account/token/"
    echo "   2. Export it: export PYPI_TOKEN=your-token-here"
    echo ""
fi

# Manual deployment instructions
echo "📝 Manual Deployment Instructions:"
echo ""
echo "1️⃣  Deploy npm package:"
echo "   cd think-ai-js"
echo "   # Update version in package.json"
echo "   npm run build"
echo "   npm test"
echo "   npm login  # if not logged in"
echo "   npm publish --access public"
echo ""
echo "2️⃣  Deploy PyPI package:"
echo "   cd think-ai-py"
echo "   # Update version in pyproject.toml"
echo "   rm -rf dist/ build/"
echo "   python3 -m build"
echo "   python3 -m pytest tests/ -v"
echo "   python3 -m twine upload dist/*"
echo ""
echo "3️⃣  Test installations:"
echo "   # Test npm"
echo "   npx thinkai-quantum@latest --version"
echo "   # Test PyPI"
echo "   pip install --upgrade thinkai-quantum"
echo "   think-ai --version"
echo ""

# Automated deployment if tokens are available
if [ -n "$NPM_TOKEN" ] && [ -n "$PYPI_TOKEN" ]; then
    echo "✅ Both tokens found! Starting automated deployment..."
    echo ""
    
    # Run the full deployment script
    if [ -f "scripts/deploy-all-libs.sh" ]; then
        chmod +x scripts/deploy-all-libs.sh
        ./scripts/deploy-all-libs.sh
    else
        echo "❌ Deployment script not found at scripts/deploy-all-libs.sh"
        exit 1
    fi
else
    echo "ℹ️  Set both NPM_TOKEN and PYPI_TOKEN environment variables to enable automated deployment."
fi