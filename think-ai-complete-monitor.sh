#!/bin/bash

# Think AI Complete Production Monitor
# Ensures 100% uptime for all services

LOG_FILE="/home/administrator/think_ai/complete-monitor.log"
NGROK_DOMAIN="thinkai.lat"
LOCAL_PORT=8080

# Logging functions
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to ensure Think AI server is running
ensure_server() {
    if ! lsof -i :$LOCAL_PORT | grep -q LISTEN; then
        log "ERROR: Think AI server not running on port $LOCAL_PORT"
        log "Starting Think AI server..."
        cd /home/administrator/think_ai
        nohup ./target/release/think-ai server > server_monitor.log 2>&1 &
        sleep 5
        if lsof -i :$LOCAL_PORT | grep -q LISTEN; then
            log "SUCCESS: Think AI server started"
        else
            log "CRITICAL: Failed to start Think AI server"
            return 1
        fi
    fi
    return 0
}

# Function to ensure ngrok tunnel is running
ensure_ngrok() {
    # Check if ngrok process exists
    if ! pgrep -f "ngrok http" > /dev/null; then
        log "ERROR: Ngrok not running"
        log "Starting ngrok tunnel..."
        cd /home/administrator/think_ai
        nohup ngrok http $LOCAL_PORT --domain=$NGROK_DOMAIN > ngrok_monitor.log 2>&1 &
        sleep 10
    fi
    
    # Verify tunnel is accessible
    if curl -sL https://$NGROK_DOMAIN/health | grep -q "healthy"; then
        log "SUCCESS: Ngrok tunnel is healthy"
        return 0
    else
        log "ERROR: Ngrok tunnel not accessible"
        # Kill and restart
        pkill -f "ngrok http"
        sleep 2
        nohup ngrok http $LOCAL_PORT --domain=$NGROK_DOMAIN > ngrok_monitor.log 2>&1 &
        sleep 10
        
        if curl -sL https://$NGROK_DOMAIN/health | grep -q "healthy"; then
            log "SUCCESS: Ngrok tunnel restored"
            return 0
        else
            log "CRITICAL: Failed to establish ngrok tunnel"
            return 1
        fi
    fi
}

# Function to test all endpoints
test_endpoints() {
    local all_good=true
    
    # Test health
    if ! curl -sL https://$NGROK_DOMAIN/health | grep -q "healthy"; then
        log "FAIL: Health endpoint"
        all_good=false
    fi
    
    # Test main page
    if ! curl -sL https://$NGROK_DOMAIN/ | grep -q "Think AI"; then
        log "FAIL: Main page"
        all_good=false
    fi
    
    # Test API docs
    if ! curl -sL https://$NGROK_DOMAIN/api-docs.html | grep -q "API"; then
        log "FAIL: API docs"
        all_good=false
    fi
    
    # Test chat API
    response=$(curl -sL -X POST https://$NGROK_DOMAIN/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "test"}' 2>/dev/null)
    
    if ! echo "$response" | grep -q "response"; then
        log "FAIL: Chat API"
        all_good=false
    fi
    
    if $all_good; then
        log "All endpoints healthy"
        return 0
    else
        return 1
    fi
}

# Main monitoring loop
main() {
    log "Starting Think AI Complete Monitor"
    log "Domain: $NGROK_DOMAIN"
    log "Port: $LOCAL_PORT"
    
    while true; do
        # Ensure server is running
        ensure_server
        
        # Ensure ngrok is running and accessible
        ensure_ngrok
        
        # Test all endpoints
        if test_endpoints; then
            log "System status: HEALTHY (100% operational)"
        else
            log "System status: DEGRADED (attempting recovery)"
        fi
        
        # Wait 30 seconds before next check
        sleep 30
    done
}

# Handle shutdown gracefully
trap 'log "Monitor shutting down..."; exit 0' SIGTERM SIGINT

# Start monitoring
main