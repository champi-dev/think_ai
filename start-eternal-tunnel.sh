#!/bin/bash

echo "🌐 Starting ngrok tunnel for Eternal Context Server"
echo "=================================================="

# Kill any existing ngrok on port 7878
pkill -f "ngrok.*7878" 2>/dev/null || true

# Start ngrok in background
ngrok http 7878 > /tmp/ngrok-eternal.log 2>&1 &
NGROK_PID=$!

echo "Waiting for ngrok to start..."
sleep 5

# Get the public URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | jq -r '.tunnels[] | select(.config.addr | contains("7878")) | .public_url' | head -1)

if [ -z "$NGROK_URL" ]; then
    echo "❌ Failed to start ngrok tunnel"
    echo "Check /tmp/ngrok-eternal.log for details"
    exit 1
fi

echo ""
echo "✅ Ngrok tunnel started!"
echo ""
echo "🌍 Public URL: $NGROK_URL"
echo ""
echo "📱 Access your Eternal Context System from anywhere:"
echo "   - Chat: $NGROK_URL"
echo "   - Health: $NGROK_URL/health"
echo "   - Stats: $NGROK_URL/stats"
echo ""
echo "🧪 Test from anywhere:"
echo "curl -X POST $NGROK_URL/api/chat \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"message\": \"Hello from the internet!\", \"session_id\": \"test\"}'"
echo ""
echo "📊 Monitor tunnel: http://localhost:4040"
echo ""
echo "🛑 Press Ctrl+C to stop the tunnel"

# Keep running
trap "kill $NGROK_PID 2>/dev/null; echo 'Tunnel stopped.'; exit" INT
wait $NGROK_PID