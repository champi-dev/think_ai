#!/bin/bash
# Deploy to Railway

echo "Deploying Think AI v3.1.0 to Railway..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Railway CLI not found. Install it from: https://docs.railway.app/develop/cli"
    exit 1
fi

# Deploy
railway up

echo "Deployment complete! Check Railway dashboard for status."
