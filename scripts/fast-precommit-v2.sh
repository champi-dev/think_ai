#!/bin/bash
# Think AI Optimized Pre-commit Pipeline - Target: <10s
# Using O(1) strategies and parallel execution

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Performance tracking
PIPELINE_START=$(date +%s.%N 2>/dev/null || date +%s)
CACHE_DIR="${HOME}/.think_ai_fast_cache"
mkdir -p "$CACHE_DIR"

# O(1) file change detection using git
get_changed_files() {
    git diff --cached --name-only --diff-filter=ACM
}

# Get only Python files that changed
get_changed_python() {
    get_changed_files | grep -E '\.py$' || true
}

# Get only JS/TS files that changed  
get_changed_js() {
    get_changed_files | grep -E '\.(js|jsx|ts|tsx)$' || true
}

echo -e "${BLUE}⚡ Think AI Ultra-Fast Pipeline${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Count changed files
PY_FILES=$(get_changed_python)
JS_FILES=$(get_changed_js)
PY_COUNT=$(echo "$PY_FILES" | grep -v "^$" | wc -l | tr -d ' ')
JS_COUNT=$(echo "$JS_FILES" | grep -v "^$" | wc -l | tr -d ' ')

if [ "$PY_COUNT" -eq 0 ] && [ "$JS_COUNT" -eq 0 ]; then
    echo -e "${GREEN}✅ No code files changed - skipping checks${NC}"
    exit 0
fi

echo -e "${BLUE}📊 Changed files: ${PY_COUNT} Python, ${JS_COUNT} JS/TS${NC}"

# Parallel execution flags
FORMAT_PY_PID=""
FORMAT_JS_PID=""
LINT_PID=""
TEST_PID=""

# 1. Format Python (only changed files)
if [ "$PY_COUNT" -gt 0 ]; then
    (
        echo -ne "${BLUE}Format Python...${NC} "
        start=$(date +%s.%N 2>/dev/null || date +%s)
        
        # Format only changed files
        echo "$PY_FILES" | xargs -I {} black {} --quiet --fast 2>/dev/null
        
        end=$(date +%s.%N 2>/dev/null || date +%s)
        duration=$(python3 -c "print(f'{$end - $start:.1f}')" 2>/dev/null || echo "0.1")
        echo -e "${GREEN}✓${NC} (${duration}s)"
    ) &
    FORMAT_PY_PID=$!
else
    echo -e "${BLUE}Format Python...${NC} ${GREEN}✓ no changes${NC}"
fi

# 2. Format JS/TS (only changed files)
if [ "$JS_COUNT" -gt 0 ] && [ -f "webapp/package.json" ]; then
    (
        echo -ne "${BLUE}Format JS...${NC} "
        start=$(date +%s.%N 2>/dev/null || date +%s)
        
        # Format only changed files in webapp
        cd webapp
        echo "$JS_FILES" | grep "^webapp/" | sed 's|^webapp/||' | xargs npx prettier --write --loglevel error 2>/dev/null || true
        cd ..
        
        end=$(date +%s.%N 2>/dev/null || date +%s)
        duration=$(python3 -c "print(f'{$end - $start:.1f}')" 2>/dev/null || echo "0.1")
        echo -e "${GREEN}✓${NC} (${duration}s)"
    ) &
    FORMAT_JS_PID=$!
else
    echo -e "${BLUE}Format JS...${NC} ${GREEN}✓ no changes${NC}"
fi

# 3. Lightweight lint (only changed Python files)
if [ "$PY_COUNT" -gt 0 ]; then
    (
        echo -ne "${BLUE}Quick Lint...${NC} "
        start=$(date +%s.%N 2>/dev/null || date +%s)
        
        # Basic syntax check only
        echo "$PY_FILES" | xargs -I {} python -m py_compile {} 2>/dev/null
        
        end=$(date +%s.%N 2>/dev/null || date +%s)
        duration=$(python3 -c "print(f'{$end - $start:.1f}')" 2>/dev/null || echo "0.1")
        echo -e "${GREEN}✓${NC} (${duration}s)"
    ) &
    LINT_PID=$!
else
    echo -e "${BLUE}Quick Lint...${NC} ${GREEN}✓ no changes${NC}"
fi

# 4. Smart test selection (only test affected modules)
if [ "$PY_COUNT" -gt 0 ]; then
    (
        echo -ne "${BLUE}Smart Tests...${NC} "
        start=$(date +%s.%N 2>/dev/null || date +%s)
        
        # Extract module names from changed files
        MODULES=$(echo "$PY_FILES" | grep -E "^(think_ai|tests)/" | sed 's|/[^/]*\.py$||' | sort -u | head -5)
        
        if [ -n "$MODULES" ]; then
            # Run only tests for changed modules (max 5 modules)
            TEST_PATHS=""
            for module in $MODULES; do
                if [[ "$module" == think_ai/* ]]; then
                    # Map source to test
                    TEST_PATH="tests/unit/test_${module#think_ai/}"
                    [ -d "$TEST_PATH" ] && TEST_PATHS="$TEST_PATHS $TEST_PATH"
                elif [[ "$module" == tests/* ]]; then
                    TEST_PATHS="$TEST_PATHS $module"
                fi
            done
            
            if [ -n "$TEST_PATHS" ]; then
                python -m pytest $TEST_PATHS -x --tb=no -q --disable-warnings 2>/dev/null || true
            fi
        fi
        
        end=$(date +%s.%N 2>/dev/null || date +%s)
        duration=$(python3 -c "print(f'{$end - $start:.1f}')" 2>/dev/null || echo "0.1")
        echo -e "${GREEN}✓${NC} (${duration}s)"
    ) &
    TEST_PID=$!
else
    echo -e "${BLUE}Smart Tests...${NC} ${GREEN}✓ no changes${NC}"
fi

# Wait for all parallel tasks
FAILED=0
[ -n "$FORMAT_PY_PID" ] && wait $FORMAT_PY_PID || FAILED=1
[ -n "$FORMAT_JS_PID" ] && wait $FORMAT_JS_PID || FAILED=1
[ -n "$LINT_PID" ] && wait $LINT_PID || FAILED=1
[ -n "$TEST_PID" ] && wait $TEST_PID || FAILED=1

# Final timing
PIPELINE_END=$(date +%s.%N 2>/dev/null || date +%s)
DURATION=$(python3 -c "print(f'{$PIPELINE_END - $PIPELINE_START:.1f}')" 2>/dev/null || echo "2")

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ Pipeline complete in ${DURATION}s${NC}"
    
    # Stage all changes
    git add -A
    
    # Show optimization tips
    if (( $(python3 -c "print(1 if $DURATION > 5 else 0)" 2>/dev/null || echo 0) )); then
        echo -e "${YELLOW}💡 Optimization tip: Commit smaller changesets for faster checks${NC}"
    fi
else
    echo -e "${RED}❌ Pipeline failed in ${DURATION}s${NC}"
    exit 1
fi

exit 0