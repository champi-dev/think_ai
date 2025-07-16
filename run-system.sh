#!/bin/bash

# Think AI Full System Runner
# This script starts all Think AI components with proper checks and monitoring

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${PROJECT_ROOT}/logs"
PID_DIR="${PROJECT_ROOT}/pids"
BUILD_MODE="${1:-release}" # debug or release

# Create necessary directories
mkdir -p "$LOG_DIR" "$PID_DIR"

# Helper functions
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Kill process on port
kill_port() {
    local port=$1
    log "Checking port $port..."
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        warning "Port $port is in use, killing process..."
        kill -9 $(lsof -t -i:$port) 2>/dev/null || true
        sleep 1
    fi
}

# Start service with logging
start_service() {
    local name=$1
    local cmd=$2
    local port=$3
    local pid_file="${PID_DIR}/${name}.pid"
    local log_file="${LOG_DIR}/${name}.log"
    
    log "Starting $name..."
    
    # Kill existing process if running
    if [ -f "$pid_file" ]; then
        old_pid=$(cat "$pid_file")
        if kill -0 "$old_pid" 2>/dev/null; then
            warning "Killing existing $name process (PID: $old_pid)"
            kill -9 "$old_pid" 2>/dev/null || true
        fi
        rm -f "$pid_file"
    fi
    
    # Kill port if specified
    if [ ! -z "$port" ]; then
        kill_port "$port"
    fi
    
    # Start service
    nohup $cmd > "$log_file" 2>&1 &
    local pid=$!
    echo $pid > "$pid_file"
    
    # Wait for service to start
    sleep 2
    
    # Check if service is running
    if kill -0 "$pid" 2>/dev/null; then
        success "$name started (PID: $pid)"
        return 0
    else
        error "$name failed to start. Check $log_file for details"
        tail -n 20 "$log_file"
        return 1
    fi
}

# Check service health
check_health() {
    local name=$1
    local url=$2
    local max_attempts=10
    local attempt=1
    
    log "Checking $name health..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            success "$name is healthy"
            return 0
        fi
        log "Waiting for $name to be ready... (attempt $attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done
    
    error "$name health check failed"
    return 1
}

# Stop all services
stop_all() {
    log "Stopping all Think AI services..."
    
    for pid_file in "$PID_DIR"/*.pid; do
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            name=$(basename "$pid_file" .pid)
            if kill -0 "$pid" 2>/dev/null; then
                log "Stopping $name (PID: $pid)"
                kill -TERM "$pid" 2>/dev/null || true
                sleep 1
                kill -9 "$pid" 2>/dev/null || true
            fi
            rm -f "$pid_file"
        fi
    done
    
    # Clean up ports
    for port in 8080 8081 8082 9090; do
        kill_port "$port"
    done
    
    success "All services stopped"
}

# Build system
build_system() {
    log "Building Think AI system in $BUILD_MODE mode..."
    
    cd "$PROJECT_ROOT"
    
    if [ "$BUILD_MODE" == "release" ]; then
        cargo build --release
    else
        cargo build
    fi
    
    if [ $? -eq 0 ]; then
        success "Build completed successfully"
    else
        error "Build failed"
        exit 1
    fi
}

# Main execution
main() {
    clear
    echo "======================================"
    echo "     Think AI System Runner v1.0      "
    echo "======================================"
    echo
    
    # Parse command
    case "${2:-start}" in
        start)
            # Stop existing services
            stop_all
            
            # Build if needed
            if [ ! -f "$PROJECT_ROOT/target/$BUILD_MODE/think-ai" ]; then
                warning "Binaries not found, building system..."
                build_system
            fi
            
            # Set binary path
            if [ "$BUILD_MODE" == "release" ]; then
                BIN_PATH="$PROJECT_ROOT/target/release"
            else
                BIN_PATH="$PROJECT_ROOT/target/debug"
            fi
            
            # Start core services
            log "Starting Think AI core services..."
            
            # 1. HTTP Server (port 8080)
            start_service "http-server" "$BIN_PATH/think-ai server" 8080
            check_health "HTTP Server" "http://localhost:8080/health"
            
            # 2. Process Manager (if exists)
            if [ -f "$BIN_PATH/think-ai-process-manager" ]; then
                start_service "process-manager" "$BIN_PATH/think-ai-process-manager" ""
            fi
            
            # 3. Knowledge Service (if exists)
            if [ -f "$BIN_PATH/think-ai-knowledge" ]; then
                start_service "knowledge-service" "$BIN_PATH/think-ai-knowledge serve" 8081
            fi
            
            # 4. Vector Service (if exists)
            if [ -f "$BIN_PATH/think-ai-vector" ]; then
                start_service "vector-service" "$BIN_PATH/think-ai-vector serve" 8082
            fi
            
            # Show status
            echo
            echo "======================================"
            echo "     System Status                    "
            echo "======================================"
            echo -e "${GREEN}HTTP Server:${NC} http://localhost:8080"
            echo -e "${GREEN}Health Check:${NC} http://localhost:8080/health"
            echo -e "${GREEN}Web Interface:${NC} http://localhost:8080"
            echo
            echo "Logs: $LOG_DIR"
            echo "PIDs: $PID_DIR"
            echo
            success "Think AI system is running!"
            echo
            echo "Commands:"
            echo "  ./run-system.sh [debug|release] start   - Start system"
            echo "  ./run-system.sh [debug|release] stop    - Stop system"
            echo "  ./run-system.sh [debug|release] restart - Restart system"
            echo "  ./run-system.sh [debug|release] status  - Show status"
            echo "  ./run-system.sh [debug|release] logs    - Tail logs"
            echo "  ./run-system.sh [debug|release] build   - Build system"
            ;;
            
        stop)
            stop_all
            ;;
            
        restart)
            stop_all
            sleep 2
            exec "$0" "$BUILD_MODE" start
            ;;
            
        status)
            echo "Think AI System Status"
            echo "====================="
            echo
            for pid_file in "$PID_DIR"/*.pid; do
                if [ -f "$pid_file" ]; then
                    pid=$(cat "$pid_file")
                    name=$(basename "$pid_file" .pid)
                    if kill -0 "$pid" 2>/dev/null; then
                        echo -e "${GREEN}✓${NC} $name (PID: $pid) - Running"
                    else
                        echo -e "${RED}✗${NC} $name (PID: $pid) - Not running"
                    fi
                fi
            done
            
            echo
            echo "Port Status:"
            for port in 8080 8081 8082; do
                if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
                    echo -e "${GREEN}✓${NC} Port $port - In use"
                else
                    echo -e "${RED}✗${NC} Port $port - Free"
                fi
            done
            ;;
            
        logs)
            log "Tailing all service logs..."
            tail -f "$LOG_DIR"/*.log
            ;;
            
        build)
            build_system
            ;;
            
        *)
            error "Unknown command: ${2}"
            echo "Usage: $0 [debug|release] {start|stop|restart|status|logs|build}"
            exit 1
            ;;
    esac
}

# Trap for cleanup
trap 'error "Script interrupted"; stop_all; exit 1' INT TERM

# Run main
main "$@"