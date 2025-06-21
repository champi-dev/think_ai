#!/bin/bash
# Install Think AI as a system service

set -e

echo "🚀 Think AI Service Installer"
echo "============================"

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "$OS" == "linux" ]; then
    echo "📦 Installing on Linux..."
    
    # Check if systemd is available
    if ! command -v systemctl &> /dev/null; then
        echo "❌ systemd not found. This installer requires systemd."
        exit 1
    fi
    
    # Install python-daemon if needed
    pip3 install python-daemon lockfile
    
    # Copy files to /opt/think_ai
    sudo mkdir -p /opt/think_ai
    sudo cp -r "$SCRIPT_DIR"/* /opt/think_ai/
    
    # Copy systemd service file
    sudo cp "$SCRIPT_DIR/think-ai.service" /etc/systemd/system/
    
    # Create config directory
    sudo mkdir -p /etc/think_ai
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    # Enable service
    sudo systemctl enable think-ai.service
    
    echo "✅ Service installed!"
    echo ""
    echo "To start the service:"
    echo "  sudo systemctl start think-ai"
    echo ""
    echo "To check status:"
    echo "  sudo systemctl status think-ai"
    echo ""
    echo "To view logs:"
    echo "  sudo journalctl -u think-ai -f"
    
elif [ "$OS" == "macos" ]; then
    echo "📦 Installing on macOS..."
    
    # Install to user LaunchAgents
    LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
    mkdir -p "$LAUNCH_AGENTS_DIR"
    
    # Update plist with correct paths
    sed "s|/Users/champi/Development/Think_AI|$SCRIPT_DIR|g" \
        "$SCRIPT_DIR/com.thinkAI.service.plist" > "$LAUNCH_AGENTS_DIR/com.thinkAI.service.plist"
    
    # Load the service
    launchctl load -w "$LAUNCH_AGENTS_DIR/com.thinkAI.service.plist"
    
    echo "✅ Service installed!"
    echo ""
    echo "To start the service:"
    echo "  launchctl start com.thinkAI.service"
    echo ""
    echo "To check status:"
    echo "  launchctl list | grep thinkAI"
    echo ""
    echo "To view logs:"
    echo "  tail -f /tmp/think_ai_service.log"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "⚠️  IMPORTANT: The service will start automatically on system boot."
echo "It will run all Think AI tests in parallel continuously."
echo "To stop the service, use the appropriate system command above."