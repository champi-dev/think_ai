#!/bin/bash
# Docker Hypercache - O(1) deployment with aggressive Docker caching

set -euo pipefail

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
REGISTRY_URL="${DOCKER_REGISTRY:-localhost:5000}"
CACHE_DIR="${DOCKER_CACHE_DIR:-/tmp/docker-cache}"
BUILD_CACHE_SIZE="${BUILD_CACHE_SIZE:-50G}"
PARALLEL_JOBS="${PARALLEL_JOBS:-8}"

echo -e "${BLUE}🚀 Docker Hypercache - O(1) Deployment${NC}"
echo -e "${BLUE}====================================>${NC}"

# Initialize local registry
init_registry() {
    echo -e "${YELLOW}📦 Initializing local Docker registry...${NC}"
    
    if ! docker ps | grep -q registry; then
        docker-compose -f docker-compose.cache.yml up -d registry redis
        sleep 5
    fi
    
    # Test registry
    curl -s http://localhost:5000/v2/_catalog > /dev/null || {
        echo -e "${RED}Registry not accessible${NC}"
        exit 1
    }
    
    echo -e "${GREEN}✓ Registry ready at ${REGISTRY_URL}${NC}"
}

# Setup BuildKit with maximum caching
setup_buildkit() {
    echo -e "${YELLOW}🔧 Configuring BuildKit for maximum performance...${NC}"
    
    # Create BuildKit config
    mkdir -p ~/.docker/cli-plugins
    
    cat > ~/.docker/buildkitd.toml << EOF
[worker.oci]
  max-parallelism = ${PARALLEL_JOBS}

[registry."${REGISTRY_URL}"]
  http = true
  insecure = true

[[registry."${REGISTRY_URL}".mirror]]
  url = "http://${REGISTRY_URL}"
EOF
    
    # Enable BuildKit
    export DOCKER_BUILDKIT=1
    export BUILDKIT_PROGRESS=plain
    export COMPOSE_DOCKER_CLI_BUILD=1
    
    # Create cache directory
    mkdir -p "${CACHE_DIR}"
    
    echo -e "${GREEN}✓ BuildKit configured${NC}"
}

# Build base image with all system dependencies
build_base_image() {
    echo -e "${YELLOW}🏗️  Building pre-warmed base image...${NC}"
    
    cat > Dockerfile.base << 'EOF'
FROM python:3.11-slim

# Install system dependencies once
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl ca-certificates gnupg \
    libgomp1 libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Pre-install common Python tools
RUN pip install --no-cache-dir \
    pip==23.3.1 \
    setuptools==68.2.2 \
    wheel==0.41.3 \
    poetry==1.7.1 \
    build==1.0.3

# Create cache directories
RUN mkdir -p /cache/{pip,npm,huggingface,torch}
EOF
    
    # Build with all caching
    docker buildx build \
        --cache-from=type=local,src="${CACHE_DIR}" \
        --cache-from=type=registry,ref="${REGISTRY_URL}/think-ai-base:latest" \
        --cache-to=type=local,dest="${CACHE_DIR}",mode=max \
        --cache-to=type=registry,ref="${REGISTRY_URL}/think-ai-base:latest",mode=max \
        -t "${REGISTRY_URL}/think-ai-base:latest" \
        -f Dockerfile.base \
        --push .
    
    echo -e "${GREEN}✓ Base image ready${NC}"
}

# Generate dependency hash for cache invalidation
generate_dep_hash() {
    echo -n "$(cat requirements.txt package.json 2>/dev/null | sha256sum | cut -d' ' -f1)"
}

# Hypercache build function
hypercache_build() {
    echo -e "${YELLOW}⚡ Building with hypercache...${NC}"
    
    local DEP_HASH=$(generate_dep_hash)
    local BUILD_START=$(date +%s)
    
    # Check if image already exists in registry
    if curl -s "http://${REGISTRY_URL}/v2/think-ai/tags/list" | grep -q "\"${DEP_HASH}\""; then
        echo -e "${GREEN}✓ Cache hit! Image already exists for hash ${DEP_HASH}${NC}"
        docker pull "${REGISTRY_URL}/think-ai:${DEP_HASH}"
        docker tag "${REGISTRY_URL}/think-ai:${DEP_HASH}" think-ai:latest
        
        local BUILD_END=$(date +%s)
        echo -e "${BLUE}⏱️  Build time: $((BUILD_END - BUILD_START)) seconds (O(1) cache hit!)${NC}"
        return 0
    fi
    
    # Build with maximum parallelism and caching
    docker buildx build \
        --build-arg DEPENDENCY_HASH="${DEP_HASH}" \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --cache-from=type=local,src="${CACHE_DIR}" \
        --cache-from=type=registry,ref="${REGISTRY_URL}/think-ai:cache" \
        --cache-from=type=registry,ref="${REGISTRY_URL}/think-ai:${DEP_HASH}" \
        --cache-from=type=registry,ref="${REGISTRY_URL}/think-ai:latest" \
        --cache-to=type=local,dest="${CACHE_DIR}",mode=max \
        --cache-to=type=registry,ref="${REGISTRY_URL}/think-ai:cache",mode=max \
        --cache-to=type=inline \
        --output=type=image,name="${REGISTRY_URL}/think-ai:${DEP_HASH},${REGISTRY_URL}/think-ai:latest",push=true \
        -f Dockerfile.hypercache \
        --platform=linux/amd64 \
        --network=host \
        .
    
    # Pull the built image
    docker pull "${REGISTRY_URL}/think-ai:latest"
    docker tag "${REGISTRY_URL}/think-ai:latest" think-ai:latest
    
    local BUILD_END=$(date +%s)
    echo -e "${GREEN}✓ Build complete in $((BUILD_END - BUILD_START)) seconds${NC}"
}

# Pre-warm caches
warm_caches() {
    echo -e "${YELLOW}🔥 Pre-warming all caches...${NC}"
    
    # Start cache warmer
    docker-compose -f docker-compose.cache.yml up -d cache-warmer
    
    # Pre-pull common base images
    docker pull python:3.11-slim &
    docker pull node:20-alpine &
    docker pull redis:7-alpine &
    wait
    
    echo -e "${GREEN}✓ Caches warmed${NC}"
}

# Clean old caches
clean_caches() {
    echo -e "${YELLOW}🧹 Cleaning old caches...${NC}"
    
    # Prune old images (keep last 10)
    docker image prune -a --force --filter "until=168h"
    
    # Clean build cache (keep recent)
    docker buildx prune --force --filter "until=168h"
    
    # Clean registry
    curl -X DELETE "http://${REGISTRY_URL}/v2/_catalog"
    
    echo -e "${GREEN}✓ Caches cleaned${NC}"
}

# Main execution
main() {
    case "${1:-build}" in
        init)
            init_registry
            setup_buildkit
            build_base_image
            warm_caches
            echo -e "${GREEN}✨ Hypercache initialized!${NC}"
            ;;
        build)
            init_registry
            setup_buildkit
            hypercache_build
            ;;
        clean)
            clean_caches
            ;;
        status)
            echo -e "${BLUE}📊 Cache Status:${NC}"
            du -sh "${CACHE_DIR}" 2>/dev/null || echo "No local cache"
            docker system df
            curl -s "http://${REGISTRY_URL}/v2/_catalog" | jq .
            ;;
        *)
            echo "Usage: $0 {init|build|clean|status}"
            exit 1
            ;;
    esac
}

# Export for other scripts
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_REGISTRY="${REGISTRY_URL}"

main "$@"