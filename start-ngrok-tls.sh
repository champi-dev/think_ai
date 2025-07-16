#!/bin/bash

# Start ngrok with your TLS certificate
CERT_ID="cert_2zgiMI9vBRCkwY54ry1h8zthW4b"

echo "Starting ngrok tunnel with TLS certificate..."

# Kill any existing ngrok processes
pkill ngrok

# Start your think-ai-full server first (if not already running as a service)
if ! systemctl is-active --quiet think-ai-full; then
    echo "Starting think-ai-full server..."
    ./target/release/think-ai-full server &
    THINK_AI_PID=$!
    sleep 2
fi

# Start ngrok with your custom domain
# This will create a secure tunnel to your local server
ngrok http 80 \
    --domain=thinkai.lat \
    --log=ngrok.log &

NGROK_PID=$!
echo "ngrok started with PID: $NGROK_PID"

# Wait a moment for ngrok to start
sleep 3

# Check if ngrok is running
if ps -p $NGROK_PID > /dev/null; then
    echo "ngrok tunnel is running!"
    echo "Your site should be accessible at: https://thinkai.lat"
    echo ""
    echo "To view ngrok status, run: curl -s http://localhost:4040/api/tunnels"
    echo "To stop ngrok, run: kill $NGROK_PID"
else
    echo "Failed to start ngrok. Check ngrok.log for details."
    tail -20 ngrok.log
fi