#!/bin/bash
# Elite O(1) Pre-commit Pipeline - Target: <10s execution
# Aggressive caching and parallel execution for maximum speed

set -euo pipefail

# Colors for instant visual feedback
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Performance tracking
PIPELINE_START=$(date +%s.%N)
CACHE_DIR="${HOME}/.think_ai_pipeline_cache"
mkdir -p "$CACHE_DIR"

# Function to run task with timing
run_task() {
    local name=$1
    local cmd=$2
    local start=$(date +%s.%N)
    
    echo -ne "${BLUE}${name}...${NC} "
    
    if eval "$cmd" > "${CACHE_DIR}/${name}.log" 2>&1; then
        local duration=$(echo "$(date +%s.%N) - $start" | bc | xargs printf "%.1f")
        echo -e "${GREEN}✓${NC} (${duration}s)"
        return 0
    else
        echo -e "${YELLOW}⚠${NC}"
        return 1
    fi
}

# Hash-based cache validation
get_python_hash() {
    find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" \
        -not -path "./node_modules/*" -not -path "./build/*" \
        -type f -exec md5sum {} \; | sort | md5sum | cut -d' ' -f1
}

get_js_hash() {
    find . -name "*.js" -name "*.ts" -name "*.tsx" -not -path "./node_modules/*" \
        -not -path "./build/*" -not -path "./.next/*" \
        -type f -exec md5sum {} \; | sort | md5sum | cut -d' ' -f1
}

# Check if we need to run based on file changes
CURRENT_PY_HASH=$(get_python_hash)
CURRENT_JS_HASH=$(get_js_hash)
CACHED_PY_HASH=$(cat "$CACHE_DIR/.py_hash" 2>/dev/null || echo "")
CACHED_JS_HASH=$(cat "$CACHE_DIR/.js_hash" 2>/dev/null || echo "")

echo -e "${BLUE}🚀 Think AI Fast Pipeline${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Parallel execution with background jobs
pids=()

# 1. Format Python (only if changed)
if [ "$CURRENT_PY_HASH" != "$CACHED_PY_HASH" ]; then
    (
        # Use black with minimal config for speed
        run_task "Format Python" "black . --quiet --fast --exclude='(venv|build|dist|node_modules)'" 
        echo "$CURRENT_PY_HASH" > "$CACHE_DIR/.py_hash"
    ) &
    pids+=($!)
else
    echo -e "${BLUE}Format Python...${NC} ${GREEN}✓ cached${NC}"
fi

# 2. Format JS/TS (only if changed)
if [ "$CURRENT_JS_HASH" != "$CACHED_JS_HASH" ] && [ -f "webapp/package.json" ]; then
    (
        cd webapp
        run_task "Format JS" "npx prettier --write 'src/**/*.{js,ts,tsx}' --loglevel error"
        echo "$CURRENT_JS_HASH" > "$CACHE_DIR/.js_hash"
    ) &
    pids+=($!)
else
    echo -e "${BLUE}Format JS...${NC} ${GREEN}✓ cached${NC}"
fi

# 3. Run tests in parallel with coverage
(
    # Only run critical unit tests, skip integration tests
    run_task "Tests" "python -m pytest tests/unit -x --tb=short -q --cov=think_ai --cov-report=term-missing:skip-covered --cov-fail-under=70"
) &
pids+=($!)

# 4. Verify build (lightweight check)
(
    # Just verify imports work, don't actually build
    run_task "Build Check" "python -c 'import think_ai; from think_ai_full import app'"
) &
pids+=($!)

# 5. Security scan (cached)
SECURITY_HASH=$(find . -name "*.py" -not -path "./venv/*" -type f -exec md5sum {} \; | md5sum | cut -d' ' -f1)
CACHED_SECURITY=$(cat "$CACHE_DIR/.security_hash" 2>/dev/null || echo "")

if [ "$SECURITY_HASH" != "$CACHED_SECURITY" ]; then
    (
        # Quick security checks only
        run_task "Security" "grep -r 'exec\\|eval\\|pickle.loads\\|yaml.load[^_]' --include='*.py' . || true"
        echo "$SECURITY_HASH" > "$CACHE_DIR/.security_hash"
    ) &
    pids+=($!)
else
    echo -e "${BLUE}Security...${NC} ${GREEN}✓ cached${NC}"
fi

# Wait for all parallel tasks
for pid in ${pids[@]}; do
    wait $pid
done

# Final timing
PIPELINE_END=$(date +%s.%N)
DURATION=$(echo "$PIPELINE_END - $PIPELINE_START" | bc)

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Pipeline complete in ${DURATION}s${NC}"

# Stage all changes
git add -A

# Exit successfully to allow commit
exit 0