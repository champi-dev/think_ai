#\!/bin/bash

# Kill any existing ngrok processes
pkill -f ngrok || true
sleep 2

# Start ngrok in a loop to handle restarts
while true; do
    echo "[$(date)] Starting ngrok tunnel for thinkai.lat..."
    ngrok http 8080 --domain=thinkai.lat --log=stdout >> /home/administrator/think_ai/ngrok-daemon.log 2>&1
    EXIT_CODE=$?
    echo "[$(date)] Ngrok exited with code $EXIT_CODE" >> /home/administrator/think_ai/ngrok-daemon.log
    
    # Wait before restarting
    sleep 5
done
