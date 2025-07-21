#!/bin/bash

# ThinkAI Production Deployment Script
# This script builds and deploys the production-ready binary

set -e

echo "🚀 ThinkAI Production Deployment"
echo "================================"

# Load environment variables from .env.production
if [ -f .env.production ]; then
    echo "📋 Loading environment from .env.production"
    export $(cat .env.production | grep -v '^#' | xargs)
else
    echo "⚠️  Warning: .env.production not found"
    echo "   Please ensure environment variables are set"
fi

# Build the production binary
echo "🔨 Building production binary..."
cargo build --release --bin think-ai-full-production

# Check if build succeeded
if [ ! -f target/release/think-ai-full-production ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"

# Create deployment directory if needed
DEPLOY_DIR="${DEPLOY_DIR:-/opt/thinkai}"
echo "📁 Deployment directory: $DEPLOY_DIR"

# Check if we need sudo
if [ -w "$DEPLOY_DIR" ]; then
    SUDO=""
else
    SUDO="sudo"
    echo "🔒 Need sudo for deployment directory"
fi

# Copy binary
echo "📦 Copying binary..."
$SUDO mkdir -p "$DEPLOY_DIR"
$SUDO cp target/release/think-ai-full-production "$DEPLOY_DIR/"
$SUDO chmod +x "$DEPLOY_DIR/think-ai-full-production"

# Copy static files
echo "📄 Copying static files..."
$SUDO mkdir -p "$DEPLOY_DIR/full-system"
$SUDO cp -r full-system/static "$DEPLOY_DIR/full-system/"

# Create audio cache directory
echo "🔊 Creating audio cache directory..."
$SUDO mkdir -p "$DEPLOY_DIR/audio_cache"
$SUDO chmod 777 "$DEPLOY_DIR/audio_cache"

# Create systemd service
if [ "$1" == "--systemd" ]; then
    echo "🔧 Installing systemd service..."
    cat <<EOF | $SUDO tee /etc/systemd/system/thinkai.service
[Unit]
Description=ThinkAI Production Server
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$DEPLOY_DIR
Environment="DEEPGRAM_API_KEY=${DEEPGRAM_API_KEY}"
Environment="ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}"
Environment="AUDIO_CACHE_DIR=$DEPLOY_DIR/audio_cache"
Environment="PORT=${PORT:-7777}"
Environment="RUST_LOG=info"
ExecStart=$DEPLOY_DIR/think-ai-full-production
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    $SUDO systemctl daemon-reload
    $SUDO systemctl enable thinkai
    echo "✅ Systemd service installed"
    echo "   Start with: sudo systemctl start thinkai"
    echo "   Check logs: sudo journalctl -u thinkai -f"
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "To run manually:"
echo "  cd $DEPLOY_DIR"
echo "  ./think-ai-full-production"
echo ""
echo "To run with systemd:"
echo "  sudo systemctl start thinkai"
echo "  sudo systemctl status thinkai"
echo ""
echo "📊 Access dashboard at: http://localhost:${PORT:-7777}/stats"