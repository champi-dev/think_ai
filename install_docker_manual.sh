#!/bin/bash
# Manual Docker Desktop installation script

echo "🐳 Docker Desktop Manual Installation"
echo "===================================="
echo ""

# Check if we have the DMG file
DMG_PATH="$HOME/Library/Caches/Homebrew/downloads/21c9e82e0f2171553a10f3236a42ec1878115743c99b1f6e2c38bc8305e36f35--Docker.dmg"

if [ -f "$DMG_PATH" ]; then
    echo "✅ Found Docker DMG file"
    echo ""
    echo "To install Docker Desktop manually:"
    echo ""
    echo "1. Double-click to open:"
    echo "   open $DMG_PATH"
    echo ""
    echo "2. Drag Docker.app to Applications folder"
    echo ""
    echo "3. Open Docker from Applications:"
    echo "   open /Applications/Docker.app"
    echo ""
    echo "4. Wait for Docker to start (whale icon in menu bar)"
    echo ""
    echo "5. Then run: ./start_full_system.sh"
    echo ""
    
    # Try to open the DMG
    echo "Opening Docker DMG file..."
    open "$DMG_PATH"
    
else
    echo "❌ Docker DMG not found in Homebrew cache"
    echo ""
    echo "Please download Docker Desktop manually:"
    echo ""
    echo "1. Visit: https://www.docker.com/products/docker-desktop/"
    echo "2. Click 'Download for Mac'"
    echo "3. Choose 'Mac with Apple chip' (for M1/M2)"
    echo "4. Install and run Docker Desktop"
    echo "5. Then run: ./start_full_system.sh"
fi

echo ""
echo "Alternative: Use Docker in a lightweight way"
echo "============================================"
echo ""
echo "If you prefer not to install Docker, you can still use Think AI"
echo "in lightweight mode with just SQLite:"
echo ""
echo "  python simple_cli.py"
echo ""
echo "This will give you:"
echo "- ✅ Consciousness framework"
echo "- ✅ Language model (Phi-2)"
echo "- ✅ Claude API integration"
echo "- ✅ Eternal memory"
echo "- ❌ But no distributed storage/search"