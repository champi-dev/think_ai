#!/bin/bash

echo "🚀 Testing Think AI 3D webapp locally..."

# Kill any existing process on port 8000
echo "📋 Checking for processes on port 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Start local server
echo "🌐 Starting local server on http://localhost:8000"
cd "$(dirname "$0")"

# Try Python 3 first, then Python 2
if command -v python3 &> /dev/null; then
    echo "📦 Using Python 3 HTTP server..."
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    echo "📦 Using Python 2 SimpleHTTPServer..."
    python -m SimpleHTTPServer 8000
else
    echo "❌ Error: Python is required to run the local server"
    echo "Please install Python and try again"
    exit 1
fi