#!/bin/bash
# Think AI Quick Commit - Shorthand version of commit.sh
# Usage: ./c.sh "commit message" [options]

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

# Check if commit message was provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Please provide a commit message${NC}"
    echo -e "${BLUE}Usage:${NC}"
    echo "  ./c.sh \"your commit message\"       # Run full pipeline and commit"
    echo "  ./c.sh \"your commit message\" --fast # Skip some checks for faster commit"
    echo "  ./c.sh \"your commit message\" --ci   # Run in CI mode (no interactive)"
    exit 1
fi

COMMIT_MSG="$1"
FAST_MODE=false
CI_MODE=""

# Parse options
if [ "$2" = "--fast" ]; then
    FAST_MODE=true
    echo -e "${YELLOW}⚡ Fast mode enabled - skipping some checks${NC}"
elif [ "$2" = "--ci" ]; then
    CI_MODE="--no-interactive"
    echo -e "${BLUE}🤖 CI mode enabled${NC}"
fi

echo -e "${BLUE}🚀 Running Think AI Pipeline...${NC}"
echo ""

# For fast mode, just run basic checks
if [ "$FAST_MODE" = true ]; then
    echo -e "${BLUE}Running quick checks...${NC}"
    
    # Just syntax check
    if ruff check think_ai/ --select=E999 --quiet; then
        echo -e "${GREEN}✓ Syntax check passed${NC}"
    else
        echo -e "${RED}✗ Syntax errors found!${NC}"
        exit 1
    fi
    
    # Quick import test
    if python3 -c "import think_ai" 2>/dev/null; then
        echo -e "${GREEN}✓ Import check passed${NC}"
    else
        echo -e "${RED}✗ Import failed!${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Quick checks passed!${NC}"
else
    # Run full pipeline with progress bar
    if CI="" ./scripts/ultra-fast-precommit.sh $CI_MODE; then
        echo -e "${GREEN}✅ All pipeline checks passed!${NC}"
    else
        echo -e "${RED}❌ Pipeline failed! Fix the issues and try again.${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}📝 Committing: ${NC}$COMMIT_MSG"

# Commit with no-verify to skip pre-commit hooks
git commit -m "$COMMIT_MSG" --no-verify

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Successfully committed!${NC}"
    echo -e "${BLUE}💡 Use 'git push' to push your changes${NC}"
    
    # Show what was committed
    echo ""
    git log --oneline -1
else
    echo -e "${RED}❌ Commit failed${NC}"
    exit 1
fi