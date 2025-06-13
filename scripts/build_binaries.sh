#!/bin/bash
# Build all Think AI binaries with GPU support

set -e

echo "🔨 Building Think AI binaries with GPU support..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Create binaries directory
BINARIES_DIR="$PROJECT_ROOT/binaries"
mkdir -p "$BINARIES_DIR"

echo -e "\n${BLUE}📁 Output directory: $BINARIES_DIR${NC}"

# Check for NVIDIA GPU
GPU_AVAILABLE=0

# Check if we're in WSL
if [[ -f /proc/version ]] && grep -qi microsoft /proc/version; then
    echo -e "${BLUE}🐧 Running in WSL2${NC}"
    
    # Check for WSL GPU passthrough
    if [[ -e /dev/dxg ]]; then
        echo -e "${GREEN}✅ WSL2 GPU passthrough detected (/dev/dxg exists)${NC}"
        
        # Check if CUDA is available
        if which nvcc &>/dev/null; then
            echo -e "${GREEN}✅ CUDA toolkit found in WSL2${NC}"
            nvcc --version | tail -n1
        fi
        
        # Try nvidia-smi
        if nvidia-smi &>/dev/null; then
            echo -e "${GREEN}✅ NVIDIA GPU detected via nvidia-smi${NC}"
            nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
            GPU_AVAILABLE=1
        else
            echo -e "${YELLOW}⚠️  nvidia-smi not working. Ensure NVIDIA drivers are installed on Windows host.${NC}"
            echo -e "${YELLOW}   WSL2 uses the Windows NVIDIA driver, not Linux drivers.${NC}"
            # Still try to use GPU if /dev/dxg exists and CUDA is available
            if which nvcc &>/dev/null; then
                echo -e "${YELLOW}   Attempting GPU build anyway (CUDA toolkit found)...${NC}"
                GPU_AVAILABLE=1
            fi
        fi
    else
        echo -e "${RED}❌ No WSL2 GPU passthrough (/dev/dxg not found)${NC}"
    fi
else
    # Not in WSL - regular Linux GPU detection
    if ! nvidia-smi &>/dev/null; then
        echo -e "${YELLOW}⚠️  No NVIDIA GPU detected. Building CPU-only binaries...${NC}"
        GPU_AVAILABLE=0
    else
        echo -e "${GREEN}✅ NVIDIA GPU detected${NC}"
        nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
        GPU_AVAILABLE=1
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "\n${YELLOW}🐍 Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip and install build tools
echo -e "\n${YELLOW}📦 Installing build dependencies...${NC}"
pip install --upgrade pip wheel setuptools
pip install pyinstaller cython numpy

# Install PyTorch with CUDA support if GPU is available
if [ $GPU_AVAILABLE -eq 1 ]; then
    echo -e "\n${YELLOW}🚀 Installing PyTorch with CUDA support...${NC}"
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
else
    echo -e "\n${YELLOW}📦 Installing PyTorch (CPU only)...${NC}"
    pip install torch torchvision torchaudio
fi

# Install all project dependencies
echo -e "\n${YELLOW}📦 Installing project dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Build the main Think AI binary
echo -e "\n${BLUE}🔨 Building main Think AI binary...${NC}"
pyinstaller --onefile \
    --name think-ai \
    --distpath "$BINARIES_DIR" \
    --workpath "$PROJECT_ROOT/build" \
    --specpath "$PROJECT_ROOT/build" \
    --hidden-import torch \
    --hidden-import transformers \
    --hidden-import numpy \
    --collect-all torch \
    --collect-all transformers \
    --clean \
    --noconfirm \
    think_ai/__main__.py

# Build worker binary if exists
if [ -f "think_ai/worker.py" ]; then
    echo -e "\n${BLUE}🔨 Building worker binary...${NC}"
    pyinstaller --onefile \
        --name think-ai-worker \
        --distpath "$BINARIES_DIR" \
        --workpath "$PROJECT_ROOT/build" \
        --specpath "$PROJECT_ROOT/build" \
        --hidden-import torch \
        --hidden-import transformers \
        --collect-all torch \
        --clean \
        --noconfirm \
        think_ai/worker.py
fi

# Build inference server if exists
if [ -f "think_ai/inference_server.py" ]; then
    echo -e "\n${BLUE}🔨 Building inference server binary...${NC}"
    pyinstaller --onefile \
        --name think-ai-inference \
        --distpath "$BINARIES_DIR" \
        --workpath "$PROJECT_ROOT/build" \
        --specpath "$PROJECT_ROOT/build" \
        --hidden-import torch \
        --hidden-import transformers \
        --hidden-import fastapi \
        --hidden-import uvicorn \
        --collect-all torch \
        --collect-all transformers \
        --clean \
        --noconfirm \
        think_ai/inference_server.py
fi

# Create a manifest file with build info
echo -e "\n${BLUE}📝 Creating build manifest...${NC}"
cat > "$BINARIES_DIR/manifest.json" << EOF
{
  "build_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "gpu_support": $GPU_AVAILABLE,
  "python_version": "$(python --version 2>&1)",
  "torch_version": "$(python -c 'import torch; print(torch.__version__)' 2>/dev/null || echo 'N/A')",
  "cuda_available": $(python -c 'import torch; print(str(torch.cuda.is_available()).lower())' 2>/dev/null || echo 'false'),
  "binaries": [
    $(ls -1 "$BINARIES_DIR" | grep -v manifest.json | awk '{printf "    \"%s\"", $0} END {print ""}' | sed 's/,$//')
  ]
}
EOF

# Compress binaries for faster Docker builds
echo -e "\n${BLUE}📦 Compressing binaries...${NC}"
cd "$BINARIES_DIR"
tar -czf ../binaries.tar.gz .
cd "$PROJECT_ROOT"

# List built binaries
echo -e "\n${GREEN}✅ Build complete! Built binaries:${NC}"
ls -lh "$BINARIES_DIR"
echo -e "\n${GREEN}📦 Compressed archive: binaries.tar.gz ($(du -h binaries.tar.gz | cut -f1))${NC}"

# Clean up build directory
echo -e "\n${YELLOW}🧹 Cleaning up build artifacts...${NC}"
rm -rf "$PROJECT_ROOT/build"

echo -e "\n${GREEN}🎉 All binaries built successfully!${NC}"