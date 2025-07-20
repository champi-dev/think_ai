#!/bin/bash

echo "🔄 Restarting Think AI Service..."

# Copy service file
sudo cp think-ai.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Stop the service
sudo systemctl stop think-ai

# Start the service
sudo systemctl start think-ai

# Check status
sleep 2
sudo systemctl status think-ai --no-pager

echo ""
echo "📊 Service logs (last 20 lines):"
sudo journalctl -u think-ai -n 20 --no-pager

echo ""
echo "🌐 Testing endpoints:"
echo "- Health check: http://localhost:7777/health"
echo "- API docs: http://localhost:7777/api-docs"
echo "- Metrics dashboard: http://localhost:7777/stats"

# Test health endpoint
echo ""
echo "🏥 Health check result:"
curl -s http://localhost:7777/health || echo "❌ Service not responding yet"