#!/bin/bash
# Start the fixed AI server with proper response mappings

cd /home/administrator/think_ai

# Kill any existing processes
pkill -f "python3.*fixed_ai_server" || true
pkill -f "python3.*7777" || true

echo "Starting fixed AI server..."
nohup python3 fixed_ai_server.py > fixed-server.log 2>&1 &
echo $! > fixed-server.pid

sleep 2

if ps -p $(cat fixed-server.pid) > /dev/null; then
    echo "✅ Fixed AI server started successfully on port 7777"
    echo "📝 Logs: tail -f fixed-server.log"
    echo "🌐 Access at: http://localhost:7777"
else
    echo "❌ Failed to start server"
    exit 1
fi