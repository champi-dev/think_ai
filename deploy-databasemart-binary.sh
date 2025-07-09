#!/bin/bash

# Deploy Think AI binaries directly to DatabaseMart GPU Server
# Builds locally and deploys pre-compiled binaries

set -euo pipefail

# Configuration
DEPLOY_USER="${DEPLOY_USER:-deploy}"
DEPLOY_HOST="${DEPLOY_HOST:-gpu.databasemart.com}"
DEPLOY_PATH="${DEPLOY_PATH:-/opt/think-ai}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Build binaries locally
build_binaries() {
    log_info "Building release binaries locally..."
    
    # Clean previous builds
    cargo clean
    
    # Build all binaries
    cargo build --release
    
    # Verify binaries exist
    local binaries=(
        "think-ai-http"
        "think-ai-webapp"
        "think-ai"
        "think-ai-linter"
    )
    
    for binary in "${binaries[@]}"; do
        if [[ ! -f "target/release/$binary" ]]; then
            log_error "Binary $binary not found after build"
            exit 1
        fi
    done
    
    log_info "All binaries built successfully"
}

# Create deployment package
create_deployment_package() {
    log_info "Creating deployment package..."
    
    # Create temporary directory
    local temp_dir=$(mktemp -d)
    local package_dir="$temp_dir/think-ai-deploy"
    
    mkdir -p "$package_dir/bin"
    mkdir -p "$package_dir/systemd"
    mkdir -p "$package_dir/scripts"
    
    # Copy binaries
    cp target/release/think-ai* "$package_dir/bin/" 2>/dev/null || true
    
    # Copy systemd service files
    cp systemd/*.service "$package_dir/systemd/" 2>/dev/null || true
    
    # Copy monitoring scripts
    cp monitor-gpu-performance.sh "$package_dir/scripts/" 2>/dev/null || true
    chmod +x "$package_dir/scripts/"*.sh
    
    # Create setup script
    cat > "$package_dir/setup.sh" << 'EOF'
#!/bin/bash
set -e

INSTALL_PATH="/opt/think-ai"

echo "Setting up Think AI on GPU server..."

# Create directories
sudo mkdir -p $INSTALL_PATH/{bin,data,logs}
sudo mkdir -p /var/log/think-ai

# Copy binaries
sudo cp bin/* $INSTALL_PATH/
sudo chmod +x $INSTALL_PATH/think-ai*

# Create system user
sudo useradd -r -s /bin/false think-ai || true
sudo chown -R think-ai:think-ai $INSTALL_PATH
sudo chown -R think-ai:think-ai /var/log/think-ai

# Install systemd services
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable think-ai-http
sudo systemctl enable think-ai-webapp

echo "Setup complete! Start services with:"
echo "  sudo systemctl start think-ai-http"
echo "  sudo systemctl start think-ai-webapp"
EOF
    
    chmod +x "$package_dir/setup.sh"
    
    # Create tarball
    cd "$temp_dir"
    tar czf think-ai-deploy.tar.gz think-ai-deploy/
    
    # Move to current directory
    mv think-ai-deploy.tar.gz "$OLDPWD/"
    
    # Clean up
    rm -rf "$temp_dir"
    
    log_info "Deployment package created: think-ai-deploy.tar.gz"
}

# Deploy to server
deploy_to_server() {
    log_info "Deploying to DatabaseMart GPU server..."
    
    # Copy deployment package
    log_info "Copying deployment package..."
    scp think-ai-deploy.tar.gz ${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/
    
    # Deploy on server
    ssh ${DEPLOY_USER}@${DEPLOY_HOST} << 'ENDSSH'
set -e

# Extract package
cd /tmp
tar xzf think-ai-deploy.tar.gz
cd think-ai-deploy

# Run setup
./setup.sh

# Clean up
cd /tmp
rm -rf think-ai-deploy think-ai-deploy.tar.gz

echo "Deployment complete!"
ENDSSH
    
    # Clean up local package
    rm think-ai-deploy.tar.gz
    
    log_info "Deployment completed successfully"
}

# Start services on server
start_services() {
    log_info "Starting Think AI services..."
    
    ssh ${DEPLOY_USER}@${DEPLOY_HOST} << 'ENDSSH'
# Check GPU availability
if command -v nvidia-smi &> /dev/null; then
    echo "GPU Status:"
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
fi

# Start services
sudo systemctl start think-ai-http
sudo systemctl start think-ai-webapp

# Check status
sleep 3
sudo systemctl status think-ai-http --no-pager
sudo systemctl status think-ai-webapp --no-pager

# Check endpoints
echo "Checking API health..."
curl -f http://localhost:8080/health && echo " - API is healthy" || echo " - API health check failed"
ENDSSH
}

# Monitor deployment
monitor_deployment() {
    log_info "Monitoring deployment..."
    
    ssh ${DEPLOY_USER}@${DEPLOY_HOST} << 'ENDSSH'
# Show logs
echo "Recent logs from think-ai-http:"
sudo journalctl -u think-ai-http -n 20 --no-pager

echo -e "\nRecent logs from think-ai-webapp:"
sudo journalctl -u think-ai-webapp -n 20 --no-pager

# GPU usage if available
if command -v nvidia-smi &> /dev/null; then
    echo -e "\nGPU Usage:"
    nvidia-smi --query-gpu=utilization.gpu,utilization.memory,temperature.gpu --format=csv
fi
ENDSSH
}

# Main deployment flow
main() {
    log_info "Starting Think AI binary deployment to DatabaseMart GPU server"
    
    # Verify prerequisites
    if ! command -v cargo &> /dev/null; then
        log_error "Rust not found. Please install Rust first."
        exit 1
    fi
    
    # Build and deploy
    build_binaries
    create_deployment_package
    deploy_to_server
    start_services
    monitor_deployment
    
    log_info "Think AI deployed successfully to DatabaseMart GPU server!"
    log_info "Access the service at: http://${DEPLOY_HOST}:8080"
    log_info "Web UI available at: http://${DEPLOY_HOST}:3000"
}

# Run if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi