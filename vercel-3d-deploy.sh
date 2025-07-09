#!/bin/bash

# Script to deploy 3D webapp to Vercel with GPU server configuration

echo "🚀 Deploying Think AI 3D Webapp to Vercel..."

# Create a temporary deployment directory
DEPLOY_DIR="/tmp/think-ai-3d-deploy"
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

# Copy the 3D webapp HTML
cp /home/champi/Dev/think_ai/minimal_3d.html $DEPLOY_DIR/index.html

# Modify the API endpoints to use the GPU server
sed -i "s|fetch('/api/|fetch('http://69.197.178.37:8080/api/|g" $DEPLOY_DIR/index.html
sed -i "s|window.location.origin + '/api/|'http://69.197.178.37:8080/api/|g" $DEPLOY_DIR/index.html

# Add CORS proxy configuration for Vercel
cat > $DEPLOY_DIR/vercel.json << 'EOF'
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "http://69.197.178.37:8080/api/:path*"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Access-Control-Allow-Methods",
          "value": "GET, POST, PUT, DELETE, OPTIONS"
        },
        {
          "key": "Access-Control-Allow-Headers",
          "value": "Content-Type, Authorization"
        }
      ]
    }
  ]
}
EOF

# Copy static assets
mkdir -p $DEPLOY_DIR/icons
if [ -d "/home/champi/Dev/think_ai/think-ai-webapp/static/icons" ]; then
    cp -r /home/champi/Dev/think_ai/think-ai-webapp/static/icons/* $DEPLOY_DIR/icons/
fi

# Copy manifest and service worker
if [ -f "/home/champi/Dev/think_ai/think-ai-webapp/static/manifest.json" ]; then
    cp /home/champi/Dev/think_ai/think-ai-webapp/static/manifest.json $DEPLOY_DIR/
fi

if [ -f "/home/champi/Dev/think_ai/think-ai-webapp/static/sw.js" ]; then
    cp /home/champi/Dev/think_ai/think-ai-webapp/static/sw.js $DEPLOY_DIR/
fi

# Deploy to Vercel
cd $DEPLOY_DIR
vercel --prod

echo "✅ Deployment complete!"
echo "📍 GPU Server: http://69.197.178.37:8080"
echo "🌐 Check your Vercel deployment URL above"