#!/bin/bash
# Ngrok daemon that ensures it stays running

while true; do
    echo "[$(date)] Starting ngrok..."
    ngrok http 8080 --domain=thinkai.lat --log=stdout
    echo "[$(date)] Ngrok exited, restarting in 5 seconds..."
    sleep 5
done