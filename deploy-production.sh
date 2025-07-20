#!/bin/bash

echo "🚀 Deploying Think AI to Production..."
echo

# Stop the service
echo "🛑 Stopping think-ai service..."
sudo systemctl stop think-ai

# Copy the updated service file
echo "📋 Updating service configuration..."
sudo cp think-ai.service /etc/systemd/system/

# Reload systemd
echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload

# Start the service
echo "▶️  Starting think-ai service..."
sudo systemctl start think-ai

# Enable on boot
sudo systemctl enable think-ai

# Wait for service to start
echo "⏳ Waiting for service to start..."
sleep 5

# Check status
echo "📊 Service status:"
sudo systemctl status think-ai --no-pager

# Test local endpoints
echo
echo "🧪 Testing local endpoints:"
echo -n "Health check: "
curl -s http://localhost:7777/health && echo " ✅" || echo " ❌"

echo -n "API docs: "
curl -s http://localhost:7777/api-docs.html | grep -q "Think AI API" && echo " ✅" || echo " ❌"

echo -n "Stats dashboard: "
curl -s http://localhost:7777/stats | grep -q "Metrics Dashboard" && echo " ✅" || echo " ❌"

# Test production
echo
echo "🌐 Testing production (thinkai.lat):"
echo -n "Health check: "
curl -s https://thinkai.lat/health && echo " ✅" || echo " ❌"

echo -n "API docs: "
curl -s https://thinkai.lat/api-docs.html | grep -q "Think AI API" && echo " ✅" || echo " ❌"

echo -n "Stats dashboard: "
curl -s https://thinkai.lat/stats | grep -q "Metrics Dashboard" && echo " ✅" || echo " ❌"

echo
echo "📝 Recent logs:"
sudo journalctl -u think-ai -n 20 --no-pager

echo
echo "✅ Deployment complete!"
echo
echo "🔗 Production URLs:"
echo "   Main app: https://thinkai.lat"
echo "   API docs: https://thinkai.lat/api-docs.html"
echo "   Metrics: https://thinkai.lat/stats"