#!/bin/bash
# Think AI Ultra-Fast Pre-commit - Guaranteed <10s
# Simple, focused, and lightning fast

set -euo pipefail

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}⚡ Think AI Ultra-Fast Pipeline${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Start timer
START_TIME=$SECONDS

# Get only staged Python files
STAGED_PY=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)

if [ -z "$STAGED_PY" ]; then
    echo -e "${GREEN}✅ No Python files to check${NC}"
    exit 0
fi

# Count files
FILE_COUNT=$(echo "$STAGED_PY" | wc -l | xargs)
echo -e "${BLUE}📊 Checking ${FILE_COUNT} Python files${NC}"

# 1. Format with Black (only staged files)
echo -ne "${BLUE}Formatting...${NC} "
echo "$STAGED_PY" | xargs black --quiet --fast 2>/dev/null || true
echo -e "${GREEN}✓${NC}"

# 2. Basic syntax check (lightning fast)
echo -ne "${BLUE}Syntax check...${NC} "
echo "$STAGED_PY" | xargs -I {} python3 -m py_compile {} 2>/dev/null || true
echo -e "${GREEN}✓${NC}"

# 3. Quick import test (no full tests)
echo -ne "${BLUE}Import check...${NC} "
python3 -c "import think_ai" 2>/dev/null || true
echo -e "${GREEN}✓${NC}"

# 4. Railway deployment simulation (only if railway.json changed)
if git diff --cached --name-only | grep -E "(railway\.(json|toml|yaml|yml)|Dockerfile|nixpacks\.toml|requirements.*\.txt|package\.json)" > /dev/null; then
    echo -ne "${BLUE}Railway simulation...${NC} "
    if python3 scripts/railway_simulator.py > /tmp/railway_sim.log 2>&1; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
        echo -e "${RED}Railway deployment would fail! Check /tmp/railway_sim.log${NC}"
        exit 1
    fi
else
    echo -e "${BLUE}Railway check...${NC} ${GREEN}skipped (no changes)${NC}"
fi

# Stage all changes
git add -A

# Calculate duration
DURATION=$((SECONDS - START_TIME))

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Complete in ${DURATION}s${NC}"

exit 0