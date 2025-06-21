#!/bin/bash
# Verify O(1) deployment setup

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Think AI O(1) Deployment Verification${NC}"
echo "========================================="

# Check required files
echo -e "\n${YELLOW}Checking required files...${NC}"

files=(
    "Dockerfile.base"
    "Dockerfile.api"
    "Dockerfile.worker"
    "build_and_push_base.sh"
    "railway.json"
    "requirements-full.txt"
)

all_files_exist=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file - Missing!"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    echo -e "\n${RED}Some required files are missing!${NC}"
    exit 1
fi

# Check Docker
echo -e "\n${YELLOW}Checking Docker...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker is installed"
    docker_version=$(docker --version)
    echo "  Version: $docker_version"
else
    echo -e "${RED}✗${NC} Docker is not installed"
    exit 1
fi

# Check Docker login
echo -e "\n${YELLOW}Checking Docker Hub login...${NC}"
if docker info 2>/dev/null | grep -q "Username"; then
    echo -e "${GREEN}✓${NC} Logged in to Docker registry"
else
    echo -e "${YELLOW}!${NC} Not logged in to Docker Hub"
    echo "  Run: docker login"
fi

# Check if base image exists locally
echo -e "\n${YELLOW}Checking for base image...${NC}"
if docker images | grep -q "think-ai-base"; then
    echo -e "${GREEN}✓${NC} Base image exists locally"
    docker images | grep "think-ai-base"
else
    echo -e "${YELLOW}!${NC} Base image not found locally"
    echo "  Run: ./build_and_push_base.sh"
fi

# Test build time with API Dockerfile
echo -e "\n${YELLOW}Testing API build time (should be <30 seconds)...${NC}"
if [ -f "Dockerfile.api" ]; then
    # Create a temporary test
    start_time=$(date +%s)
    
    # Do a dry run build (without pushing)
    echo "Building API image..."
    if docker build -f Dockerfile.api -t think-ai-api-test . >/dev/null 2>&1; then
        end_time=$(date +%s)
        build_time=$((end_time - start_time))
        
        if [ $build_time -lt 30 ]; then
            echo -e "${GREEN}✓${NC} Build completed in ${build_time} seconds"
        else
            echo -e "${YELLOW}!${NC} Build took ${build_time} seconds (target: <30s)"
            echo "  Ensure base image is being used correctly"
        fi
    else
        echo -e "${RED}✗${NC} Build failed"
    fi
else
    echo -e "${RED}✗${NC} Dockerfile.api not found"
fi

# Check railway.json configuration
echo -e "\n${YELLOW}Checking Railway configuration...${NC}"
if grep -q "Dockerfile.api" railway.json; then
    echo -e "${GREEN}✓${NC} railway.json uses Dockerfile.api"
else
    echo -e "${RED}✗${NC} railway.json doesn't use Dockerfile.api"
fi

if grep -q "BASE_IMAGE" railway.json; then
    echo -e "${GREEN}✓${NC} railway.json has BASE_IMAGE buildArg"
else
    echo -e "${YELLOW}!${NC} railway.json missing BASE_IMAGE buildArg"
fi

# Summary
echo -e "\n${GREEN}=========================================${NC}"
echo -e "${GREEN}Verification Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Update 'yourusername' in all config files"
echo "2. Run: ./build_and_push_base.sh"
echo "3. Deploy to Railway"
echo ""
echo "Expected deployment time: <10 seconds"