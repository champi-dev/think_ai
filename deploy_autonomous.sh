#!/bin/bash

# Deploy ThinkAI with Autonomous Agent to Production

echo "🚀 Deploying ThinkAI Autonomous Agent to Production"
echo "================================================="

# Check if running on production server
if [[ ! -f /opt/thinkai/think-ai-full-production ]]; then
    echo "❌ Error: Not on production server"
    echo "This script should be run on the production server"
    exit 1
fi

# Stop current service
echo "📦 Stopping current service..."
sudo systemctl stop thinkai

# Backup current binary
echo "💾 Creating backup..."
sudo cp /opt/thinkai/think-ai-full-production /opt/thinkai/think-ai-full-production.backup.$(date +%Y%m%d_%H%M%S)

# Build new binary with autonomous capabilities
echo "🔨 Building autonomous binary..."
cd /home/champi/Dev/think_ai
cargo build --release --bin think-ai-autonomous

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

# Copy new binary
echo "📋 Deploying new binary..."
sudo cp target/release/think-ai-autonomous /opt/thinkai/think-ai-full-production

# Update static files
echo "📄 Updating static files..."
sudo cp -r full-system/static/* /opt/thinkai/full-system/static/
sudo cp docs/AUTONOMOUS_AGENT.md /opt/thinkai/docs/

# Set permissions
sudo chmod +x /opt/thinkai/think-ai-full-production

# Create systemd service for autonomous agent if it doesn't exist
if [[ ! -f /etc/systemd/system/thinkai-autonomous.service ]]; then
    echo "🔧 Creating autonomous agent service..."
    sudo tee /etc/systemd/system/thinkai-autonomous.service > /dev/null <<EOF
[Unit]
Description=ThinkAI Autonomous Agent
After=network.target

[Service]
Type=simple
User=thinkai
WorkingDirectory=/opt/thinkai
Environment="RUST_LOG=info"
Environment="PORT=7777"
Environment="ENABLE_AUTONOMOUS=true"
Environment="AUTONOMOUS_WORKERS=4"
Environment="DEEPGRAM_API_KEY=${DEEPGRAM_API_KEY}"
Environment="ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}"
Environment="ENABLE_AUDIO=true"
Environment="ENABLE_WHATSAPP=false"
ExecStart=/opt/thinkai/think-ai-full-production
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
fi

# Reload systemd
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

# Start service
echo "▶️ Starting autonomous agent..."
sudo systemctl start thinkai
sudo systemctl enable thinkai

# Check status
echo "✅ Checking service status..."
sudo systemctl status thinkai --no-pager

# Test endpoints
echo "🧪 Testing endpoints..."
sleep 3

# Test health
echo "Testing health endpoint..."
curl -s http://localhost:7777/health | jq .

# Test autonomous status
echo "Testing autonomous status..."
curl -s http://localhost:7777/api/autonomous/status | jq .

# Test metrics
echo "Testing metrics..."
curl -s http://localhost:7777/api/metrics | jq '.system_metrics | {total_requests, cpu_usage, memory_usage}'

echo ""
echo "✅ Deployment complete!"
echo "📊 Dashboard: https://thinkai.lat/stats"
echo "🤖 Autonomous Status: https://thinkai.lat/api/autonomous/status"
echo ""
echo "To view logs: sudo journalctl -u thinkai -f"