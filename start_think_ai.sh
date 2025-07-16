#!/bin/bash

# Think AI Complete System Launcher
# This script starts all Think AI components with proper error handling and monitoring

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SERVER_PORT=8080
SERVER_HOST="0.0.0.0"
LOG_DIR="./logs"
PID_FILE="./think_ai.pid"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[Think AI]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_info() {
    echo -e "${CYAN}[i]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to kill all Think AI processes on exit
cleanup() {
    print_warning "Shutting down Think AI services..."
    
    # Kill specific PIDs if available
    if [ -f "$PID_FILE" ]; then
        while read -r pid; do
            if kill -0 "$pid" 2>/dev/null; then
                kill -TERM "$pid" 2>/dev/null || true
            fi
        done < "$PID_FILE"
        rm -f "$PID_FILE"
    fi
    
    # Kill all Think AI processes
    pkill -f "think-ai" 2>/dev/null || true
    pkill -f "train-knowledge" 2>/dev/null || true
    
    # Kill processes on specific ports
    lsof -ti:$SERVER_PORT | xargs kill -9 2>/dev/null || true
    
    print_success "All services stopped"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    if ! command_exists cargo; then
        print_error "Rust/Cargo not found! Please install Rust from https://rustup.rs/"
        exit 1
    fi
    
    if ! command_exists jq; then
        print_warning "jq not found. Some features may not work properly."
        print_info "Install with: sudo apt install jq (Ubuntu) or brew install jq (macOS)"
    fi
    
    print_success "Prerequisites check passed"
}

# Build the project if needed
build_project() {
    if [ ! -f "./target/release/think-ai" ] || [ "$1" == "--rebuild" ]; then
        print_status "Building Think AI in release mode..."
        
        if cargo build --release; then
            print_success "Build completed successfully"
        else
            print_error "Build failed!"
            exit 1
        fi
    else
        print_info "Using existing build (use --rebuild to force rebuild)"
    fi
}

# Create log directory
setup_logging() {
    if [ ! -d "$LOG_DIR" ]; then
        mkdir -p "$LOG_DIR"
        print_success "Created log directory: $LOG_DIR"
    fi
}

# Clear old logs
clear_logs() {
    if [ "$1" == "--clear-logs" ]; then
        rm -f "$LOG_DIR"/*.log
        print_info "Cleared old log files"
    fi
}

# Check and kill existing processes on port
check_port() {
    if lsof -Pi :$SERVER_PORT -sTCP:LISTEN -t >/dev/null; then
        print_warning "Port $SERVER_PORT is already in use. Killing existing process..."
        lsof -ti:$SERVER_PORT | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
}

# Start the HTTP server
start_server() {
    print_status "Starting HTTP server on http://$SERVER_HOST:$SERVER_PORT..."
    
    ./target/release/think-ai server --host $SERVER_HOST --port $SERVER_PORT > "$LOG_DIR/server.log" 2>&1 &
    local server_pid=$!
    echo $server_pid >> "$PID_FILE"
    
    # Wait for server to start
    local retries=0
    while [ $retries -lt 10 ]; do
        if curl -s "http://localhost:$SERVER_PORT/health" >/dev/null 2>&1; then
            print_success "Server started successfully (PID: $server_pid)"
            print_success "Web interface: ${GREEN}http://localhost:$SERVER_PORT${NC}"
            return 0
        fi
        sleep 1
        retries=$((retries + 1))
    done
    
    print_error "Server failed to start. Check $LOG_DIR/server.log for details"
    return 1
}

# Start knowledge training (optional)
start_knowledge_training() {
    if [ "$1" == "--with-training" ]; then
        print_status "Starting knowledge training in background..."
        
        if [ -f "./target/release/train-knowledge" ]; then
            ./target/release/train-knowledge > "$LOG_DIR/training.log" 2>&1 &
            local training_pid=$!
            echo $training_pid >> "$PID_FILE"
            print_success "Knowledge training started (PID: $training_pid)"
        else
            print_warning "Knowledge training binary not found. Skipping..."
        fi
    fi
}

# Monitor system health
monitor_system() {
    if [ "$1" == "--monitor" ]; then
        print_status "Starting system monitor..."
        
        (
            while true; do
                if curl -s "http://localhost:$SERVER_PORT/health" >/dev/null 2>&1; then
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] System healthy" >> "$LOG_DIR/monitor.log"
                else
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] System unhealthy!" >> "$LOG_DIR/monitor.log"
                fi
                sleep 30
            done
        ) &
        local monitor_pid=$!
        echo $monitor_pid >> "$PID_FILE"
        print_success "System monitor started (PID: $monitor_pid)"
    fi
}

# Display system status
display_status() {
    echo
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║                   🧠 THINK AI SYSTEM STATUS                      ║${NC}"
    echo -e "${PURPLE}╠══════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${PURPLE}║${NC} ${GREEN}▶${NC} Web Interface:    ${CYAN}http://localhost:$SERVER_PORT${NC}"
    echo -e "${PURPLE}║${NC} ${GREEN}▶${NC} API Health:       ${CYAN}http://localhost:$SERVER_PORT/health${NC}"
    echo -e "${PURPLE}║${NC} ${GREEN}▶${NC} API Docs:         ${CYAN}http://localhost:$SERVER_PORT/docs${NC}"
    echo -e "${PURPLE}║${NC} ${GREEN}▶${NC} Server Logs:      ${CYAN}tail -f $LOG_DIR/server.log${NC}"
    
    if [ -f "$LOG_DIR/training.log" ]; then
        echo -e "${PURPLE}║${NC} ${GREEN}▶${NC} Training Logs:    ${CYAN}tail -f $LOG_DIR/training.log${NC}"
    fi
    
    if [ -f "$LOG_DIR/monitor.log" ]; then
        echo -e "${PURPLE}║${NC} ${GREEN}▶${NC} Monitor Logs:     ${CYAN}tail -f $LOG_DIR/monitor.log${NC}"
    fi
    
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo
}

# Start interactive mode
start_interactive() {
    if [ "$1" != "--daemon" ]; then
        print_status "Starting Think AI Interactive Chat..."
        print_info "Type 'help' for available commands"
        echo
        
        # Run the CLI (this will be interactive)
        ./target/release/think-ai chat
        
        print_status "Chat session ended"
    else
        print_info "Running in daemon mode. Use 'tail -f $LOG_DIR/server.log' to view logs"
        print_info "Press Ctrl+C to stop all services"
        
        # Keep the script running
        while true; do
            sleep 1
        done
    fi
}

# Main execution
main() {
    clear
    
    # Display banner
    echo -e "${BLUE}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════╗
║                      🧠 THINK AI SYSTEM LAUNCHER                      ║
╠═══════════════════════════════════════════════════════════════════════╣
║     O(1) Performance AI with Consciousness Framework v4.0             ║
╚═══════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    # Parse command line arguments
    REBUILD=""
    CLEAR_LOGS=""
    WITH_TRAINING=""
    MONITOR=""
    DAEMON=""
    
    for arg in "$@"; do
        case $arg in
            --rebuild) REBUILD="--rebuild" ;;
            --clear-logs) CLEAR_LOGS="--clear-logs" ;;
            --with-training) WITH_TRAINING="--with-training" ;;
            --monitor) MONITOR="--monitor" ;;
            --daemon) DAEMON="--daemon" ;;
            --help)
                echo "Usage: $0 [OPTIONS]"
                echo
                echo "Options:"
                echo "  --rebuild        Force rebuild the project"
                echo "  --clear-logs     Clear old log files"
                echo "  --with-training  Start knowledge training in background"
                echo "  --monitor        Enable system health monitoring"
                echo "  --daemon         Run in daemon mode (no interactive chat)"
                echo "  --help           Show this help message"
                echo
                echo "Examples:"
                echo "  $0                     # Start with interactive chat"
                echo "  $0 --daemon --monitor  # Run as daemon with monitoring"
                echo "  $0 --rebuild --clear-logs --with-training"
                exit 0
                ;;
        esac
    done
    
    # Execute startup sequence
    check_prerequisites
    build_project "$REBUILD"
    setup_logging
    clear_logs "$CLEAR_LOGS"
    check_port
    
    # Start services
    if start_server; then
        start_knowledge_training "$WITH_TRAINING"
        monitor_system "$MONITOR"
        display_status
        
        # Health check
        print_status "Performing health check..."
        if HEALTH=$(curl -s "http://localhost:$SERVER_PORT/health"); then
            print_success "Health check passed: $(echo $HEALTH | jq -r '.status // "unknown"')"
        else
            print_warning "Health check failed"
        fi
        
        # Start interactive mode or daemon
        start_interactive "$DAEMON"
    else
        print_error "Failed to start system"
        exit 1
    fi
}

# Run main function
main "$@"