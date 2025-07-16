#!/bin/bash

# Kill any existing ngrok processes
echo "[$(date)] Stopping existing ngrok processes..."
pkill -f "ngrok http" || true
sleep 2

# Function to check if ngrok tunnel is active
check_tunnel() {
    curl -s http://localhost:4040/api/tunnels | grep -q "thinkai.lat"
}

# Function to start ngrok with proper error handling
start_ngrok() {
    echo "[$(date)] Starting ngrok tunnel for thinkai.lat..."
    
    # Start ngrok in background with explicit config
    ngrok http 8080 \
        --domain=thinkai.lat \
        --log=stdout \
        --log-level=info \
        > /home/administrator/think_ai/ngrok_detailed.log 2>&1 &
    
    NGROK_PID=$!
    echo "[$(date)] Ngrok started with PID: $NGROK_PID"
    
    # Wait for tunnel to establish
    sleep 5
    
    # Check if process is still running
    if ps -p $NGROK_PID > /dev/null; then
        echo "[$(date)] Ngrok process is running"
        
        # Check if tunnel is active
        if check_tunnel; then
            echo "[$(date)] Tunnel successfully established at thinkai.lat"
            return 0
        else
            echo "[$(date)] ERROR: Tunnel not established, checking logs..."
            tail -20 /home/administrator/think_ai/ngrok_detailed.log
            return 1
        fi
    else
        echo "[$(date)] ERROR: Ngrok process died, checking logs..."
        tail -20 /home/administrator/think_ai/ngrok_detailed.log
        return 1
    fi
}

# Main monitoring loop
while true; do
    if ! check_tunnel; then
        echo "[$(date)] Tunnel is down, restarting..."
        pkill -f "ngrok http" || true
        sleep 2
        
        if start_ngrok; then
            echo "[$(date)] Ngrok restarted successfully"
        else
            echo "[$(date)] Failed to restart ngrok, will retry in 10 seconds"
            sleep 10
            continue
        fi
    fi
    
    # Check every 30 seconds
    sleep 30
done