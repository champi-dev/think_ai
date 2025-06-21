#!/bin/bash
# Quick setup script for O(1) Railway deployments

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🚀 Think AI O(1) Deployment Setup${NC}"
echo "===================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker not found. Please install Docker first.${NC}"
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Get Docker Hub username
echo -e "${BLUE}Step 1: Docker Hub Configuration${NC}"
read -p "Enter your Docker Hub username: " DOCKER_USERNAME

if [ -z "$DOCKER_USERNAME" ]; then
    echo "Docker Hub username is required!"
    exit 1
fi

# Update all config files with the username
echo -e "${YELLOW}Updating configuration files...${NC}"
find . -name "*.json" -o -name "Dockerfile.*" -o -name "*.yml" | while read file; do
    if [[ "$file" != *"node_modules"* ]]; then
        sed -i.bak "s/yourusername/$DOCKER_USERNAME/g" "$file" 2>/dev/null || true
    fi
done

# Login to Docker Hub
echo -e "${BLUE}Step 2: Docker Hub Login${NC}"
docker login

# Build and push base image
echo -e "${BLUE}Step 3: Building Base Image${NC}"
echo -e "${YELLOW}This will take 15-20 minutes the first time...${NC}"
./build_and_push_base.sh

echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Commit and push your changes to GitHub"
echo "2. Connect your Railway project to the GitHub repo"
echo "3. Deploy! Your builds will now take <10 seconds"
echo ""
echo -e "${YELLOW}Important:${NC}"
echo "- Base image: ${DOCKER_USERNAME}/think-ai-base:latest"
echo "- Rebuild base image when requirements-full.txt changes"
echo "- Monitor first deployment to ensure everything works"