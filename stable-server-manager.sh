#!/bin/bash
# Stable Server Manager - Ensures only one instance runs

PIDFILE="/var/run/stable-server.pid"
LOCKFILE="/var/lock/stable-server.lock"
LOGFILE="/home/administrator/think_ai/stable-server.log"

# Function to clean up old processes
cleanup_old_processes() {
    echo "[$(date)] Cleaning up old processes..." >> "$LOGFILE"
    
    # Kill any process on port 8080
    if lsof -ti:8080 >/dev/null 2>&1; then
        echo "[$(date)] Found process on port 8080, killing..." >> "$LOGFILE"
        lsof -ti:8080 | xargs -r kill -9 2>/dev/null || true
        sleep 2
    fi
    
    # Kill any stable-server processes
    pkill -f "stable-server" 2>/dev/null || true
    
    # Clean up stale PID file
    if [ -f "$PIDFILE" ]; then
        OLD_PID=$(cat "$PIDFILE" 2>/dev/null)
        if [ -n "$OLD_PID" ] && ! kill -0 "$OLD_PID" 2>/dev/null; then
            echo "[$(date)] Removing stale PID file" >> "$LOGFILE"
            rm -f "$PIDFILE"
        fi
    fi
    
    # Remove lock file
    rm -f "$LOCKFILE"
}

# Function to start the server
start_server() {
    # Use flock to ensure single instance
    exec 200>"$LOCKFILE"
    if ! flock -n 200; then
        echo "[$(date)] Another instance is already running" >> "$LOGFILE"
        exit 1
    fi
    
    # Clean up first
    cleanup_old_processes
    
    # Start the server
    echo "[$(date)] Starting stable server..." >> "$LOGFILE"
    exec /home/administrator/think_ai/target/release/stable-server-streaming-websearch
}

# Handle termination
trap 'echo "[$(date)] Received termination signal" >> "$LOGFILE"; rm -f "$PIDFILE" "$LOCKFILE"; exit 0' SIGTERM SIGINT

# Main execution
case "${1:-start}" in
    start)
        start_server
        ;;
    cleanup)
        cleanup_old_processes
        ;;
    *)
        echo "Usage: $0 {start|cleanup}"
        exit 1
        ;;
esac