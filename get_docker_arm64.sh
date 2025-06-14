#!/bin/bash
# Get the correct Docker Desktop for Apple Silicon

echo "🍎 Getting Docker Desktop for Apple Silicon (ARM64)"
echo "=================================================="
echo ""

# Close any open DMG
echo "Closing Intel Docker DMG..."
osascript -e 'tell application "Finder" to close every window whose name contains "Docker"' 2>/dev/null || true

# Download URL for Apple Silicon version
ARM64_URL="https://desktop.docker.com/mac/main/arm64/Docker.dmg"

echo "📥 Downloading Docker Desktop for Apple Silicon..."
echo "   This may take a few minutes..."
echo ""

# Download to a specific location
DOWNLOAD_PATH="$HOME/Downloads/Docker-arm64.dmg"

# Download with curl showing progress
curl -L -# -o "$DOWNLOAD_PATH" "$ARM64_URL"

if [ -f "$DOWNLOAD_PATH" ]; then
    echo ""
    echo "✅ Download complete!"
    echo ""
    echo "📦 Opening Docker installer..."
    open "$DOWNLOAD_PATH"
    
    echo ""
    echo "Installation steps:"
    echo "1. ✅ The correct ARM64 version is now open"
    echo "2. 🖱️  Drag Docker.app to Applications"
    echo "3. 🚀 Open Docker from Applications"
    echo "4. ⏳ Wait for Docker to start"
    echo "5. 🎉 Run: ./start_full_system.sh"
else
    echo "❌ Download failed"
    echo ""
    echo "Please download manually:"
    echo "1. Visit: https://www.docker.com/products/docker-desktop/"
    echo "2. Click 'Download for Mac'"
    echo "3. Choose 'Mac with Apple chip' (IMPORTANT!)"
fi