#!/bin/bash

# Setup NVIDIA GPU for Think AI on DatabaseMart
# Configures CUDA, drivers, and container toolkit

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

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running with sudo
check_sudo() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run with sudo"
        exit 1
    fi
}

# Install NVIDIA drivers
install_nvidia_drivers() {
    log_info "Installing NVIDIA drivers..."
    
    # Add NVIDIA package repositories
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    
    # Remove old GPG key
    apt-key del 7fa2af80 2>/dev/null || true
    
    # Add new GPG key
    wget -qO - https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/3bf863cc.pub | apt-key add -
    
    # Setup CUDA repository
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/ /" > /etc/apt/sources.list.d/cuda.list
    
    # Update and install
    apt-get update
    apt-get install -y cuda-drivers
    
    log_info "NVIDIA drivers installed successfully"
}

# Install NVIDIA Container Toolkit
install_nvidia_container_toolkit() {
    log_info "Installing NVIDIA Container Toolkit..."
    
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list
    
    apt-get update
    apt-get install -y nvidia-container-toolkit
    
    # Configure Docker daemon
    nvidia-ctk runtime configure --runtime=docker
    systemctl restart docker
    
    log_info "NVIDIA Container Toolkit installed successfully"
}

# Configure GPU settings
configure_gpu() {
    log_info "Configuring GPU settings..."
    
    # Set persistence mode
    nvidia-smi -pm 1
    
    # Set power limit (adjust based on GPU model)
    # Example for RTX 3090: 350W
    nvidia-smi -pl 350 2>/dev/null || log_warning "Could not set power limit"
    
    # Configure memory growth
    cat > /etc/modprobe.d/nvidia.conf << EOF
options nvidia NVreg_PreserveVideoMemoryAllocations=1
options nvidia NVreg_TemporaryFilePath=/var/tmp
EOF
    
    # Create CUDA environment script
    cat > /etc/profile.d/cuda.sh << 'EOF'
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda
EOF
    
    log_info "GPU configured successfully"
}

# Setup monitoring
setup_gpu_monitoring() {
    log_info "Setting up GPU monitoring..."
    
    # Create monitoring directory
    mkdir -p /opt/think-ai/monitoring
    
    # Create GPU monitoring script
    cat > /opt/think-ai/monitoring/gpu-monitor.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import json
import time
from datetime import datetime
import os

LOG_DIR = "/var/log/think-ai/gpu"
os.makedirs(LOG_DIR, exist_ok=True)

def get_gpu_stats():
    """Get GPU statistics using nvidia-smi"""
    cmd = [
        "nvidia-smi",
        "--query-gpu=timestamp,name,index,utilization.gpu,utilization.memory,memory.total,memory.used,memory.free,temperature.gpu,power.draw",
        "--format=csv,noheader,nounits"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    
    stats = []
    for line in result.stdout.strip().split('\n'):
        parts = line.split(', ')
        stats.append({
            "timestamp": parts[0],
            "name": parts[1],
            "index": int(parts[2]),
            "gpu_util": float(parts[3]),
            "mem_util": float(parts[4]),
            "mem_total": float(parts[5]),
            "mem_used": float(parts[6]),
            "mem_free": float(parts[7]),
            "temperature": float(parts[8]),
            "power_draw": float(parts[9])
        })
    
    return stats

def main():
    """Main monitoring loop"""
    log_file = os.path.join(LOG_DIR, f"gpu-metrics-{datetime.now().strftime('%Y%m%d')}.jsonl")
    
    while True:
        try:
            stats = get_gpu_stats()
            if stats:
                with open(log_file, 'a') as f:
                    for stat in stats:
                        json.dump(stat, f)
                        f.write('\n')
            
            # Rotate log file daily
            current_date = datetime.now().strftime('%Y%m%d')
            if current_date not in log_file:
                log_file = os.path.join(LOG_DIR, f"gpu-metrics-{current_date}.jsonl")
            
            time.sleep(60)  # Monitor every minute
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
EOF
    
    chmod +x /opt/think-ai/monitoring/gpu-monitor.py
    
    # Create systemd service
    cat > /etc/systemd/system/think-ai-gpu-monitor.service << EOF
[Unit]
Description=Think AI GPU Monitor
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/think-ai/monitoring/gpu-monitor.py
Restart=always
User=think-ai
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable think-ai-gpu-monitor
    
    log_info "GPU monitoring setup complete"
}

# Optimize GPU for ML workloads
optimize_for_ml() {
    log_info "Optimizing GPU for ML workloads..."
    
    # Disable GPU boost for consistent performance
    nvidia-smi -lgc 1350,1350 2>/dev/null || log_warning "Could not lock GPU clocks"
    
    # Set compute mode to exclusive process
    nvidia-smi -c 3
    
    # Configure memory oversubscription
    cat > /etc/nvidia-container-runtime/config.toml << EOF
[nvidia-container-runtime]
  [nvidia-container-runtime.mode]
    compute = "exclusive_process"
  [nvidia-container-runtime.memory]
    oversubscription = true
EOF
    
    log_info "GPU optimized for ML workloads"
}

# Verify installation
verify_installation() {
    log_info "Verifying GPU installation..."
    
    # Check NVIDIA driver
    if ! command -v nvidia-smi &> /dev/null; then
        log_error "nvidia-smi not found"
        return 1
    fi
    
    # Check GPU visibility
    gpu_count=$(nvidia-smi --query-gpu=count --format=csv,noheader | head -1)
    log_info "Found $gpu_count GPU(s)"
    
    # Display GPU info
    nvidia-smi
    
    # Test CUDA
    if command -v nvcc &> /dev/null; then
        nvcc --version
    else
        log_warning "CUDA compiler not found"
    fi
    
    # Test container toolkit
    if docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi &> /dev/null; then
        log_info "Docker GPU support verified"
    else
        log_error "Docker GPU support not working"
        return 1
    fi
    
    return 0
}

# Main setup
main() {
    log_info "Starting NVIDIA GPU setup for Think AI"
    
    check_sudo
    
    # Install components
    install_nvidia_drivers
    install_nvidia_container_toolkit
    
    # Configure
    configure_gpu
    setup_gpu_monitoring
    optimize_for_ml
    
    # Verify
    if verify_installation; then
        log_info "GPU setup completed successfully!"
        log_info "Please reboot the system to ensure all changes take effect"
    else
        log_error "GPU setup encountered errors"
        exit 1
    fi
}

# Run if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi