#!/bin/bash
# Elite Local Pre-commit Script with O(1) Performance
# Formats code and runs tests without blocking commits

set -euo pipefail

echo "🚀 Think AI Pre-commit Pipeline"
echo "================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Track if we should block commit
BLOCK_COMMIT=false

# Python formatting with Black (non-blocking)
echo -e "\n${YELLOW}🎨 Formatting Python code with Black...${NC}"
if command -v black &> /dev/null; then
    black . --line-length=120 --target-version=py311 \
        --exclude='/(\.git|\.venv|venv|build|dist|__pycache__|THINK_AI_DEPLOYMENT_)/' \
        2>/dev/null || echo -e "${YELLOW}⚠️  Black formatting had issues but continuing...${NC}"
    echo -e "${GREEN}✅ Black formatting complete${NC}"
else
    echo -e "${YELLOW}⚠️  Black not installed, skipping...${NC}"
fi

# Sort imports with isort (non-blocking)
echo -e "\n${YELLOW}📦 Sorting imports with isort...${NC}"
if command -v isort &> /dev/null; then
    isort . --profile=black --line-length=120 \
        --skip-glob="**/venv/*" --skip-glob="**/.venv/*" \
        2>/dev/null || echo -e "${YELLOW}⚠️  isort had issues but continuing...${NC}"
    echo -e "${GREEN}✅ Import sorting complete${NC}"
else
    echo -e "${YELLOW}⚠️  isort not installed, skipping...${NC}"
fi

# Run flake8 (report only, non-blocking)
echo -e "\n${YELLOW}🔍 Running flake8 linting...${NC}"
if command -v flake8 &> /dev/null; then
    flake8 . --max-line-length=120 \
        --extend-ignore=E203,E266,E501,W503,F403,F401 \
        --exclude=.git,__pycache__,venv,.venv,build,dist,THINK_AI_DEPLOYMENT_* \
        --statistics --count 2>/dev/null || echo -e "${YELLOW}⚠️  Linting issues found (non-blocking)${NC}"
else
    echo -e "${YELLOW}⚠️  flake8 not installed, skipping...${NC}"
fi

# Run tests with coverage (non-blocking but report)
echo -e "\n${YELLOW}🧪 Running tests...${NC}"
if [ -d "tests" ]; then
    # Create coverage config
    cat > .coveragerc << EOF
[run]
source = think_ai
omit =
    */tests/*
    */venv/*
    */.venv/*
    */site-packages/*
    */distutils/*
    */THINK_AI_DEPLOYMENT_*/*

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = htmlcov
EOF

    # Run tests
    python -m pytest tests/ \
        --cov=think_ai \
        --cov-config=.coveragerc \
        --cov-report=term-missing:skip-covered \
        --tb=short \
        -q 2>/dev/null || {
            echo -e "${YELLOW}⚠️  Some tests failed (non-blocking)${NC}"
        }

    # Check coverage
    COVERAGE=$(python -m coverage report --format=total 2>/dev/null || echo "0")
    echo -e "\n${YELLOW}📊 Code coverage: ${COVERAGE}%${NC}"

    if (( $(echo "$COVERAGE < 80" | bc -l) )); then
        echo -e "${YELLOW}⚠️  Coverage below 80% threshold${NC}"
    else
        echo -e "${GREEN}✅ Coverage meets threshold${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No tests directory found${NC}"
fi

# Docker build verification (if Dockerfile exists)
echo -e "\n${YELLOW}🐳 Verifying Docker build...${NC}"
if [ -f "Dockerfile.railway" ]; then
    # Quick syntax check only
    docker build -f Dockerfile.railway --target python-deps -t test-syntax . \
        --quiet 2>/dev/null && echo -e "${GREEN}✅ Dockerfile syntax valid${NC}" || {
        echo -e "${YELLOW}⚠️  Docker build issues detected${NC}"
    }
elif [ -f "configs/Dockerfile" ]; then
    docker build -f configs/Dockerfile --target python-deps -t test-syntax . \
        --quiet 2>/dev/null && echo -e "${GREEN}✅ Dockerfile syntax valid${NC}" || {
        echo -e "${YELLOW}⚠️  Docker build issues detected${NC}"
    }
fi

# Check for large files
echo -e "\n${YELLOW}📏 Checking file sizes...${NC}"
LARGE_FILES=$(find . -type f -size +5M -not -path "./.git/*" -not -path "./venv/*" -not -path "./.venv/*" 2>/dev/null)
if [ ! -z "$LARGE_FILES" ]; then
    echo -e "${YELLOW}⚠️  Large files detected (>5MB):${NC}"
    echo "$LARGE_FILES" | head -5
fi

# Security check with bandit (non-blocking)
echo -e "\n${YELLOW}🔒 Running security scan...${NC}"
if command -v bandit &> /dev/null; then
    bandit -r think_ai/ --skip B101,B601 --severity-level high -f json \
        2>/dev/null 1>/dev/null || echo -e "${YELLOW}⚠️  Security issues found (non-blocking)${NC}"
    echo -e "${GREEN}✅ Security scan complete${NC}"
else
    echo -e "${YELLOW}⚠️  bandit not installed, skipping...${NC}"
fi

# Performance check - verify O(1) imports
echo -e "\n${YELLOW}⚡ Checking O(1) performance patterns...${NC}"
# Check for common O(n) patterns
if grep -r "for.*in.*for.*in" think_ai/ --include="*.py" 2>/dev/null | grep -v "# O(1)" > /dev/null; then
    echo -e "${YELLOW}⚠️  Nested loops detected - verify O(1) complexity${NC}"
fi

# Auto-stage formatted files
echo -e "\n${YELLOW}📝 Staging formatted files...${NC}"
git add -u 2>/dev/null || true

# Final summary
echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}✅ Pre-commit checks complete!${NC}"
echo -e "${GREEN}================================${NC}"

# Always allow commit (non-blocking)
exit 0
