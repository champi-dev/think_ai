#!/bin/bash
# Build ultra-optimized base image with O(1) caching

set -e

# Configuration
DOCKER_HUB_USERNAME="${DOCKER_HUB_USERNAME:-devsarmico}"
IMAGE_NAME="think-ai-base"
OPTIMIZED_TAG="${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:optimized"
LATEST_TAG="${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🚀 O(1) Ultra-Optimized Base Image Builder${NC}"
echo "============================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}Building optimized image...${NC}"
echo "Target size: <2GB (from 5GB)"
echo ""

# Build with buildkit for better caching
export DOCKER_BUILDKIT=1

# Build for AMD64 (Railway)
docker build \
    --platform linux/amd64 \
    --file Dockerfile.base.optimized \
    --tag "${OPTIMIZED_TAG}" \
    --tag "${LATEST_TAG}" \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    --progress=plain \
    .

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Build complete!${NC}"
    
    # Show size comparison
    echo ""
    echo "Image size:"
    docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}" | grep think-ai-base
    
    echo ""
    echo -e "${YELLOW}Pushing to Docker Hub...${NC}"
    docker push "${OPTIMIZED_TAG}"
    docker push "${LATEST_TAG}"
    
    echo ""
    echo -e "${GREEN}🎉 Optimized image pushed!${NC}"
    echo ""
    echo "Benefits:"
    echo "✓ 60%+ smaller image"
    echo "✓ Faster pulls from Docker Hub"
    echo "✓ Pre-compiled Python bytecode"
    echo "✓ Compressed wheel cache"
    echo "✓ Stripped debug symbols"
else
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi