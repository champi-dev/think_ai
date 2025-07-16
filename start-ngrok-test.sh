#!/bin/bash

# Start ngrok tunnel for Think AI test server
# This provides HTTPS access from anywhere

echo "🚀 Starting ngrok tunnel for Think AI Test Server"
echo "================================================="
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed!"
    echo ""
    echo "To install ngrok:"
    echo "1. wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
    echo "2. tar -xzf ngrok-v3-stable-linux-amd64.tgz"
    echo "3. sudo mv ngrok /usr/local/bin/"
    echo "4. ngrok config add-authtoken YOUR_AUTH_TOKEN"
    echo ""
    echo "Get your auth token at: https://dashboard.ngrok.com/get-started/your-authtoken"
    exit 1
fi

# Check if test server is running
if ! curl -s http://localhost:9090/health > /dev/null 2>&1; then
    echo "⚠️  Test server is not running on port 9090!"
    echo "Please run ./test-context-isolated.sh first"
    exit 1
fi

echo "✅ Test server detected on port 9090"
echo "🌐 Starting ngrok tunnel..."
echo ""
echo "You will see the public HTTPS URL below."
echo "Share this URL to access from anywhere!"
echo ""
echo "Press Ctrl+C to stop the tunnel"
echo "================================================="
echo ""

# Start ngrok
ngrok http 9090 --log-level=info --log=stdout