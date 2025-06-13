#!/bin/bash
# Think AI Local CI/CD Runner - Format Only Mode
# Automatically formats all Python files without blocking

echo "🚀 Think AI Auto-Formatter"
echo "========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "\n${YELLOW}🐍 Activating virtual environment...${NC}"
source venv/bin/activate

# Install formatting tools
echo -e "\n${YELLOW}📦 Installing formatting tools...${NC}"
pip install --upgrade pip wheel setuptools
pip install autopep8 black isort

# Format all Python files
echo -e "\n${YELLOW}🎨 Formatting Python files...${NC}"

# Run isort for import sorting
echo "  → Sorting imports with isort..."
isort think_ai/ --quiet

# Run black for code formatting
echo "  → Formatting with black..."
black think_ai/ --quiet 2>/dev/null || true

# Run autopep8 for additional PEP8 compliance
echo "  → Applying PEP8 with autopep8..."
find think_ai/ -name "*.py" -type f -exec autopep8 --in-place --aggressive --aggressive {} \; 2>/dev/null || true

# Add any changed files to git
echo -e "\n${YELLOW}📝 Adding formatted files to git...${NC}"
git add -A

# Show what was changed
CHANGED_FILES=$(git diff --cached --name-only | grep -E '\.py$' | wc -l)
if [ $CHANGED_FILES -gt 0 ]; then
    echo -e "${GREEN}✅ Formatted $CHANGED_FILES Python files${NC}"
    echo -e "\nFormatted files:"
    git diff --cached --name-only | grep -E '\.py$' | head -20
    if [ $CHANGED_FILES -gt 20 ]; then
        echo "  ... and $((CHANGED_FILES - 20)) more"
    fi
else
    echo -e "${GREEN}✅ All files already properly formatted${NC}"
fi

# Auto-deploy
echo -e "\n${YELLOW}🚀 Starting auto-deployment...${NC}"
python scripts/auto_deploy.py
DEPLOY_EXIT=$?

if [ $DEPLOY_EXIT -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
else
    echo -e "${YELLOW}⚠️  Deployment failed - check credentials${NC}"
fi

echo -e "\n${GREEN}🎉 Formatting complete! Proceeding with push...${NC}"
exit 0