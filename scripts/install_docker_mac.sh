#!/bin/bash
# Install Docker Desktop on macOS and start the full Think AI system

set -e

echo "🤖 Think AI Full System Setup"
echo "============================"
echo ""

# Check if Docker is already installed
if command -v docker &> /dev/null; then
    echo "✅ Docker is already installed"
    docker --version
else
    echo "📦 Docker Desktop needs to be installed"
    echo ""
    echo "Please install Docker Desktop for Mac:"
    echo ""
    echo "1. Visit: https://www.docker.com/products/docker-desktop/"
    echo "2. Download Docker Desktop for Mac (Apple Silicon)"
    echo "3. Install and start Docker Desktop"
    echo "4. Run this script again after Docker is running"
    echo ""
    echo "Alternatively, you can install via Homebrew:"
    echo "  brew install --cask docker"
    echo ""
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is installed but not running"
    echo "Please start Docker Desktop and run this script again"
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p data/{scylla,redis,milvus,neo4j,etcd,minio}
mkdir -p logs

# Check system resources
echo "🔍 Checking system resources..."
TOTAL_MEM=$(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024}')
echo "Total RAM: ${TOTAL_MEM}GB"

if (( $(echo "$TOTAL_MEM < 8" | bc -l) )); then
    echo "⚠️  Warning: System has less than 8GB RAM. Services may run slowly."
    echo "   Continuing anyway as you mentioned 6-8GB is fine..."
fi

# Pull all required images
echo ""
echo "📥 Pulling Docker images (this may take a while)..."
docker-compose -f docker-compose.full.yml pull

# Initialize configuration
echo ""
echo "🔧 Initializing configuration..."
cp config/full_system.yaml config/active.yaml

# Start services
echo ""
echo "🚀 Starting all services..."
docker-compose -f docker-compose.full.yml up -d

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.full.yml ps

# Initialize databases
echo ""
echo "🗄️ Initializing databases..."
./scripts/init_databases.sh

echo ""
echo "✅ Think AI Full System is ready!"
echo ""
echo "Services running:"
echo "  - ScyllaDB: localhost:9042"
echo "  - Redis: localhost:6379" 
echo "  - Milvus: localhost:19530"
echo "  - Neo4j: localhost:7474 (browser), localhost:7687 (bolt)"
echo ""
echo "Neo4j credentials: neo4j / think_ai_2024"
echo ""
echo "To stop all services: docker-compose -f docker-compose.full.yml down"
echo "To view logs: docker-compose -f docker-compose.full.yml logs -f"