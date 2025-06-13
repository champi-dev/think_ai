#!/bin/bash

set -e

echo "🚀 Installing Think AI Web Application Services..."

# Check if running as root/sudo
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run with sudo: sudo $0"
    exit 1
fi

# Create required directories
echo "📁 Creating directories..."
mkdir -p /var/log/think-ai
mkdir -p /var/run/think-ai
chown -R $SUDO_USER:$SUDO_USER /var/log/think-ai /var/run/think-ai

# Build Go server
echo "🔨 Building Go API server..."
cd server
go mod download
go build -o bin/think-ai-api cmd/api/main.go
chmod +x bin/think-ai-api
cd ..

# Install Python dependencies for bridge
echo "📦 Installing Python dependencies..."
pip3 install daemon pid

# Copy systemd service files
echo "📋 Installing systemd services..."
cp systemd/*.service /etc/systemd/system/
systemctl daemon-reload

# Enable services
echo "✅ Enabling services..."
systemctl enable think-ai-core.service
systemctl enable think-ai-api.service

echo "
✨ Installation complete!

Start services with:
  sudo systemctl start think-ai-core
  sudo systemctl start think-ai-api

Monitor services:
  sudo systemctl status think-ai-core
  sudo systemctl status think-ai-api

View logs:
  sudo journalctl -u think-ai-core -f
  sudo journalctl -u think-ai-api -f

Health check:
  curl http://localhost:8888/health
  curl http://localhost:8080/api/v1/health

Web interface will be available at:
  http://localhost:3000 (after webapp is built)
"