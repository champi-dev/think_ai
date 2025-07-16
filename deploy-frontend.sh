#!/bin/bash
# Deploy script for Think AI frontend with cache busting

set -e

echo "Building frontend with Vite..."
cd /home/administrator/think_ai/frontend
npm run build

echo "Restarting backend service..."
sudo systemctl restart think-ai-full.service

echo "Waiting for service to start..."
sleep 2

echo "Testing deployment..."
if curl -s http://localhost:8080/health | grep -q "OK"; then
    echo "✓ Service is healthy"
else
    echo "✗ Service health check failed"
    exit 1
fi

echo "Deployment complete!"
echo "Cache-busted assets have been deployed with content hashes."