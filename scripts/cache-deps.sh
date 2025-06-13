#!/bin/bash
# Aggressive dependency caching script for O(1) builds

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Cache directories
CACHE_BASE="${HOME}/.think-ai-cache"
PIP_CACHE="${CACHE_BASE}/pip"
NPM_CACHE="${CACHE_BASE}/npm"
VENV_CACHE="${CACHE_BASE}/venv"
MODEL_CACHE="${CACHE_BASE}/models"
BUILD_CACHE="${CACHE_BASE}/build"

# Create cache directories
mkdir -p "${PIP_CACHE}" "${NPM_CACHE}" "${VENV_CACHE}" "${MODEL_CACHE}" "${BUILD_CACHE}"

# Generate cache keys
PIP_CACHE_KEY=$(sha256sum requirements.txt | cut -d' ' -f1)
NPM_CACHE_KEY=$(sha256sum package.json | cut -d' ' -f1)

echo -e "${BLUE}🚀 ThinkAI Aggressive Dependency Caching${NC}"
echo -e "${BLUE}=====================================>${NC}"

# Function to cache Python dependencies
cache_python_deps() {
    echo -e "${YELLOW}📦 Caching Python dependencies...${NC}"
    
    VENV_PATH="${VENV_CACHE}/${PIP_CACHE_KEY}"
    
    if [ -d "${VENV_PATH}" ]; then
        echo -e "${GREEN}✓ Python cache hit! Using cached environment${NC}"
        ln -sf "${VENV_PATH}" .venv
    else
        echo -e "${YELLOW}Building Python cache...${NC}"
        python -m venv "${VENV_PATH}"
        source "${VENV_PATH}/bin/activate"
        
        # Use pip cache
        pip install --cache-dir="${PIP_CACHE}" -U pip wheel setuptools
        pip install --cache-dir="${PIP_CACHE}" -r requirements.txt
        
        # Pre-download models
        python -c "
from sentence_transformers import SentenceTransformer
import os
os.environ['TRANSFORMERS_CACHE'] = '${MODEL_CACHE}'
os.environ['HF_HOME'] = '${MODEL_CACHE}'
SentenceTransformer('all-MiniLM-L6-v2')
print('✓ Models cached')
"
        
        ln -sf "${VENV_PATH}" .venv
        echo -e "${GREEN}✓ Python dependencies cached${NC}"
    fi
}

# Function to cache Node dependencies
cache_node_deps() {
    echo -e "${YELLOW}📦 Caching Node dependencies...${NC}"
    
    NODE_MODULES_CACHE="${NPM_CACHE}/${NPM_CACHE_KEY}"
    
    if [ -d "${NODE_MODULES_CACHE}" ]; then
        echo -e "${GREEN}✓ Node cache hit! Using cached modules${NC}"
        ln -sf "${NODE_MODULES_CACHE}" node_modules
    else
        echo -e "${YELLOW}Building Node cache...${NC}"
        npm ci --cache "${NPM_CACHE}/.npm"
        mv node_modules "${NODE_MODULES_CACHE}"
        ln -sf "${NODE_MODULES_CACHE}" node_modules
        echo -e "${GREEN}✓ Node dependencies cached${NC}"
    fi
}

# Function to cache Docker layers
cache_docker_build() {
    echo -e "${YELLOW}🐳 Building Docker with cache...${NC}"
    
    # Enable BuildKit for better caching
    export DOCKER_BUILDKIT=1
    
    docker build \
        --cache-from think-ai:cache \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        -t think-ai:latest \
        -t think-ai:cache \
        --target runtime \
        .
    
    echo -e "${GREEN}✓ Docker image built with cache${NC}"
}

# Clean old cache entries
clean_old_cache() {
    echo -e "${YELLOW}🧹 Cleaning old cache entries...${NC}"
    
    # Keep only 3 most recent cache entries for each type
    for cache_dir in "${VENV_CACHE}" "${NPM_CACHE}"; do
        if [ -d "${cache_dir}" ]; then
            ls -t "${cache_dir}" | tail -n +4 | xargs -I {} rm -rf "${cache_dir}/{}"
        fi
    done
    
    echo -e "${GREEN}✓ Cache cleaned${NC}"
}

# Main execution
main() {
    case "${1:-all}" in
        python)
            cache_python_deps
            ;;
        node)
            cache_node_deps
            ;;
        docker)
            cache_docker_build
            ;;
        clean)
            clean_old_cache
            ;;
        all)
            cache_python_deps
            cache_node_deps
            echo -e "${GREEN}✨ All dependencies cached successfully!${NC}"
            echo -e "${BLUE}Next builds will be O(1) complexity${NC}"
            ;;
        *)
            echo "Usage: $0 {python|node|docker|clean|all}"
            exit 1
            ;;
    esac
}

# Export cache paths for other scripts
export TRANSFORMERS_CACHE="${MODEL_CACHE}"
export HF_HOME="${MODEL_CACHE}"
export PIP_CACHE_DIR="${PIP_CACHE}"
export npm_config_cache="${NPM_CACHE}/.npm"

main "$@"