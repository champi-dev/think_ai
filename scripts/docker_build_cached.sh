#!/bin/bash
# Fast Docker build with caching

set -e

echo "🚀 Building Docker images with caching..."
echo "======================================"

# Enable BuildKit
export DOCKER_BUILDKIT=1

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Build lightweight image if binaries exist
if [ -f "Dockerfile.lightweight" ] && [ -f "binaries.tar.gz" ]; then
    echo -e "\n${YELLOW}🐳 Building lightweight image with cache...${NC}"
    docker build \
        -f Dockerfile.lightweight \
        -t think-ai:lightweight \
        --cache-from think-ai:lightweight \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --progress=plain \
        .
    echo -e "${GREEN}✅ Lightweight image built!${NC}"
else
    echo -e "\n${YELLOW}🐳 Building standard image with cache...${NC}"
    docker build \
        -f Dockerfile \
        -t think-ai:latest \
        --cache-from think-ai:latest \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --progress=plain \
        .
    echo -e "${GREEN}✅ Standard image built!${NC}"
fi

# Show image sizes
echo -e "\n${GREEN}📊 Docker images:${NC}"
docker images | grep think-ai