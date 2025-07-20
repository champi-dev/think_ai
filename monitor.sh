#!/bin/bash
# Think AI Health Monitor - Prevents downtime through proactive monitoring

LOGFILE="/home/champi/Dev/think_ai/monitor.log"
PIDFILE="/home/champi/Dev/think_ai/app-prod.pid"
SERVICE_PORT=7777
MAX_RETRIES=3
RETRY_DELAY=5

check_service() {
    # Check if process exists
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        if ! kill -0 "$PID" 2>/dev/null; then
            echo "[$(date)] Process $PID is dead" >> "$LOGFILE"
            return 1
        fi
    else
        echo "[$(date)] PID file missing" >> "$LOGFILE"
        return 1
    fi
    
    # Check HTTP endpoint
    if ! curl -f -s -m 5 "http://localhost:$SERVICE_PORT/" > /dev/null; then
        echo "[$(date)] HTTP check failed" >> "$LOGFILE"
        return 1
    fi
    
    return 0
}

restart_service() {
    echo "[$(date)] Restarting service..." >> "$LOGFILE"
    
    # Kill existing process
    if [ -f "$PIDFILE" ]; then
        kill $(cat "$PIDFILE") 2>/dev/null
        sleep 2
        kill -9 $(cat "$PIDFILE") 2>/dev/null
    fi
    
    # Clean up stale locks
    rm -f /home/champi/Dev/think_ai/full-system/think_ai_sessions.db/db.lock*
    
    # Start service
    cd /home/champi/Dev/think_ai/full-system
    /home/champi/Dev/think_ai/full-system/target/release/think-ai-full > /home/champi/Dev/think_ai/app-prod.log 2>&1 & 
    echo $! > "$PIDFILE"
    
    sleep 5
    
    # Verify restart
    if check_service; then
        echo "[$(date)] Service restarted successfully" >> "$LOGFILE"
        return 0
    else
        echo "[$(date)] Service restart failed" >> "$LOGFILE"
        return 1
    fi
}

# Main monitoring loop
echo "[$(date)] Monitor started" >> "$LOGFILE"

retry_count=0
while true; do
    if ! check_service; then
        retry_count=$((retry_count + 1))
        echo "[$(date)] Health check failed (attempt $retry_count/$MAX_RETRIES)" >> "$LOGFILE"
        
        if [ $retry_count -ge $MAX_RETRIES ]; then
            if restart_service; then
                retry_count=0
            else
                echo "[$(date)] CRITICAL: Service restart failed after $MAX_RETRIES attempts" >> "$LOGFILE"
                # Send alert here if needed
            fi
        fi
    else
        retry_count=0
    fi
    
    sleep $RETRY_DELAY
done