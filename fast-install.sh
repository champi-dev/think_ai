#!/bin/bash
# Elite Fast Installation System for Think AI
# O(1) performance through intelligent caching

set -euo pipefail

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${PURPLE}⚡ Think AI Fast Install System${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Performance tracking
START_TIME=$(date +%s.%N)

# Cache configuration
CACHE_ROOT="${HOME}/.think_ai_cache"
PIP_CACHE="${CACHE_ROOT}/pip"
WHEEL_CACHE="${CACHE_ROOT}/wheels"
NPM_CACHE="${CACHE_ROOT}/npm"

# Ensure cache directories exist
mkdir -p "${PIP_CACHE}" "${WHEEL_CACHE}" "${NPM_CACHE}"

# Configure environment for caching
export PIP_CACHE_DIR="${PIP_CACHE}"
export PIP_FIND_LINKS="file://${WHEEL_CACHE}"
export npm_config_cache="${NPM_CACHE}"

# Function to check if deps are already cached
check_python_cache() {
    local req_hash=$(sha256sum requirements-full.txt | cut -d' ' -f1)
    local cache_file="${CACHE_ROOT}/.python_hash"

    if [ -f "$cache_file" ] && [ "$(cat $cache_file)" = "$req_hash" ]; then
        return 0
    fi
    echo "$req_hash" > "$cache_file"
    return 1
}

check_node_cache() {
    local pkg_hash=$(sha256sum webapp/package.json | cut -d' ' -f1)
    local cache_file="${CACHE_ROOT}/.node_hash"

    if [ -f "$cache_file" ] && [ "$(cat $cache_file)" = "$pkg_hash" ]; then
        return 0
    fi
    echo "$pkg_hash" > "$cache_file"
    return 1
}

# Python setup with caching
echo -e "\n${BLUE}🐍 Setting up Python environment...${NC}"

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate

if check_python_cache; then
    echo -e "${GREEN}✅ Using cached Python dependencies!${NC}"
    pip install -r requirements-full.txt --find-links="${WHEEL_CACHE}" --prefer-binary --no-index 2>/dev/null || \
    pip install -r requirements-full.txt --find-links="${WHEEL_CACHE}" --prefer-binary
else
    echo -e "${YELLOW}Building Python wheel cache...${NC}"
    # First, upgrade pip for better performance
    pip install --upgrade pip wheel setuptools

    # Build all wheels
    pip wheel -r requirements-full.txt --wheel-dir="${WHEEL_CACHE}"

    # Install from wheels
    pip install -r requirements-full.txt --find-links="${WHEEL_CACHE}" --prefer-binary
fi

# Node.js setup with caching
echo -e "\n${BLUE}📦 Setting up Node.js environment...${NC}"

cd webapp

if check_node_cache; then
    echo -e "${GREEN}✅ Using cached Node dependencies!${NC}"
else
    echo -e "${YELLOW}Installing Node dependencies...${NC}"
    npm ci --cache="${NPM_CACHE}" --prefer-offline
fi

cd ..

# Pre-download AI models for instant startup
echo -e "\n${BLUE}🧠 Pre-caching AI models...${NC}"

python3 -c "
import os
os.environ['TRANSFORMERS_CACHE'] = '${CACHE_ROOT}/transformers'
os.environ['HF_HOME'] = '${CACHE_ROOT}/models'

try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print('✅ Model cached successfully!')
except Exception as e:
    print(f'⚠️  Model caching skipped: {e}')
"

# Performance report
END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc)

echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Installation complete!${NC}"
echo -e "${CYAN}📊 Performance:${NC}"
echo -e "  ⏱️  Total time: ${DURATION}s"
echo -e "  💾 Cache size: $(du -sh ${CACHE_ROOT} 2>/dev/null | cut -f1 || echo 'N/A')"
echo -e "\n${BLUE}🚀 Start Think AI with:${NC}"
echo -e "  ${YELLOW}python think_ai_full.py${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
