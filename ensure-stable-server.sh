#!/bin/bash
# Ensure stable-server-streaming is running instead of regular think-ai server

while true; do
    # Kill any regular think-ai server
    pkill -f "think-ai server" 2>/dev/null
    
    # Check if stable-server is running
    if ! pgrep -f "stable-server-streaming" > /dev/null; then
        echo "[$(date)] Starting stable-server-streaming..."
        cd /home/administrator/think_ai
        nohup ./target/release/stable-server-streaming > stable-server.log 2>&1 &
        sleep 5
    fi
    
    sleep 10
done