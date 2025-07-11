#!/bin/bash

echo "Starting ngrok tunnel to thinkai.lat..."

# Kill any existing ngrok processes
pkill ngrok

# Start ngrok in background
nohup ngrok http 80 --domain=thinkai.lat --log=ngrok.log > /dev/null 2>&1 &

NGROK_PID=$!
echo "ngrok started with PID: $NGROK_PID"

# Wait for ngrok to start
sleep 3

# Check if it's running
if ps -p $NGROK_PID > /dev/null; then
    echo "✓ ngrok tunnel is running!"
    echo "✓ Your site is accessible at: https://thinkai.lat"
    echo ""
    echo "To stop ngrok: kill $NGROK_PID"
    echo "To check status: curl http://localhost:4040/api/tunnels"
else
    echo "✗ Failed to start ngrok"
    tail -10 ngrok.log
fi