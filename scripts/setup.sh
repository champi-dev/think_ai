#!/bin/bash
# Setup script for Think AI development environment

set -e

echo "🚀 Setting up Think AI development environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service health
echo "🏥 Checking service health..."
docker-compose ps

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -e ".[dev]"

# Initialize the system
echo "🔧 Initializing Think AI system..."
python -m think_ai.cli init

echo "✅ Setup complete! You can now:"
echo "   - Run the CLI: think-ai --help"
echo "   - Launch the TUI: think-ai tui"
echo "   - Run the example: python example.py"
echo ""
echo "Services running:"
echo "   - ScyllaDB: localhost:9042"
echo "   - Redis: localhost:6379"
echo "   - Milvus: localhost:19530"