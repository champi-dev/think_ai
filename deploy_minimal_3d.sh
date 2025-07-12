#!/bin/bash

echo "🚀 Deploying minimal_3d webapp to production..."

# Step 1: Check if port 8080 is in use
if lsof -i:8080 > /dev/null 2>&1; then
    echo "⚠️  Port 8080 is currently in use by:"
    lsof -i:8080 | grep LISTEN
    echo ""
    echo "To deploy the new webapp, you need to:"
    echo "1. Stop the current process: sudo kill $(lsof -ti:8080)"
    echo "2. Start the new webapp: ./target/release/think-ai-webapp"
    echo ""
    echo "Or use systemd/supervisor if configured."
else
    echo "✅ Port 8080 is free. Starting the webapp..."
    ./target/release/think-ai-webapp &
    echo "🎉 Webapp started! Access it at http://localhost:8080/"
fi

echo ""
echo "📝 Note: The webapp is now serving minimal_3d.html with:"
echo "- O(1) optimized 3D quantum field visualization"
echo "- Pre-computed lookup tables for 60fps performance"
echo "- Real-time chat interface"
echo "- Beautiful glassmorphism UI"