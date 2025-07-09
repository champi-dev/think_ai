#!/bin/bash

# Setup Think AI directly on GPU server
# Run this script on the GPU server after cloning the repo

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Rust
    if ! command -v cargo &> /dev/null; then
        log_info "Installing Rust..."
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source "$HOME/.cargo/env"
    else
        log_info "Rust is installed: $(rustc --version)"
    fi
    
    # Check GPU
    if command -v nvidia-smi &> /dev/null; then
        log_info "GPU detected:"
        nvidia-smi --query-gpu=name,memory.total --format=csv
    else
        log_error "No GPU detected. Is NVIDIA driver installed?"
    fi
}

# 2. Build the project
build_project() {
    log_info "Building Think AI..."
    
    # Clean and build
    cargo clean
    cargo build --release
    
    # Check binaries
    if [[ -f target/release/think-ai-http ]]; then
        log_info "Build successful!"
    else
        log_error "Build failed!"
        exit 1
    fi
}

# 3. Setup directories and permissions
setup_directories() {
    log_info "Setting up directories..."
    
    # Create required directories
    mkdir -p data logs
    mkdir -p /tmp/think-ai
    
    # Set permissions
    chmod 755 data logs
}

# 4. Kill any existing processes
kill_existing() {
    log_info "Stopping any existing Think AI processes..."
    
    # Kill existing processes
    pkill -f "think-ai" || true
    
    # Kill processes on ports
    sudo fuser -k 8080/tcp 2>/dev/null || true
    sudo fuser -k 3000/tcp 2>/dev/null || true
    
    sleep 2
}

# 5. Start services
start_services() {
    log_info "Starting Think AI services..."
    
    # Export GPU environment
    export RUST_LOG=info
    export THINK_AI_GPU_ENABLED=true
    export CUDA_VISIBLE_DEVICES=0
    
    # Start HTTP server
    log_info "Starting HTTP server on port 8080..."
    nohup ./target/release/think-ai-http > logs/http.log 2>&1 &
    HTTP_PID=$!
    echo $HTTP_PID > /tmp/think-ai/http.pid
    
    # Wait for HTTP server to start
    sleep 3
    
    # Start webapp
    log_info "Starting webapp on port 3000..."
    nohup ./target/release/think-ai-webapp > logs/webapp.log 2>&1 &
    WEBAPP_PID=$!
    echo $WEBAPP_PID > /tmp/think-ai/webapp.pid
    
    # Wait for services to stabilize
    sleep 3
    
    # Check if services are running
    if ps -p $HTTP_PID > /dev/null; then
        log_info "HTTP server running (PID: $HTTP_PID)"
    else
        log_error "HTTP server failed to start. Check logs/http.log"
    fi
    
    if ps -p $WEBAPP_PID > /dev/null; then
        log_info "Webapp running (PID: $WEBAPP_PID)"
    else
        log_error "Webapp failed to start. Check logs/webapp.log"
    fi
}

# 6. Verify deployment
verify_deployment() {
    log_info "Verifying deployment..."
    
    # Check HTTP health
    if curl -f http://localhost:8080/health > /dev/null 2>&1; then
        log_info "✓ HTTP API is healthy"
    else
        log_error "✗ HTTP API health check failed"
    fi
    
    # Check webapp
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log_info "✓ Webapp is accessible"
    else
        log_error "✗ Webapp not accessible"
    fi
    
    # Show logs
    echo -e "\n${YELLOW}Recent HTTP logs:${NC}"
    tail -n 10 logs/http.log || true
    
    echo -e "\n${YELLOW}Recent webapp logs:${NC}"
    tail -n 10 logs/webapp.log || true
}

# Main execution
main() {
    log_info "Setting up Think AI on GPU server..."
    
    # Run setup steps
    check_prerequisites
    build_project
    setup_directories
    kill_existing
    start_services
    verify_deployment
    
    echo -e "\n${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Think AI is now running!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "HTTP API: http://localhost:8080"
    echo -e "Web UI:   http://localhost:3000"
    echo -e "\nTo monitor:"
    echo -e "  tail -f logs/http.log"
    echo -e "  tail -f logs/webapp.log"
    echo -e "\nTo stop:"
    echo -e "  ./stop-services.sh"
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi