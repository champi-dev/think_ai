#!/bin/bash
# SSH Tunnel Helper for Think AI

CLOUD_USER="${1:-user}"
CLOUD_IP="${2:-}"
LOCAL_PORT="${3:-7777}"
REMOTE_PORT="${4:-8080}"

if [ -z "$CLOUD_IP" ]; then
    echo "Usage: $0 [USER] <CLOUD_IP> [LOCAL_PORT] [REMOTE_PORT]"
    echo "Example: $0 ubuntu 123.45.67.89"
    exit 1
fi

echo "Creating SSH tunnel..."
echo "Local: http://localhost:$LOCAL_PORT"
echo "Remote: $CLOUD_USER@$CLOUD_IP:$REMOTE_PORT"
echo ""
echo "Press Ctrl+C to close tunnel"

ssh -N -L $LOCAL_PORT:localhost:$REMOTE_PORT $CLOUD_USER@$CLOUD_IP
