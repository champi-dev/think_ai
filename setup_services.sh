#!/bin/bash

echo "🧠 THINK AI - SERVICE SETUP"
echo "==========================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Docker is installed
if ! command_exists docker; then
    echo -e "${YELLOW}Docker is not installed. Would you like to install it? (y/n)${NC}"
    read -r response
    
    if [[ "$response" == "y" ]]; then
        echo "Installing Docker..."
        
        # Detect OS
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Install Docker on Ubuntu/Debian
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
            sudo usermod -aG docker $USER
            rm get-docker.sh
            
            echo -e "${GREEN}Docker installed! Please log out and back in for group changes to take effect.${NC}"
            echo "Then run this script again."
            exit 0
            
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
            exit 1
        else
            echo "Please install Docker manually for your OS"
            exit 1
        fi
    else
        echo -e "${YELLOW}Think AI can run without distributed databases, but with limited features.${NC}"
        echo "To run without Docker, just use: ./launch_consciousness.sh"
        exit 0
    fi
fi

# Check if docker-compose exists
if ! command_exists docker-compose; then
    echo "Installing docker-compose..."
    sudo apt-get update
    sudo apt-get install -y docker-compose
fi

echo -e "${GREEN}✓ Docker is installed${NC}"

# Check if user can run Docker without sudo
if ! docker ps >/dev/null 2>&1; then
    echo -e "${YELLOW}You need to run Docker commands with sudo or add your user to the docker group.${NC}"
    echo "Run: sudo usermod -aG docker $USER && newgrp docker"
    echo "Then log out and back in."
    
    # Try with sudo
    echo "Attempting to start services with sudo..."
    DOCKER_CMD="sudo docker-compose"
else
    DOCKER_CMD="docker-compose"
fi

# Start services
echo ""
echo "Starting Think AI distributed services..."
echo "This will run:"
echo "  • ScyllaDB (distributed database) on port 9042"
echo "  • Redis (cache) on port 6379"
echo "  • Milvus (vector search) on port 19530"
echo "  • Neo4j (knowledge graph) on port 7687"
echo ""

# Pull images first
echo "Pulling Docker images (this may take a few minutes)..."
$DOCKER_CMD pull scylladb/scylla:latest
$DOCKER_CMD pull redis:7-alpine
$DOCKER_CMD pull milvusdb/milvus:v2.3.0
$DOCKER_CMD pull neo4j:5-community

# Start services
echo "Starting services..."
$DOCKER_CMD up -d

# Wait for services to be healthy
echo ""
echo "Waiting for services to be ready..."
sleep 5

# Check service status
echo ""
echo "Service Status:"
$DOCKER_CMD ps

echo ""
echo -e "${GREEN}✅ Services are starting up!${NC}"
echo ""
echo "It may take 30-60 seconds for all services to be fully ready."
echo "You can check status with: $DOCKER_CMD ps"
echo "View logs with: $DOCKER_CMD logs -f [service-name]"
echo ""
echo "Once ready, run: ./launch_consciousness.sh"
echo ""
echo "To stop services later: $DOCKER_CMD down"