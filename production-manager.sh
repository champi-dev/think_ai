#!/bin/bash
# Production Manager for Think AI
# Ensures all services are running with proper monitoring

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
PID_DIR="$SCRIPT_DIR/pids"

# Create directories if they don't exist
mkdir -p "$LOG_DIR" "$PID_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $*" >&2
}

warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $*"
}

# Kill any existing ngrok processes
kill_ngrok() {
    log "Killing existing ngrok processes..."
    if [[ -f "$PID_DIR/ngrok.pid" ]]; then
        local ngrok_pid=$(cat "$PID_DIR/ngrok.pid")
        if ps -p $ngrok_pid > /dev/null; then
            kill $ngrok_pid
        fi
        rm -f "$PID_DIR/ngrok.pid"
    fi
    pkill -f "ngrok http" || true
    sleep 2
}

# Start ngrok with proper configuration
start_ngrok() {
    kill_ngrok
    
    log "Starting ngrok tunnel to thinkai.lat..."
    nohup ngrok http 8080 --domain=thinkai.lat --log=stdout > "$LOG_DIR/ngrok.log" 2>&1 &
    local ngrok_pid=$!
    echo $ngrok_pid > "$PID_DIR/ngrok.pid"
    
    # Wait for ngrok to start
    sleep 5
    
    # Verify ngrok is running
    if ps -p $ngrok_pid > /dev/null; then
        log "✅ Ngrok started with PID $ngrok_pid"
        
        # Check if tunnel is established
        if curl -s http://localhost:4040/api/tunnels | grep -q "thinkai.lat"; then
            log "✅ Ngrok tunnel established at https://thinkai.lat"
        else
            warning "Ngrok is running but tunnel not confirmed"
        fi
    else
        error "Failed to start ngrok"
        return 1
    fi
}

# Check Think AI service
check_think_ai() {
    log "Checking Think AI service..."
    
    if systemctl is-active --quiet think-ai-full.service; then
        log "✅ Think AI service is active"
        
        # Test health endpoint
        if curl -s -f http://localhost:8080/health > /dev/null 2>&1; then
            log "✅ Think AI health check passed"
        else
            error "Think AI health check failed"
            return 1
        fi
    else
        error "Think AI service is not active"
        return 1
    fi
}

# Test full stack
test_stack() {
    log "Testing full stack..."
    
    # Test local API
    if curl -s -f http://localhost:8080/health | grep -q "healthy"; then
        log "✅ Local API is healthy"
    else
        error "Local API test failed"
        return 1
    fi
    
    # Test ngrok tunnel
    sleep 2
    if curl -s -f https://thinkai.lat/health --max-time 10 | grep -q "healthy"; then
        log "✅ Public URL (https://thinkai.lat) is accessible"
    else
        warning "Public URL test failed, retrying..."
        sleep 5
        if curl -s -f https://thinkai.lat/health --max-time 10 | grep -q "healthy"; then
            log "✅ Public URL is now accessible"
        else
            error "Public URL is not accessible"
            return 1
        fi
    fi
    
    # Test chat API
    local response=$(curl -s -X POST http://localhost:8080/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "test"}' \
        --max-time 5 || echo "failed")
    
    if [[ "$response" == *"response"* ]]; then
        log "✅ Chat API is responding"
    else
        error "Chat API test failed"
        return 1
    fi
}

# Monitor services
monitor_loop() {
    log "Starting monitoring loop..."
    
    while true; do
        # Check Think AI
        if ! check_think_ai; then
            warning "Restarting Think AI service..."
            sudo systemctl restart think-ai-full.service
            sleep 5
        fi
        
        # Check ngrok
        if [[ -f "$PID_DIR/ngrok.pid" ]]; then
            local ngrok_pid=$(cat "$PID_DIR/ngrok.pid")
            if ! ps -p $ngrok_pid > /dev/null; then
                warning "Ngrok is not running, restarting..."
                start_ngrok
            fi
        else
            warning "Ngrok PID file not found, starting ngrok..."
            start_ngrok
        fi
        
        # Quick health check
        if curl -s -f https://thinkai.lat --max-time 5 > /dev/null 2>&1; then
            log "✅ All systems operational"
        else
            warning "Public URL not responding, checking services..."
        fi
        
        sleep 30
    done
}

# Main function
main() {
    case "${1:-}" in
        start)
            log "Starting production services..."
            check_think_ai || sudo systemctl restart think-ai-full.service
            start_ngrok
            test_stack
            log "🚀 Production stack is running!"
            log "📱 Access at: https://thinkai.lat"
            ;;
        
        stop)
            log "Stopping services..."
            kill_ngrok
            log "Services stopped (Think AI service remains running)"
            ;;
        
        restart)
            log "Restarting services..."
            $0 stop
            sleep 2
            $0 start
            ;;
        
        status)
            log "Checking service status..."
            check_think_ai
            
            if [[ -f "$PID_DIR/ngrok.pid" ]]; then
                local ngrok_pid=$(cat "$PID_DIR/ngrok.pid")
                if ps -p $ngrok_pid > /dev/null; then
                    log "✅ Ngrok is running (PID: $ngrok_pid)"
                else
                    warning "Ngrok is not running"
                fi
            else
                warning "Ngrok is not running"
            fi
            
            test_stack || true
            ;;
        
        monitor)
            log "Starting service monitor..."
            monitor_loop
            ;;
        
        logs)
            log "Showing recent logs..."
            echo -e "\n${GREEN}=== Think AI Logs ===${NC}"
            sudo journalctl -u think-ai-full.service -n 20 --no-pager
            
            echo -e "\n${GREEN}=== Ngrok Logs ===${NC}"
            if [[ -f "$LOG_DIR/ngrok.log" ]]; then
                tail -20 "$LOG_DIR/ngrok.log"
            else
                warning "No ngrok logs found"
            fi
            ;;
        
        test)
            log "Running E2E test..."
            test_stack
            ;;
        
        *)
            echo "Usage: $0 {start|stop|restart|status|monitor|logs|test}"
            echo ""
            echo "Commands:"
            echo "  start    - Start all production services"
            echo "  stop     - Stop ngrok (Think AI service continues)"
            echo "  restart  - Restart all services"
            echo "  status   - Check status of all services"
            echo "  monitor  - Run continuous monitoring (daemon mode)"
            echo "  logs     - Show recent logs from all services"
            echo "  test     - Run full stack test"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"