#!/bin/bash

# Deploy and start all ThinkAI systemd services
# This script installs, enables, and starts all systemd services

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
SYSTEMD_DIR="/etc/systemd/system"
PROJECT_DIR="/home/administrator/think_ai"
LOG_DIR="$PROJECT_DIR/logs"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[DEPLOY]${NC} $1"
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

# Check if running as root or with sudo
check_permissions() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run with sudo"
        exit 1
    fi
}

# Create necessary directories
setup_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p "$LOG_DIR"
    mkdir -p "$PROJECT_DIR/cache"
    mkdir -p "$PROJECT_DIR/audio_cache"
    
    # Set proper permissions
    chown -R administrator:administrator "$LOG_DIR"
    chown -R administrator:administrator "$PROJECT_DIR/cache"
    chown -R administrator:administrator "$PROJECT_DIR/audio_cache"
    
    print_success "Directories created"
}

# Check if ngrok is installed
check_ngrok() {
    print_status "Checking ngrok installation..."
    
    if ! command -v ngrok &> /dev/null; then
        print_warning "ngrok not found. Installing..."
        
        # Download ngrok
        wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -O /tmp/ngrok.tgz
        tar -xzf /tmp/ngrok.tgz -C /tmp
        mv /tmp/ngrok /usr/local/bin/
        chmod +x /usr/local/bin/ngrok
        rm /tmp/ngrok.tgz
        
        print_success "ngrok installed"
    else
        print_success "ngrok found at: $(which ngrok)"
    fi
}

# Stop existing services
stop_existing_services() {
    print_status "Stopping existing services..."
    
    # Stop services if they exist
    systemctl stop think-ai-main.service 2>/dev/null || true
    systemctl stop think-ai-ngrok.service 2>/dev/null || true
    systemctl stop think-ai-monitor.service 2>/dev/null || true
    
    # Also stop any old services
    systemctl stop think-ai.service 2>/dev/null || true
    systemctl stop think-ai-full.service 2>/dev/null || true
    systemctl stop ngrok.service 2>/dev/null || true
    systemctl stop monitor.service 2>/dev/null || true
    
    print_success "Existing services stopped"
}

# Copy service files
install_service_files() {
    print_status "Installing systemd service files..."
    
    # Copy new service files
    cp "$PROJECT_DIR/systemd/think-ai-main.service" "$SYSTEMD_DIR/"
    cp "$PROJECT_DIR/systemd/think-ai-ngrok.service" "$SYSTEMD_DIR/"
    cp "$PROJECT_DIR/systemd/think-ai-monitor.service" "$SYSTEMD_DIR/"
    
    # Set proper permissions
    chmod 644 "$SYSTEMD_DIR/think-ai-main.service"
    chmod 644 "$SYSTEMD_DIR/think-ai-ngrok.service"
    chmod 644 "$SYSTEMD_DIR/think-ai-monitor.service"
    
    print_success "Service files installed"
}

# Reload systemd
reload_systemd() {
    print_status "Reloading systemd daemon..."
    systemctl daemon-reload
    print_success "Systemd daemon reloaded"
}

# Enable services
enable_services() {
    print_status "Enabling services..."
    
    systemctl enable think-ai-main.service
    systemctl enable think-ai-ngrok.service
    systemctl enable think-ai-monitor.service
    
    print_success "Services enabled"
}

# Start services
start_services() {
    print_status "Starting services..."
    
    # Start main service first
    print_status "Starting Think AI main service..."
    systemctl start think-ai-main.service
    
    # Wait for main service to be ready
    sleep 5
    
    # Check if main service is running
    if systemctl is-active --quiet think-ai-main.service; then
        print_success "Think AI main service started"
    else
        print_error "Failed to start Think AI main service"
        systemctl status think-ai-main.service
        exit 1
    fi
    
    # Start ngrok tunnel
    print_status "Starting ngrok tunnel..."
    systemctl start think-ai-ngrok.service
    sleep 3
    
    if systemctl is-active --quiet think-ai-ngrok.service; then
        print_success "Ngrok tunnel started"
    else
        print_warning "Ngrok service may have issues - check logs"
    fi
    
    # Start monitor
    print_status "Starting monitor service..."
    systemctl start think-ai-monitor.service
    
    if systemctl is-active --quiet think-ai-monitor.service; then
        print_success "Monitor service started"
    else
        print_warning "Monitor service may have issues - check logs"
    fi
}

# Display service status
display_status() {
    echo
    print_status "Service Status:"
    echo
    
    # Show service status
    systemctl status think-ai-main.service --no-pager | head -n 5
    echo
    systemctl status think-ai-ngrok.service --no-pager | head -n 5
    echo
    systemctl status think-ai-monitor.service --no-pager | head -n 5
    
    echo
    print_status "Access Information:"
    echo -e "  ${GREEN}▶${NC} Local: http://localhost:8080"
    echo -e "  ${GREEN}▶${NC} Public: https://thinkai.lat"
    echo
    print_status "Log files:"
    echo -e "  ${GREEN}▶${NC} Main: $LOG_DIR/think-ai-main.log"
    echo -e "  ${GREEN}▶${NC} Ngrok: $LOG_DIR/ngrok.log"
    echo -e "  ${GREEN}▶${NC} Monitor: $LOG_DIR/monitor.log"
    echo
    print_status "Useful commands:"
    echo -e "  ${GREEN}▶${NC} View logs: journalctl -u think-ai-main -f"
    echo -e "  ${GREEN}▶${NC} Restart: sudo systemctl restart think-ai-main"
    echo -e "  ${GREEN}▶${NC} Stop all: sudo systemctl stop think-ai-main think-ai-ngrok think-ai-monitor"
}

# Main execution
main() {
    clear
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║           THINK AI SYSTEMD DEPLOYMENT                        ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo
    
    check_permissions
    setup_directories
    check_ngrok
    stop_existing_services
    install_service_files
    reload_systemd
    enable_services
    start_services
    display_status
    
    echo
    print_success "Deployment completed successfully!"
}

# Run main function
main "$@"