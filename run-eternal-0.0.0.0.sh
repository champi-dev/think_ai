#!/bin/bash

echo "🧠 Starting Eternal Context System on 0.0.0.0:7878"
echo "================================================="

# Get local IP address
LOCAL_IP=$(hostname -I | awk '{print $1}')

# Kill any existing processes on port 7878
echo "Cleaning up port 7878..."
lsof -ti:7878 | xargs kill -9 2>/dev/null || true

# Start the server
echo "Starting Eternal Context Server..."
PORT=7878 ./target/release/eternal-context-server &
SERVER_PID=$!

sleep 3

echo ""
echo "✅ Server is running on 0.0.0.0:7878!"
echo ""
echo "🌐 Access from this machine:"
echo "   - http://localhost:7878"
echo "   - http://127.0.0.1:7878"
echo "   - http://0.0.0.0:7878"
echo ""
echo "📱 Access from other devices on your network:"
echo "   - http://$LOCAL_IP:7878"
echo ""
echo "🖥️  Available interfaces:"
echo "   - Chat UI: http://$LOCAL_IP:7878/"
echo "   - Health: http://$LOCAL_IP:7878/health"
echo "   - Stats: http://$LOCAL_IP:7878/stats"
echo ""
echo "🧪 Test with curl:"
echo "curl -X POST http://localhost:7878/api/chat \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"message\": \"Hello!\", \"session_id\": \"test\"}'"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Show network interfaces
echo "📡 Your network interfaces:"
ip addr show | grep "inet " | grep -v "127.0.0.1" | awk '{print "   - " $2}'
echo ""

# Wait for user to stop
trap "kill $SERVER_PID 2>/dev/null; echo 'Server stopped.'; exit" INT
wait $SERVER_PID