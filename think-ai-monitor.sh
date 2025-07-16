#!/bin/bash

# Think AI Production Monitor - Ensures 100% success rate
# This script monitors all Think AI services and automatically fixes issues

# Configuration
HEALTH_CHECK_INTERVAL=30  # seconds
NGROK_DOMAIN="thinkai.lat"
LOCAL_PORT=8080
LOG_FILE="/home/administrator/think_ai/monitor.log"
STATE_FILE="/home/administrator/think_ai/monitor.state"

# Color codes for logging
log_info() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $1" | tee -a "$LOG_FILE"
}

# Function to check if a process is running
check_process() {
    local process_name="$1"
    if pgrep -f "$process_name" > /dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to start Think AI server
start_think_ai_server() {
    log_info "Starting Think AI server on port $LOCAL_PORT..."
    
    # Kill any existing process on the port
    fuser -k $LOCAL_PORT/tcp 2>/dev/null || true
    sleep 2
    
    # Start the server
    cd /home/administrator/think_ai
    nohup /home/administrator/think_ai/target/release/think-ai server > server.log 2>&1 &
    
    sleep 5
    
    # Verify it started
    if curl -s http://localhost:$LOCAL_PORT/health | grep -q "healthy"; then
        log_success "Think AI server started successfully"
        return 0
    else
        log_error "Failed to start Think AI server"
        return 1
    fi
}

# Function to start ngrok tunnel
start_ngrok_tunnel() {
    log_info "Starting ngrok tunnel for $NGROK_DOMAIN..."
    
    # Kill any existing ngrok processes
    pkill -f "ngrok http" 2>/dev/null || true
    sleep 2
    
    # Start ngrok
    nohup ngrok http $LOCAL_PORT --domain=$NGROK_DOMAIN --log=stdout > ngrok.log 2>&1 &
    
    sleep 10
    
    # Verify tunnel is up
    if curl -sL https://$NGROK_DOMAIN/health | grep -q "healthy"; then
        log_success "Ngrok tunnel established successfully"
        return 0
    else
        log_error "Failed to establish ngrok tunnel"
        return 1
    fi
}

# Function to perform health checks
perform_health_checks() {
    local all_healthy=true
    
    # Check 1: Think AI server process
    if check_process "think-ai server"; then
        echo -n "✓" > "$STATE_FILE.server"
    else
        echo -n "✗" > "$STATE_FILE.server"
        all_healthy=false
        log_error "Think AI server process not running"
    fi
    
    # Check 2: Local health endpoint
    if curl -s http://localhost:$LOCAL_PORT/health | grep -q "healthy"; then
        echo -n "✓" > "$STATE_FILE.local_health"
    else
        echo -n "✗" > "$STATE_FILE.local_health"
        all_healthy=false
        log_error "Local health endpoint not responding"
    fi
    
    # Check 3: Ngrok process
    if check_process "ngrok http"; then
        echo -n "✓" > "$STATE_FILE.ngrok"
    else
        echo -n "✗" > "$STATE_FILE.ngrok"
        all_healthy=false
        log_error "Ngrok process not running"
    fi
    
    # Check 4: Public endpoint
    if curl -sL https://$NGROK_DOMAIN/health | grep -q "healthy"; then
        echo -n "✓" > "$STATE_FILE.public_health"
    else
        echo -n "✗" > "$STATE_FILE.public_health"
        all_healthy=false
        log_error "Public endpoint not responding"
    fi
    
    # Check 5: API functionality
    response=$(curl -sL -X POST https://$NGROK_DOMAIN/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "health check"}' 2>/dev/null)
    
    if echo "$response" | grep -q "response"; then
        echo -n "✓" > "$STATE_FILE.api"
    else
        echo -n "✗" > "$STATE_FILE.api"
        all_healthy=false
        log_error "API not functioning properly"
    fi
    
    # Check 6: WebSocket endpoint
    ws_response=$(curl -sL -I https://$NGROK_DOMAIN/ws \
        -H "Upgrade: websocket" \
        -H "Connection: Upgrade" 2>/dev/null | head -1)
    
    if echo "$ws_response" | grep -q "101\|426\|400"; then
        echo -n "✓" > "$STATE_FILE.websocket"
    else
        echo -n "✗" > "$STATE_FILE.websocket"
        all_healthy=false
        log_error "WebSocket endpoint not responding"
    fi
    
    if $all_healthy; then
        return 0
    else
        return 1
    fi
}

# Function to fix issues
fix_issues() {
    log_info "Attempting to fix issues..."
    
    # Check if server is down
    if [ -f "$STATE_FILE.server" ] && [ "$(cat $STATE_FILE.server)" = "✗" ]; then
        start_think_ai_server
    fi
    
    # Check if local health is down but server is up
    if [ -f "$STATE_FILE.local_health" ] && [ "$(cat $STATE_FILE.local_health)" = "✗" ]; then
        if [ -f "$STATE_FILE.server" ] && [ "$(cat $STATE_FILE.server)" = "✓" ]; then
            log_info "Server is running but not responding, restarting..."
            pkill -f "think-ai server" 2>/dev/null || true
            sleep 2
            start_think_ai_server
        fi
    fi
    
    # Check if ngrok is down
    if [ -f "$STATE_FILE.ngrok" ] && [ "$(cat $STATE_FILE.ngrok)" = "✗" ]; then
        start_ngrok_tunnel
    fi
    
    # Check if public endpoint is down but ngrok is up
    if [ -f "$STATE_FILE.public_health" ] && [ "$(cat $STATE_FILE.public_health)" = "✗" ]; then
        if [ -f "$STATE_FILE.ngrok" ] && [ "$(cat $STATE_FILE.ngrok)" = "✓" ]; then
            log_info "Ngrok is running but tunnel is broken, restarting..."
            start_ngrok_tunnel
        fi
    fi
}

# Function to generate status report
generate_status_report() {
    local status_line="[$(date '+%H:%M:%S')] Status: "
    
    [ -f "$STATE_FILE.server" ] && status_line+="Server:$(cat $STATE_FILE.server) "
    [ -f "$STATE_FILE.local_health" ] && status_line+="Local:$(cat $STATE_FILE.local_health) "
    [ -f "$STATE_FILE.ngrok" ] && status_line+="Ngrok:$(cat $STATE_FILE.ngrok) "
    [ -f "$STATE_FILE.public_health" ] && status_line+="Public:$(cat $STATE_FILE.public_health) "
    [ -f "$STATE_FILE.api" ] && status_line+="API:$(cat $STATE_FILE.api) "
    [ -f "$STATE_FILE.websocket" ] && status_line+="WS:$(cat $STATE_FILE.websocket)"
    
    echo "$status_line"
}

# Main monitoring loop
main() {
    log_info "Think AI Production Monitor started"
    log_info "Monitoring interval: ${HEALTH_CHECK_INTERVAL}s"
    log_info "Domain: $NGROK_DOMAIN"
    
    # Initial startup
    if ! perform_health_checks; then
        log_info "Initial health check failed, starting services..."
        start_think_ai_server
        start_ngrok_tunnel
    fi
    
    # Main loop
    while true; do
        if perform_health_checks; then
            log_success "All services healthy - 100% success rate"
            generate_status_report
        else
            log_error "Health check failed, attempting to fix..."
            generate_status_report
            fix_issues
            
            # Wait a bit for services to stabilize
            sleep 10
            
            # Re-check after fixes
            if perform_health_checks; then
                log_success "Issues resolved - services restored"
            else
                log_error "Some issues persist, will retry on next cycle"
            fi
        fi
        
        sleep $HEALTH_CHECK_INTERVAL
    done
}

# Trap to handle shutdown gracefully
trap 'log_info "Monitor shutting down..."; exit 0' SIGTERM SIGINT

# Start monitoring
main