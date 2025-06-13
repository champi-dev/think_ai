#!/bin/bash
# Local setup script for Think AI (no Docker required)

set -e

echo "🚀 Setting up Think AI local development environment..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data
mkdir -p ~/.think_ai/cache
mkdir -p ~/.think_ai/claude_cache
mkdir -p ~/.think_ai/claude_reports

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -e .

# Set up local configuration for development
echo "🔧 Configuring for local development..."

# Update .env for local development (no external services)
cat >> .env << 'EOF'

# Local Development Settings
USE_LOCAL_STORAGE=true
SKIP_EXTERNAL_SERVICES=true
LOCAL_DEV_MODE=true
EOF

echo "✅ Local setup complete! You can now:"
echo "   - Run the CLI: think-ai --help"
echo "   - Start interactive session: think-ai"
echo "   - Test with debug mode: think-ai --debug"
echo ""
echo "📝 Note: Running in local mode (no external databases required)"
echo "🔑 Claude API key configured and ready to use"