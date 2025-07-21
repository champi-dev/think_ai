#!/bin/bash

# Rebuild and Deploy ThinkAI Production

set -e

echo "🔨 Building new production binary..."
echo "=================================="

# Clean old build
echo "🧹 Cleaning old build artifacts..."
cargo clean --release --package think-ai-full

# Build new production binary
echo "🏗️  Building think-ai-full-production..."
cargo build --release --bin think-ai-full-production

if [ ! -f "target/release/think-ai-full-production" ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"
echo ""

# Check current systemd status
echo "📊 Current service status:"
sudo systemctl status thinkai --no-pager || true
echo ""

# Stop the service
echo "🛑 Stopping ThinkAI service..."
sudo systemctl stop thinkai

# Wait a moment for clean shutdown
sleep 2

# Copy new binary
echo "📦 Deploying new binary..."
sudo cp target/release/think-ai-full-production /opt/thinkai/think-ai-full-production
sudo chmod +x /opt/thinkai/think-ai-full-production

# Copy updated static files (including new dashboard)
echo "📄 Updating static files..."
sudo cp -r full-system/static/* /opt/thinkai/full-system/static/

# Clear systemd cache and reload
echo "🔄 Reloading systemd configuration..."
sudo systemctl daemon-reload

# Start the service
echo "🚀 Starting ThinkAI service with new binary..."
sudo systemctl start thinkai

# Wait for startup
sleep 3

# Check if service started successfully
if sudo systemctl is-active --quiet thinkai; then
    echo "✅ Service started successfully!"
else
    echo "❌ Service failed to start!"
    echo "Checking logs..."
    sudo journalctl -u thinkai -n 50 --no-pager
    exit 1
fi

# Show service status
echo ""
echo "📊 New service status:"
sudo systemctl status thinkai --no-pager

# Test endpoints
echo ""
echo "🧪 Testing endpoints..."
echo -n "Health check: "
if curl -s -f http://localhost:7777/health > /dev/null; then
    echo "✅ OK"
else
    echo "❌ Failed"
fi

echo -n "Metrics API: "
if curl -s -f http://localhost:7777/api/metrics > /dev/null; then
    echo "✅ OK"
    echo "Current metrics:"
    curl -s http://localhost:7777/api/metrics | jq -r '.system_metrics | "- Requests: \(.total_requests)\n- CPU: \(.cpu_usage)%\n- Memory: \(.memory_usage)%"'
else
    echo "❌ Failed"
fi

echo -n "Dashboard: "
if curl -s -f http://localhost:7777/stats > /dev/null; then
    echo "✅ OK"
else
    echo "❌ Failed"
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📊 View dashboard: https://thinkai.lat/stats"
echo "📝 View logs: sudo journalctl -u thinkai -f"