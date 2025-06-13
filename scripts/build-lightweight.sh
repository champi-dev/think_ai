#!/bin/bash
# Build lightweight Docker images with pre-compiled binaries
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Building lightweight Docker images...${NC}"

# Enable BuildKit for better caching
export DOCKER_BUILDKIT=1

# Build Python API lightweight image
echo -e "${YELLOW}Building Python API lightweight image...${NC}"
docker build \
    --target runtime \
    --cache-from type=registry,ref=ghcr.io/think-ai/api:cache \
    --cache-to type=registry,ref=ghcr.io/think-ai/api:cache,mode=max \
    -t think-ai-api:lightweight \
    -f Dockerfile.lightweight .

# Get image size
API_SIZE=$(docker images think-ai-api:lightweight --format "{{.Size}}")
echo -e "${GREEN}✓ API image built successfully. Size: ${API_SIZE}${NC}"

# Build webapp lightweight image
if [ -d "webapp" ]; then
    echo -e "${YELLOW}Building webapp lightweight image...${NC}"
    cd webapp
    docker build \
        --cache-from type=registry,ref=ghcr.io/think-ai/webapp:cache \
        --cache-to type=registry,ref=ghcr.io/think-ai/webapp:cache,mode=max \
        -t think-ai-webapp:lightweight \
        -f Dockerfile.lightweight .
    
    WEBAPP_SIZE=$(docker images think-ai-webapp:lightweight --format "{{.Size}}")
    echo -e "${GREEN}✓ Webapp image built successfully. Size: ${WEBAPP_SIZE}${NC}"
    cd ..
fi

# Build binary-optimized image
echo -e "${YELLOW}Building binary-optimized image...${NC}"
docker build \
    --cache-from type=registry,ref=ghcr.io/think-ai/api:binary-cache \
    --cache-to type=registry,ref=ghcr.io/think-ai/api:binary-cache,mode=max \
    -t think-ai-api:binary \
    -f Dockerfile.binary .

BINARY_SIZE=$(docker images think-ai-api:binary --format "{{.Size}}")
echo -e "${GREEN}✓ Binary image built successfully. Size: ${BINARY_SIZE}${NC}"

# Compare with standard build
echo -e "${YELLOW}Building standard image for comparison...${NC}"
docker build -t think-ai-api:standard .
STANDARD_SIZE=$(docker images think-ai-api:standard --format "{{.Size}}")

# Summary
echo -e "\n${GREEN}=== Build Summary ===${NC}"
echo -e "Standard image size: ${STANDARD_SIZE}"
echo -e "Lightweight image size: ${API_SIZE}"
echo -e "Binary-optimized image size: ${BINARY_SIZE}"
if [ -d "webapp" ]; then
    echo -e "Webapp image size: ${WEBAPP_SIZE}"
fi

# Push images if requested
if [ "$1" == "--push" ]; then
    echo -e "\n${YELLOW}Pushing images...${NC}"
    docker tag think-ai-api:lightweight ghcr.io/think-ai/api:lightweight
    docker tag think-ai-api:binary ghcr.io/think-ai/api:binary
    docker push ghcr.io/think-ai/api:lightweight
    docker push ghcr.io/think-ai/api:binary
    
    if [ -d "webapp" ]; then
        docker tag think-ai-webapp:lightweight ghcr.io/think-ai/webapp:lightweight
        docker push ghcr.io/think-ai/webapp:lightweight
    fi
    
    echo -e "${GREEN}✓ Images pushed successfully${NC}"
fi

echo -e "\n${GREEN}Build complete!${NC}"