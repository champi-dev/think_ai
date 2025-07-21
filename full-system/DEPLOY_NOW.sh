#!/bin/bash

# Quick deployment commands for ThinkAI production

echo "🚀 ThinkAI Production Deployment Commands"
echo "========================================"
echo ""
echo "Run these commands on your production server:"
echo ""
echo "1. First, copy the built binary to your server:"
echo "   scp target/release/think-ai-full-production your-server:/opt/thinkai/"
echo ""
echo "2. Copy static files:"
echo "   scp -r full-system/static your-server:/opt/thinkai/full-system/"
echo ""
echo "3. SSH to your server and run:"
cat << 'EOF'

# On production server:
cd /opt/thinkai

# Set environment variables
export DEEPGRAM_API_KEY="e31341c95ee93fd2c8fced1bf37636f042fe038b"
export ELEVENLABS_API_KEY="sk_aa595f99bc5842b5df837d4c47fe3a18ce00b9a39a0f2877"
export AUDIO_CACHE_DIR="./audio_cache"
export PORT="7777"

# Create audio cache directory
mkdir -p audio_cache

# Stop old service if running
sudo systemctl stop thinkai

# Make binary executable
chmod +x think-ai-full-production

# Test run first
./think-ai-full-production

# If it works, Ctrl+C and install as service:
sudo tee /etc/systemd/system/thinkai.service << 'SERVICE'
[Unit]
Description=ThinkAI Production Server
After=network.target

[Service]
Type=simple
User=thinkai
WorkingDirectory=/opt/thinkai
Environment="DEEPGRAM_API_KEY=e31341c95ee93fd2c8fced1bf37636f042fe038b"
Environment="ELEVENLABS_API_KEY=sk_aa595f99bc5842b5df837d4c47fe3a18ce00b9a39a0f2877"
Environment="AUDIO_CACHE_DIR=/opt/thinkai/audio_cache"
Environment="PORT=7777"
Environment="RUST_LOG=info"
ExecStart=/opt/thinkai/think-ai-full-production
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable thinkai
sudo systemctl start thinkai

# Check status
sudo systemctl status thinkai

# Check logs
sudo journalctl -u thinkai -f

EOF

echo ""
echo "4. Verify deployment:"
echo "   curl https://thinkai.lat/health"
echo "   curl https://thinkai.lat/api/metrics"
echo ""
echo "5. Monitor dashboard:"
echo "   https://thinkai.lat/stats"