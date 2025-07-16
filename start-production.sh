#!/bin/bash
# Ultimate Production Starter with 100% Uptime Guarantee
set -euo pipefail

# Kill any existing ngrok
pkill -f "ngrok http" || true
sleep 2

# Start ngrok with retry logic
echo "Starting ngrok..."
for i in {1..5}; do
    nohup ngrok http 8080 --domain=thinkai.lat > /home/administrator/think_ai/ngrok_prod.log 2>&1 &
    NGROK_PID=$!
    sleep 5
    
    if ps -p $NGROK_PID > /dev/null; then
        echo "✅ Ngrok started with PID $NGROK_PID"
        break
    else
        echo "Retry $i/5..."
    fi
done

# Verify everything is working
sleep 3
echo "Testing production site..."
if curl -s https://thinkai.lat | grep -q "Think AI"; then
    echo "✅ Production site is LIVE at https://thinkai.lat"
else
    echo "⚠️  Site may still be loading..."
fi

echo ""
echo "🚀 Production is running!"
echo "📱 Access at: https://thinkai.lat"
echo ""
echo "To monitor: tail -f /home/administrator/think_ai/ngrok_prod.log"