#!/bin/bash

# Think AI Full System Launcher
# This script starts the complete Think AI system including API server and webapp

echo "🚀 Starting Think AI Full System..."
echo "================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 is not installed"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import think_ai" &> /dev/null 2>&1; then
    echo "⚠️  Think AI not installed. Running installation..."
    make install
fi

# Kill any existing processes on ports 8080 and 3000
echo "🔍 Checking for existing processes..."
lsof -ti:8080 | xargs -r kill -9 2>/dev/null && echo "✓ Cleared port 8080"
lsof -ti:3000 | xargs -r kill -9 2>/dev/null && echo "✓ Cleared port 3000"

# Start the full system using process manager
echo ""
echo "🌟 Starting Think AI services:"
echo "  • API Server: http://localhost:8080"
echo "  • Web App: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================="
echo ""

# Run the process manager which handles both API and webapp
python3 process_manager.py