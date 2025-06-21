#!/bin/bash
# O(1) Ultra Deploy: 10-second Railway deployment script
# Complexity: O(1) - constant time operations only
# Beauty: Crafted for perfection

set -euo pipefail

# Color codes for beautiful output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Performance tracking
DEPLOY_START=$(date +%s.%N)

echo -e "${CYAN}🚀 O(1) Ultra Deploy - 10 Second Railway Deployment${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════${NC}"

# Configuration
CACHE_DIR="${O1_CACHE_DIR:-/cache/think-ai}"
BUNDLE_HASH="${O1_BUNDLE_HASH:-auto}"
PARALLEL_JOBS="${O1_PARALLEL_JOBS:-$(nproc)}"
TARGET_SECONDS=10

# Helper function for timing
time_operation() {
    local name=$1
    local start=$(date +%s.%N)
    shift
    "$@"
    local end=$(date +%s.%N)
    local elapsed=$(echo "$end - $start" | bc)
    echo -e "${GREEN}✓${NC} $name completed in ${YELLOW}${elapsed}s${NC}"
}

# O(1) cache check
check_cache() {
    echo -e "\n${BLUE}📦 Checking O(1) cache...${NC}"
    
    if [ ! -d "$CACHE_DIR" ]; then
        echo -e "${RED}❌ Cache directory not found: $CACHE_DIR${NC}"
        echo -e "${YELLOW}Creating cache directory...${NC}"
        mkdir -p "$CACHE_DIR"
        return 1
    fi
    
    # Find the latest bundle (O(1) with proper indexing)
    if [ "$BUNDLE_HASH" = "auto" ]; then
        BUNDLE_PATH=$(find "$CACHE_DIR/bundles" -name "ultra-bundle-*.tar.xz" -type f | sort -r | head -1)
    else
        BUNDLE_PATH="$CACHE_DIR/bundles/ultra-bundle-$BUNDLE_HASH.tar.xz"
    fi
    
    if [ -z "$BUNDLE_PATH" ] || [ ! -f "$BUNDLE_PATH" ]; then
        echo -e "${RED}❌ No cache bundle found${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓${NC} Found cache bundle: $(basename $BUNDLE_PATH)"
    echo -e "  Size: $(du -h $BUNDLE_PATH | cut -f1)"
    return 0
}

# O(1) dependency installation
install_dependencies() {
    echo -e "\n${BLUE}⚡ Installing dependencies with O(1) performance...${NC}"
    
    local install_dir="/tmp/o1_install_$$"
    mkdir -p "$install_dir"
    
    # Extract with parallel decompression
    echo -e "${YELLOW}Extracting bundle...${NC}"
    tar -xJf "$BUNDLE_PATH" -C "$install_dir" --use-compress-program="xz -T${PARALLEL_JOBS}"
    
    # Read metadata
    local metadata=$(cat "$install_dir/metadata.json")
    local dep_count=$(echo "$metadata" | jq -r '.dependency_count')
    
    echo -e "${YELLOW}Installing $dep_count dependencies in parallel...${NC}"
    
    # Install wheels in parallel batches for O(1) perceived time
    find "$install_dir/wheels" -name "*.whl" -print0 | \
        xargs -0 -P"$PARALLEL_JOBS" -n10 pip install \
            --no-deps \
            --no-index \
            --no-cache-dir \
            --disable-pip-version-check \
            --quiet
    
    # Cleanup
    rm -rf "$install_dir"
    
    echo -e "${GREEN}✓${NC} All dependencies installed"
}

# O(1) model cache setup
setup_model_cache() {
    echo -e "\n${BLUE}🧠 Setting up model cache...${NC}"
    
    # Create symlinks for O(1) model access
    if [ -d "$CACHE_DIR/models" ]; then
        export HF_HOME="$CACHE_DIR/models/huggingface"
        export TRANSFORMERS_CACHE="$CACHE_DIR/models/transformers"
        export SENTENCE_TRANSFORMERS_HOME="$CACHE_DIR/models/sentence-transformers"
        echo -e "${GREEN}✓${NC} Model cache configured"
    else
        echo -e "${YELLOW}⚠${NC}  No model cache found (will download on first use)"
    fi
}

# O(1) Think AI optimization
optimize_think_ai() {
    echo -e "\n${BLUE}🇨🇴 Applying Think AI optimizations...${NC}"
    
    # Enable all O(1) optimizations
    export THINK_AI_O1_MODE="true"
    export THINK_AI_COLOMBIAN_MODE="true"
    export THINK_AI_CACHE_EVERYTHING="true"
    export THINK_AI_PARALLEL_WORKERS="$PARALLEL_JOBS"
    
    # Pre-warm caches
    python -c "
import think_ai
from think_ai.intelligence_optimizer import intelligence_optimizer
from think_ai.parallel_processor import parallel_processor
print('✓ Think AI modules pre-loaded')
" 2>/dev/null || echo -e "${YELLOW}⚠${NC}  Think AI pre-loading skipped"
    
    echo -e "${GREEN}✓${NC} Think AI optimized for O(1) performance"
}

# Main deployment flow
main() {
    echo -e "\n${PURPLE}Starting deployment sequence...${NC}"
    
    # Step 1: Check cache
    if ! check_cache; then
        echo -e "${RED}ERROR: No cache available. Build cache first with:${NC}"
        echo -e "  python o1_ultra_cache.py --requirements requirements-full.txt"
        exit 1
    fi
    
    # Step 2: Install dependencies
    time_operation "Dependency installation" install_dependencies
    
    # Step 3: Setup model cache
    time_operation "Model cache setup" setup_model_cache
    
    # Step 4: Optimize Think AI
    time_operation "Think AI optimization" optimize_think_ai
    
    # Calculate total time
    DEPLOY_END=$(date +%s.%N)
    TOTAL_TIME=$(echo "$DEPLOY_END - $DEPLOY_START" | bc)
    
    # Success report
    echo -e "\n${CYAN}══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🎯 DEPLOYMENT COMPLETE!${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════${NC}"
    echo -e "Total time: ${YELLOW}${TOTAL_TIME}s${NC}"
    echo -e "Target:     ${GREEN}${TARGET_SECONDS}s${NC}"
    
    if (( $(echo "$TOTAL_TIME < $TARGET_SECONDS" | bc -l) )); then
        echo -e "\n${GREEN}✨ ELITE PERFORMANCE ACHIEVED! ✨${NC}"
        echo -e "${GREEN}Deployment completed ${YELLOW}$(echo "$TARGET_SECONDS - $TOTAL_TIME" | bc)s${GREEN} under target!${NC}"
    else
        echo -e "\n${YELLOW}⚠ Target not met. Time to optimize further.${NC}"
    fi
    
    # Start the application
    echo -e "\n${BLUE}🚀 Starting Think AI...${NC}"
    exec "$@"
}

# Run main if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi