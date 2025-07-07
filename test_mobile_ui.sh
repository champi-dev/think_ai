#!/bin/bash

echo "==================================="
echo "Think AI Mobile UI Test Script"
echo "==================================="

# Kill any existing processes on port 8080
echo "Cleaning up port 8080..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
sleep 1

# Get local IP address for mobile testing
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "📱 Mobile Test URLs:"
echo "-------------------"
echo "Local:   http://localhost:8080/static/chat.html"
echo "Mobile:  http://${LOCAL_IP}:8080/static/chat.html"
echo "Simple:  http://${LOCAL_IP}:8080/static/simple_webapp.html"
echo ""

# Start the server
echo "🚀 Starting Think AI server..."
echo "Press Ctrl+C to stop"
echo ""

./target/release/think-ai server