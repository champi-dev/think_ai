#!/bin/bash
# Run Think AI with GPU support locally

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 Starting Think AI with GPU support...${NC}"

# Check if NVIDIA Docker runtime is installed
if ! docker info | grep -q nvidia; then
    echo -e "${RED}❌ NVIDIA Docker runtime not found!${NC}"
    echo "Please install nvidia-docker2:"
    echo "  sudo apt-get install nvidia-docker2"
    echo "  sudo systemctl restart docker"
    exit 1
fi

# Check if NVIDIA GPU is available
if ! nvidia-smi &> /dev/null; then
    echo -e "${RED}❌ NVIDIA GPU not detected!${NC}"
    echo "Make sure you have NVIDIA drivers installed"
    exit 1
fi

echo -e "${YELLOW}GPU Info:${NC}"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader

# Build GPU image
echo -e "${YELLOW}Building GPU-enabled Docker image...${NC}"
DOCKER_BUILDKIT=1 docker build -t think-ai:gpu -f Dockerfile.gpu .

# Start services with GPU support
echo -e "${YELLOW}Starting services...${NC}"
docker-compose -f docker-compose.gpu.yml up -d

# Wait for services to be ready
echo -e "${YELLOW}Waiting for services to start...${NC}"
sleep 10

# Test GPU availability in container
echo -e "${YELLOW}Testing GPU access in container...${NC}"
docker exec think-ai-gpu python -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA device: {torch.cuda.get_device_name(0)}')
    print(f'CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB')
"

echo -e "${GREEN}✅ Think AI is running with GPU support!${NC}"
echo -e "API available at: http://localhost:8080"
echo -e "To view logs: docker-compose -f docker-compose.gpu.yml logs -f"
echo -e "To stop: docker-compose -f docker-compose.gpu.yml down"