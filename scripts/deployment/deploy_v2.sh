#!/bin/bash
# Deploy Think AI v2.0.0 to PyPI and npm

set -e

echo "🚀 Think AI v2.0.0 Deployment Script"
echo "===================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're on main branch
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ]; then
    echo -e "${RED}❌ Must be on main branch to deploy${NC}"
    exit 1
fi

# Check if everything is committed
if [[ -n $(git status -s) ]]; then
    echo -e "${RED}❌ Uncommitted changes detected${NC}"
    git status -s
    exit 1
fi

echo -e "${BLUE}📦 Preparing Python package...${NC}"

# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build Python package
python setup.py sdist bdist_wheel

echo -e "${GREEN}✅ Python package built${NC}"
echo ""

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo -e "${BLUE}Installing twine...${NC}"
    pip install twine
fi

echo -e "${BLUE}📤 Uploading to PyPI...${NC}"
echo "Note: You'll need your PyPI credentials"
echo ""

# Upload to PyPI (will prompt for credentials)
twine upload dist/*

echo -e "${GREEN}✅ Python package deployed to PyPI${NC}"
echo ""

# Build TypeScript/JavaScript
if [ -d "src" ] && [ -f "tsconfig.json" ]; then
    echo -e "${BLUE}📦 Building TypeScript package...${NC}"
    npm run build
    
    echo -e "${BLUE}📤 Publishing to npm...${NC}"
    echo "Note: You'll need to be logged in to npm"
    echo ""
    
    # Publish to npm
    npm publish
    
    echo -e "${GREEN}✅ JavaScript package deployed to npm${NC}"
else
    echo -e "${BLUE}ℹ️  No TypeScript source found, skipping npm deployment${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Deployment complete!${NC}"
echo ""
echo "Installation commands:"
echo "  Python: pip install think-ai-consciousness==2.0.0"
echo "  Node.js: npm install think-ai-js@2.0.0"
echo ""
echo "GitHub release:"
echo "  Create release at: https://github.com/champi-dev/think_ai/releases/new"
echo "  Tag: v2.0.0"
echo "  Title: Think AI v2.0.0 - The Exponential Evolution"