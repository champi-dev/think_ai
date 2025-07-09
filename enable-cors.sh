#!/bin/bash
# Run this on the GPU server to enable CORS for Vercel

# Add CORS headers to Think AI HTTP server
# This allows the Vercel frontend to communicate with GPU backend

echo "Enabling CORS for Vercel deployment..."

# Find your Vercel URL after deployment and update this
VERCEL_URL="https://think-ai-webapp.vercel.app"

# Add to your Think AI startup script or environment
export THINK_AI_CORS_ORIGIN="$VERCEL_URL"
export THINK_AI_CORS_ENABLED=true

echo "CORS enabled for: $VERCEL_URL"
echo "Restart Think AI services for changes to take effect"
