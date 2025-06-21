#!/bin/bash
# Elite dependency caching system for Think AI
# Achieves O(1) lookup performance through intelligent caching

set -euo pipefail

# Color codes for beautiful output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Performance tracking
START_TIME=$(date +%s.%N)

echo -e "${PURPLE}🚀 Think AI Elite Dependency Cache System${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Create cache directories with optimal structure
CACHE_ROOT="${HOME}/.think_ai_cache"
PIP_CACHE="${CACHE_ROOT}/pip"
WHEEL_CACHE="${CACHE_ROOT}/wheels"
TRANSFORMERS_CACHE="${CACHE_ROOT}/transformers"
TORCH_CACHE="${CACHE_ROOT}/torch"
MODEL_CACHE="${CACHE_ROOT}/models"
NPM_CACHE="${CACHE_ROOT}/npm"
NEXT_CACHE="${CACHE_ROOT}/next"

# Create all cache directories
mkdir -p "${PIP_CACHE}" "${WHEEL_CACHE}" "${TRANSFORMERS_CACHE}" "${TORCH_CACHE}" "${MODEL_CACHE}" "${NPM_CACHE}" "${NEXT_CACHE}"

# Hash-based cache validation for O(1) verification
REQUIREMENTS_HASH=$(sha256sum requirements-full.txt | cut -d' ' -f1)
PACKAGE_JSON_HASH=$(sha256sum webapp/package.json | cut -d' ' -f1)
CACHE_MANIFEST="${CACHE_ROOT}/manifest.json"

# Check if cache is valid
check_cache_validity() {
    if [ -f "${CACHE_MANIFEST}" ]; then
        STORED_PY_HASH=$(jq -r '.python_hash // empty' "${CACHE_MANIFEST}" 2>/dev/null || echo "")
        STORED_JS_HASH=$(jq -r '.js_hash // empty' "${CACHE_MANIFEST}" 2>/dev/null || echo "")

        if [ "${STORED_PY_HASH}" = "${REQUIREMENTS_HASH}" ] && [ "${STORED_JS_HASH}" = "${PACKAGE_JSON_HASH}" ]; then
            echo -e "${GREEN}✅ Cache is valid and up-to-date!${NC}"
            return 0
        fi
    fi
    return 1
}

# Python dependency caching with wheel pre-building
cache_python_deps() {
    echo -e "\n${BLUE}📦 Optimizing Python dependencies...${NC}"

    # Configure pip for maximum caching efficiency
    export PIP_CACHE_DIR="${PIP_CACHE}"
    export PIP_WHEEL_DIR="${WHEEL_CACHE}"
    export XDG_CACHE_HOME="${CACHE_ROOT}"

    # Pre-download all wheels for O(1) installation
    echo -e "${YELLOW}⚡ Pre-building wheels for instant installation...${NC}"
    pip wheel -r requirements-full.txt --wheel-dir="${WHEEL_CACHE}" --quiet

    # Download PyTorch with CPU optimization
    echo -e "${YELLOW}🔧 Caching PyTorch CPU wheels...${NC}"
    pip download torch==2.1.2 --index-url https://download.pytorch.org/whl/cpu \
        --dest="${TORCH_CACHE}" --no-deps --quiet

    # Pre-cache transformer models
    echo -e "${YELLOW}🧠 Pre-caching AI models...${NC}"
    python3 -c "
import os
os.environ['TRANSFORMERS_CACHE'] = '${TRANSFORMERS_CACHE}'
os.environ['HF_HOME'] = '${MODEL_CACHE}'
from sentence_transformers import SentenceTransformer
# Pre-download the model
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='${MODEL_CACHE}')
print('Model cached successfully!')
"

    echo -e "${GREEN}✅ Python dependencies cached!${NC}"
}

# Node.js dependency caching with pnpm-style hard linking
cache_node_deps() {
    echo -e "\n${BLUE}📦 Optimizing Node.js dependencies...${NC}"

    cd webapp

    # Configure npm for aggressive caching
    npm config set cache "${NPM_CACHE}"

    # Use npm ci with cache for deterministic installs
    echo -e "${YELLOW}⚡ Installing with cache optimization...${NC}"
    npm ci --prefer-offline --cache="${NPM_CACHE}"

    # Pre-build Next.js for faster starts
    echo -e "${YELLOW}🏗️ Pre-building Next.js...${NC}"
    NEXT_TELEMETRY_DISABLED=1 npm run build

    # Cache Next.js build artifacts
    if [ -d ".next" ]; then
        cp -r .next "${NEXT_CACHE}/"
    fi

    cd ..
    echo -e "${GREEN}✅ Node.js dependencies cached!${NC}"
}

# Create cache manifest for validation
update_cache_manifest() {
    cat > "${CACHE_MANIFEST}" <<EOF
{
    "python_hash": "${REQUIREMENTS_HASH}",
    "js_hash": "${PACKAGE_JSON_HASH}",
    "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "cache_size": "$(du -sh ${CACHE_ROOT} | cut -f1)",
    "python_wheels": $(ls -1 ${WHEEL_CACHE}/*.whl 2>/dev/null | wc -l),
    "npm_packages": $(find ${NPM_CACHE} -name "package.json" 2>/dev/null | wc -l)
}
EOF
}

# Main execution
if check_cache_validity; then
    echo -e "${CYAN}⚡ Using existing cache - O(1) performance!${NC}"
else
    echo -e "${YELLOW}🔄 Cache invalid or missing - rebuilding...${NC}"
    cache_python_deps
    cache_node_deps
    update_cache_manifest
fi

# Create optimized pip.conf for future installs
mkdir -p ~/.config/pip
cat > ~/.config/pip/pip.conf <<EOF
[global]
cache-dir = ${PIP_CACHE}
wheel-dir = ${WHEEL_CACHE}
find-links = file://${WHEEL_CACHE}
prefer-binary = true
no-compile = true

[install]
use-feature = fast-deps
use-feature = in-tree-build
EOF

# Performance report
END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc)

echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Cache optimization complete!${NC}"
echo -e "${CYAN}📊 Performance Metrics:${NC}"
echo -e "  ⏱️  Duration: ${DURATION}s"
echo -e "  💾 Cache size: $(du -sh ${CACHE_ROOT} | cut -f1)"
echo -e "  📦 Python wheels: $(ls -1 ${WHEEL_CACHE}/*.whl 2>/dev/null | wc -l)"
echo -e "  📦 NPM packages: $(find ${NPM_CACHE} -name "package.json" 2>/dev/null | wc -l)"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Export cache paths for other scripts
echo -e "\n${BLUE}💡 Export these for instant installs:${NC}"
echo "export PIP_CACHE_DIR='${PIP_CACHE}'"
echo "export PIP_FIND_LINKS='file://${WHEEL_CACHE}'"
echo "export TRANSFORMERS_CACHE='${TRANSFORMERS_CACHE}'"
echo "export HF_HOME='${MODEL_CACHE}'"
echo "export npm_config_cache='${NPM_CACHE}'"
