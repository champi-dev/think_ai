#!/bin/bash

# Deploy Think AI to DatabaseMart GPU Server
# Optimized for NVIDIA GPU acceleration and O(1) performance

set -euo pipefail

# Configuration
DEPLOY_USER="${DEPLOY_USER:-deploy}"
DEPLOY_HOST="${DEPLOY_HOST:-gpu.databasemart.com}"
DEPLOY_PATH="${DEPLOY_PATH:-/opt/think-ai}"
DOCKER_IMAGE="think-ai-gpu"
DOCKER_TAG="${DOCKER_TAG:-latest}"

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

# Build optimized Docker image with GPU support
build_gpu_image() {
    log_info "Building GPU-optimized Docker image..."
    
    # Create GPU-specific Dockerfile
    cat > Dockerfile.gpu << 'EOF'
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Configure DNS for better reliability
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && \
    echo "nameserver 8.8.4.4" >> /etc/resolv.conf

# Install Rust and system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    libssl-dev \
    ca-certificates \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.cargo/bin:${PATH}"
ENV CARGO_NET_RETRY=10
ENV CARGO_HTTP_TIMEOUT=300

WORKDIR /app

# Copy entire project
COPY . .

# Build release binaries (no GPU feature needed)
RUN cargo build --release

# Expose ports
EXPOSE 8080 3000

# Run with GPU support
CMD ["./target/release/think-ai-http"]
EOF

    # Build with DNS configuration
    docker build --network=host -f Dockerfile.gpu -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
    
    log_info "Docker image built successfully"
}

# Deploy to DatabaseMart server
deploy_to_server() {
    log_info "Deploying to DatabaseMart GPU server..."
    
    # Save Docker image
    docker save ${DOCKER_IMAGE}:${DOCKER_TAG} | gzip > think-ai-gpu.tar.gz
    
    # Copy to server
    log_info "Copying Docker image to server..."
    scp think-ai-gpu.tar.gz ${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/
    
    # Deploy script
    ssh ${DEPLOY_USER}@${DEPLOY_HOST} << 'ENDSSH'
set -e

# Ensure NVIDIA Container Toolkit is installed
if ! command -v nvidia-container-cli &> /dev/null; then
    echo "Installing NVIDIA Container Toolkit..."
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
    sudo systemctl restart docker
fi

# Load Docker image
echo "Loading Docker image..."
gunzip -c /tmp/think-ai-gpu.tar.gz | docker load
rm /tmp/think-ai-gpu.tar.gz

# Stop existing container if running
docker stop think-ai || true
docker rm think-ai || true

# Create deployment directory
sudo mkdir -p /opt/think-ai/{data,logs}
sudo chown -R $USER:$USER /opt/think-ai

# Run with GPU support
echo "Starting Think AI with GPU acceleration..."
docker run -d \
    --name think-ai \
    --gpus all \
    --restart unless-stopped \
    -p 8080:8080 \
    -p 3000:3000 \
    -v /opt/think-ai/data:/app/data \
    -v /opt/think-ai/logs:/app/logs \
    -e RUST_LOG=info \
    -e THINK_AI_GPU_ENABLED=true \
    -e THINK_AI_GPU_MEMORY_FRACTION=0.8 \
    think-ai-gpu:latest

# Verify GPU access
echo "Verifying GPU access..."
docker exec think-ai nvidia-smi

echo "Deployment complete!"
ENDSSH
    
    # Clean up local file
    rm think-ai-gpu.tar.gz
    
    log_info "Deployment completed successfully"
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    ssh ${DEPLOY_USER}@${DEPLOY_HOST} << 'ENDSSH'
# Check container status
if docker ps | grep -q think-ai; then
    echo "Container is running"
else
    echo "ERROR: Container is not running"
    exit 1
fi

# Check GPU utilization
echo "GPU Status:"
docker exec think-ai nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv

# Check API endpoints
echo "Checking API health..."
curl -f http://localhost:8080/health || echo "WARNING: Health endpoint not responding"

# Check logs
echo "Recent logs:"
docker logs --tail 20 think-ai
ENDSSH
}

# Monitor GPU performance
setup_monitoring() {
    log_info "Setting up GPU monitoring..."
    
    ssh ${DEPLOY_USER}@${DEPLOY_HOST} << 'ENDSSH'
# Create monitoring script
cat > /opt/think-ai/monitor-gpu.sh << 'EOF'
#!/bin/bash
# Monitor GPU utilization for Think AI

LOG_FILE="/opt/think-ai/logs/gpu-metrics.log"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    GPU_INFO=$(docker exec think-ai nvidia-smi --query-gpu=timestamp,name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader)
    echo "${TIMESTAMP},${GPU_INFO}" >> ${LOG_FILE}
    sleep 60
done
EOF

chmod +x /opt/think-ai/monitor-gpu.sh

# Create systemd service for monitoring
sudo tee /etc/systemd/system/think-ai-gpu-monitor.service > /dev/null << 'EOF'
[Unit]
Description=Think AI GPU Monitor
After=docker.service

[Service]
Type=simple
User=deploy
ExecStart=/opt/think-ai/monitor-gpu.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable think-ai-gpu-monitor
sudo systemctl start think-ai-gpu-monitor
ENDSSH
}

# Main deployment flow
main() {
    log_info "Starting Think AI deployment to DatabaseMart GPU server"
    
    # Verify prerequisites
    if ! command -v docker &> /dev/null; then
        log_error "Docker not found. Please install Docker first."
        exit 1
    fi
    
    if ! command -v cargo &> /dev/null; then
        log_error "Rust not found. Please install Rust first."
        exit 1
    fi
    
    # Build and deploy
    build_gpu_image
    deploy_to_server
    health_check
    setup_monitoring
    
    log_info "Think AI deployed successfully to DatabaseMart GPU server!"
    log_info "Access the service at: http://${DEPLOY_HOST}:8080"
    log_info "Web UI available at: http://${DEPLOY_HOST}:3000"
    log_info "Monitor GPU usage: ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'tail -f /opt/think-ai/logs/gpu-metrics.log'"
}

# Run if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi