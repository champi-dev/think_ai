#!/bin/bash
# Build base image for multiple architectures (including Railway's AMD64)

set -e

# Configuration
DOCKER_HUB_USERNAME="${DOCKER_HUB_USERNAME:-devsarmico}"
IMAGE_NAME="think-ai-base"
VERSION=$(date +%Y%m%d-%H%M%S)
LATEST_TAG="${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest"
VERSION_TAG="${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 Think AI Multi-Architecture Base Image Builder${NC}"
echo "=================================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${YELLOW}Building for AMD64 (Railway) and ARM64 (your Mac)...${NC}"
echo ""

# Check if buildx is available
if ! docker buildx version &>/dev/null; then
    echo -e "${RED}Docker buildx not found. Installing...${NC}"
    docker buildx create --use
fi

# Build and push multi-architecture image
echo "Building and pushing to Docker Hub..."
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --file Dockerfile.base \
    --tag "${LATEST_TAG}" \
    --tag "${VERSION_TAG}" \
    --push \
    .

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Multi-architecture image pushed successfully!${NC}"
    echo ""
    echo "Image: ${LATEST_TAG}"
    echo "Platforms: linux/amd64 (Railway), linux/arm64 (Apple Silicon)"
    echo ""
    echo "Railway will now use the AMD64 version automatically!"
else
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi