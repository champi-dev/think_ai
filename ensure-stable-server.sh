#!/bin/bash
# Ensure stable-server-streaming is running instead of regular think-ai server

LOG_FILE="/home/administrator/think_ai/ensure-stable-server.log"

while true; do
    # Kill any regular think-ai server
    pkill -f "think-ai server" 2>/dev/null
    
    # Check if stable-server is running
    if ! pgrep -f "stable-server-streaming" > /dev/null; then
        echo "[$(date)] Starting stable-server-streaming..." >> "$LOG_FILE"
        cd /home/administrator/think_ai
        # Start with explicit path and wait a moment
        /home/administrator/think_ai/target/release/stable-server-streaming >> stable-server.log 2>&1 &
        PID=$!
        sleep 5
        
        # Verify it started successfully
        if ps -p $PID > /dev/null; then
            echo "[$(date)] stable-server-streaming started successfully with PID $PID" >> "$LOG_FILE"
        else
            echo "[$(date)] Failed to start stable-server-streaming" >> "$LOG_FILE"
        fi
    fi
    
    sleep 10
done