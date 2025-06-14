#!/bin/bash
# Start the full Think AI distributed system

set -e

echo "🤖 Think AI Full System Launcher"
echo "================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo ""
    echo "To install Docker Desktop on Mac:"
    echo ""
    echo "1. Using Homebrew (recommended):"
    echo "   brew install --cask docker"
    echo ""
    echo "2. Or download directly:"
    echo "   https://www.docker.com/products/docker-desktop/"
    echo ""
    echo "After installing Docker:"
    echo "1. Open Docker Desktop"
    echo "2. Wait for it to start"
    echo "3. Run this script again"
    echo ""
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "⚠️  Docker is installed but not running!"
    echo ""
    echo "Please:"
    echo "1. Open Docker Desktop"
    echo "2. Wait for the whale icon to appear in your menu bar"
    echo "3. Run this script again"
    echo ""
    exit 1
fi

echo "✅ Docker is ready"
echo ""

# Check if docker-compose.full.yml exists
if [ ! -f "docker-compose.full.yml" ]; then
    echo "❌ docker-compose.full.yml not found!"
    echo "Make sure you're running this from the Think AI directory"
    exit 1
fi

# Option to choose
echo "What would you like to do?"
echo "1) Start full distributed system (recommended)"
echo "2) Install and start full system"
echo "3) Stop all services"
echo "4) View service logs"
echo "5) Check service health"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting distributed services..."
        docker-compose -f docker-compose.full.yml up -d
        
        echo ""
        echo "⏳ Waiting for services to be ready..."
        sleep 10
        
        echo ""
        echo "📊 Service Status:"
        docker-compose -f docker-compose.full.yml ps
        
        echo ""
        echo "✅ Services started!"
        echo ""
        echo "Now run: python full_system_cli.py"
        ;;
        
    2)
        echo ""
        echo "📦 Running full installation..."
        ./scripts/install_docker_mac.sh
        ;;
        
    3)
        echo ""
        echo "🛑 Stopping all services..."
        docker-compose -f docker-compose.full.yml down
        echo "✅ All services stopped"
        ;;
        
    4)
        echo ""
        echo "📋 Showing logs (Ctrl+C to exit)..."
        docker-compose -f docker-compose.full.yml logs -f
        ;;
        
    5)
        echo ""
        echo "🏥 Checking service health..."
        docker-compose -f docker-compose.full.yml ps
        echo ""
        
        # Test each service
        echo "Testing ScyllaDB..."
        docker exec think_ai_scylla cqlsh -e "DESCRIBE keyspaces" &> /dev/null && echo "✅ ScyllaDB: Healthy" || echo "❌ ScyllaDB: Not responding"
        
        echo "Testing Redis..."
        docker exec think_ai_redis redis-cli PING &> /dev/null && echo "✅ Redis: Healthy" || echo "❌ Redis: Not responding"
        
        echo "Testing Neo4j..."
        curl -s http://localhost:7474 &> /dev/null && echo "✅ Neo4j: Healthy" || echo "❌ Neo4j: Not responding"
        
        echo "Testing Milvus..."
        curl -s http://localhost:19530/health &> /dev/null && echo "✅ Milvus: Healthy" || echo "❌ Milvus: Not responding"
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac