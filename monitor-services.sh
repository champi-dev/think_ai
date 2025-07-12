#!/bin/bash
# Service Monitor for Think AI and Ngrok
# Ensures both services are always running with health checks

set -euo pipefail

LOG_FILE="/home/administrator/think_ai/service-monitor.log"
HEALTH_CHECK_INTERVAL=30  # seconds
NGROK_API="http://localhost:4040/api/tunnels"
THINK_AI_HEALTH="http://localhost:8080/health"
THINK_AI_CHAT="http://localhost:8080/api/chat"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

check_think_ai() {
    # Check if service is active
    if ! systemctl is-active --quiet think-ai.service; then
        log "WARNING: Think AI service is not active, restarting..."
        sudo systemctl restart think-ai.service
        sleep 5
    fi
    
    # Health check
    if ! curl -s -f "$THINK_AI_HEALTH" > /dev/null 2>&1; then
        log "ERROR: Think AI health check failed, restarting service..."
        sudo systemctl restart think-ai.service
        sleep 5
    fi
    
    # API check with timeout
    if ! curl -X POST "$THINK_AI_CHAT" \
         -H "Content-Type: application/json" \
         -d '{"message": "test"}' \
         --max-time 5 \
         -s -f > /dev/null 2>&1; then
        log "ERROR: Think AI API check failed, restarting service..."
        sudo systemctl restart think-ai.service
        sleep 5
    fi
}

check_ngrok() {
    # Check if any ngrok process is running
    if ! pgrep -f "ngrok http" > /dev/null; then
        log "WARNING: Ngrok is not running, starting..."
        sudo systemctl start ngrok.service
        sleep 10  # Give ngrok time to establish tunnel
    fi
    
    # Check ngrok API
    if ! curl -s -f "$NGROK_API" | grep -q "thinkai.lat"; then
        log "ERROR: Ngrok tunnel not established correctly, restarting..."
        sudo systemctl restart ngrok.service
        sleep 10
    fi
    
    # Check if tunnel is accessible
    if ! curl -s -f -I "https://thinkai.lat" --max-time 5 > /dev/null 2>&1; then
        log "ERROR: thinkai.lat not accessible, restarting ngrok..."
        sudo systemctl restart ngrok.service
        sleep 10
    fi
}

main() {
    log "Starting service monitor..."
    
    while true; do
        # Check Think AI first (ngrok depends on it)
        check_think_ai
        
        # Then check ngrok
        check_ngrok
        
        # Quick validation that everything is working
        if curl -s -f "https://thinkai.lat/health" > /dev/null 2>&1; then
            log "✓ All services healthy"
        else
            log "⚠ Services may have issues, will recheck on next cycle"
        fi
        
        sleep "$HEALTH_CHECK_INTERVAL"
    done
}

# Run in background if called with 'daemon' argument
if [[ "${1:-}" == "daemon" ]]; then
    log "Starting monitor in daemon mode..."
    nohup "$0" > /dev/null 2>&1 &
    echo $! > /home/administrator/think_ai/monitor.pid
    log "Monitor daemon started with PID $(cat /home/administrator/think_ai/monitor.pid)"
else
    main
fi