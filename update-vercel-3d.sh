#!/bin/bash

# Update Vercel deployment with 3D visualization webapp

echo "🚀 Updating Vercel deployment with 3D visualization webapp..."

# Clean and prepare vercel-deploy directory
echo "📦 Preparing deployment directory..."
rm -rf vercel-deploy/index.html
rm -rf vercel-deploy/script.js
rm -rf vercel-deploy/style.css

# Copy the 3D visualization webapp
echo "🎨 Copying 3D visualization webapp..."
cp fullstack_3d.html vercel-deploy/index.html

# Update API endpoint in the HTML to use relative path for Vercel proxy
echo "🔧 Updating API endpoints for Vercel proxy..."
sed -i 's|http://69.197.178.37:8080/api/|/api/|g' vercel-deploy/index.html
sed -i 's|ws://69.197.178.37:8080/ws|wss://think-ai.vercel.app/ws|g' vercel-deploy/index.html

# Ensure Three.js is loaded from CDN
echo "📚 Verifying Three.js CDN links..."
if ! grep -q "cdn.jsdelivr.net/npm/three" vercel-deploy/index.html; then
    # Add Three.js CDN if not present
    sed -i '/<\/head>/i \    <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>' vercel-deploy/index.html
fi

# Create a proper manifest.json for the 3D webapp
echo "📋 Updating PWA manifest..."
cat > vercel-deploy/manifest.json << 'EOF'
{
  "name": "Think AI - Quantum Consciousness",
  "short_name": "Think AI 3D",
  "description": "Revolutionary O(1) consciousness with 3D visualization",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#000000",
  "theme_color": "#6366f1",
  "orientation": "any",
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
EOF

# Update vercel.json to handle WebSocket properly
echo "⚙️ Updating Vercel configuration..."
cat > vercel-deploy/vercel.json << 'EOF'
{
  "name": "think-ai-3d-webapp",
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "http://69.197.178.37:8080/api/$1"
    },
    {
      "source": "/ws",
      "destination": "http://69.197.178.37:8080/ws"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "SAMEORIGIN"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        },
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
    },
    {
      "source": "/sw.js",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "no-cache"
        },
        {
          "key": "Service-Worker-Allowed",
          "value": "/"
        }
      ]
    }
  ],
  "buildCommand": "",
  "outputDirectory": ".",
  "framework": null
}
EOF

echo "✅ Vercel deployment updated with 3D visualization webapp!"
echo ""
echo "📌 Next steps:"
echo "1. cd vercel-deploy"
echo "2. vercel --prod"
echo ""
echo "The 3D visualization webapp should now be properly deployed!"