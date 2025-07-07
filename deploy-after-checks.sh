#!/bin/bash
# Deploy libraries after successful pre-commit checks

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Think AI Post-Check Deployment${NC}"
echo "=================================="
echo ""

# Check if pre-commit passed
if [ "$1" != "--force" ]; then
    echo "Running pre-commit checks first..."
    if ! .git/hooks/pre-commit; then
        echo ""
        echo "❌ Pre-commit checks failed!"
        echo "Fix the issues or run with --force to skip checks"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}📦 Deploying Libraries${NC}"
echo "---------------------"

# Deploy Python package
if [ -n "$PYPI_TOKEN" ]; then
    echo ""
    echo "🐍 Deploying to PyPI..."
    cd think-ai-py
    python3 -m twine upload dist/* -u __token__ -p "$PYPI_TOKEN"
    cd ..
    echo -e "${GREEN}✓ Python package deployed${NC}"
else
    echo "⚠️  Skipping PyPI deployment (no PYPI_TOKEN set)"
fi

# Deploy npm package  
if [ -n "$NPM_TOKEN" ]; then
    echo ""
    echo "📦 Deploying to npm..."
    cd think-ai-js
    npm config set //registry.npmjs.org/:_authToken "$NPM_TOKEN"
    npm publish --access public
    cd ..
    echo -e "${GREEN}✓ JavaScript package deployed${NC}"
else
    echo "⚠️  Skipping npm deployment (no NPM_TOKEN set)"
fi

# Push to git
echo ""
echo -e "${BLUE}📤 Pushing to Git${NC}"
echo "-----------------"
git push

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📊 Verify deployments:"
echo "  - npm: https://www.npmjs.com/package/thinkai-quantum"
echo "  - PyPI: https://pypi.org/project/thinkai-quantum/"
echo "  - Railway: https://thinkai-production.up.railway.app"