#!/bin/bash
# Build and push the base Docker image to Docker Hub
# This script should be run whenever requirements-full.txt changes

set -e  # Exit on error

# Configuration
DOCKER_HUB_USERNAME="${DOCKER_HUB_USERNAME:-yourusername}"
IMAGE_NAME="think-ai-base"
VERSION=$(date +%Y%m%d-%H%M%S)
LATEST_TAG="${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest"
VERSION_TAG="${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Think AI Base Image Builder${NC}"
echo "========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

# Check if logged in to Docker Hub
if ! docker info 2>/dev/null | grep -q "Username"; then
    echo -e "${YELLOW}Warning: Not logged in to Docker Hub${NC}"
    echo "Please run: docker login"
    exit 1
fi

# Check if requirements file exists
if [ ! -f "requirements-full.txt" ]; then
    echo -e "${RED}Error: requirements-full.txt not found${NC}"
    exit 1
fi

echo -e "${YELLOW}Building base image...${NC}"
echo "Version: ${VERSION}"
echo "Tags: ${VERSION_TAG}, ${LATEST_TAG}"

# Build the base image
docker build \
    --file Dockerfile.base \
    --tag "${VERSION_TAG}" \
    --tag "${LATEST_TAG}" \
    --platform linux/amd64 \
    --progress plain \
    .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Build successful${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi

# Show image size
IMAGE_SIZE=$(docker images "${LATEST_TAG}" --format "{{.Size}}")
echo -e "${YELLOW}Image size: ${IMAGE_SIZE}${NC}"

# Push to Docker Hub
echo -e "${YELLOW}Pushing to Docker Hub...${NC}"

# Push version tag
docker push "${VERSION_TAG}"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Pushed ${VERSION_TAG}${NC}"
else
    echo -e "${RED}✗ Failed to push ${VERSION_TAG}${NC}"
    exit 1
fi

# Push latest tag
docker push "${LATEST_TAG}"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Pushed ${LATEST_TAG}${NC}"
else
    echo -e "${RED}✗ Failed to push ${LATEST_TAG}${NC}"
    exit 1
fi

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}✓ Base image successfully built and pushed!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Update Dockerfile.api and Dockerfile.worker with:"
echo "   ARG BASE_IMAGE=${LATEST_TAG}"
echo ""
echo "2. Update railway.json to use Dockerfile.api"
echo ""
echo "3. Deploy to Railway - builds should now take ~10 seconds!"
echo ""
echo "Version tag for production: ${VERSION_TAG}"