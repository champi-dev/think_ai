#!/bin/bash
# Build base image in background with progress monitoring

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
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🚀 Think AI Base Image Builder (Background Mode)${NC}"
echo "================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create log file
LOG_FILE="${SCRIPT_DIR}/build_base.log"
echo "Build started at $(date)" > "$LOG_FILE"

echo -e "${YELLOW}Building base image in background...${NC}"
echo "This will take 15-20 minutes for the full system"
echo ""
echo "Docker Hub: ${DOCKER_HUB_USERNAME}"
echo "Image: ${LATEST_TAG}"
echo "Log file: ${LOG_FILE}"
echo ""

# Build in background
nohup docker build \
    --file Dockerfile.base \
    --tag "${VERSION_TAG}" \
    --tag "${LATEST_TAG}" \
    --progress=plain \
    . >> "$LOG_FILE" 2>&1 &

BUILD_PID=$!
echo "Build PID: ${BUILD_PID}"
echo ""

# Monitor progress
echo -e "${BLUE}Monitor progress with:${NC}"
echo "  tail -f ${LOG_FILE}"
echo ""
echo -e "${BLUE}Check if build is complete:${NC}"
echo "  ps -p ${BUILD_PID}"
echo ""
echo -e "${BLUE}Once complete, push to Docker Hub:${NC}"
echo "  docker push ${LATEST_TAG}"
echo ""

# Save build info
cat > "${SCRIPT_DIR}/build_info.txt" << EOF
Build started: $(date)
PID: ${BUILD_PID}
Image: ${LATEST_TAG}
Version: ${VERSION_TAG}
Log: ${LOG_FILE}
EOF

echo -e "${GREEN}✅ Build started in background!${NC}"
echo ""
echo "Next steps:"
echo "1. Wait for build to complete (check with: ps -p ${BUILD_PID})"
echo "2. Push image: docker push ${LATEST_TAG}"
echo "3. Deploy to Railway!"