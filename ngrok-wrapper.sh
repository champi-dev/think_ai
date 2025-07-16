#!/bin/bash
while true; do
    echo "[$(date)] Starting ngrok tunnel..."
    ngrok http 8080 --domain=thinkai.lat
    echo "[$(date)] Ngrok exited, restarting in 5 seconds..."
    sleep 5
done
