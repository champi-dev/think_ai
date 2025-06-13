#!/bin/bash
# Setup WSL GPU environment for Think AI

echo "🚀 Setting up WSL GPU environment for Think AI"
echo "=============================================="

# Add CUDA to PATH if it exists
if [ -d "/usr/local/cuda/bin" ]; then
    echo "✅ CUDA found at /usr/local/cuda"
    export PATH=/usr/local/cuda/bin:$PATH
    export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
    
    # Add to bashrc for persistence
    if ! grep -q "CUDA PATH" ~/.bashrc; then
        echo "" >> ~/.bashrc
        echo "# CUDA PATH" >> ~/.bashrc
        echo "export PATH=/usr/local/cuda/bin:\$PATH" >> ~/.bashrc
        echo "export LD_LIBRARY_PATH=/usr/local/cuda/lib64:\$LD_LIBRARY_PATH" >> ~/.bashrc
        echo "✅ Added CUDA to ~/.bashrc"
    fi
else
    echo "❌ CUDA not found at /usr/local/cuda"
fi

# Test nvidia-smi
echo ""
echo "🎮 Testing NVIDIA GPU access..."
if nvidia-smi &>/dev/null; then
    echo "✅ nvidia-smi is working!"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo "❌ nvidia-smi not working"
    echo ""
    echo "📋 WSL GPU Troubleshooting Steps:"
    echo "1. On Windows, open PowerShell as Administrator and run:"
    echo "   wsl --update"
    echo ""
    echo "2. Check Windows NVIDIA driver version:"
    echo "   Open NVIDIA Control Panel → Help → System Information"
    echo "   You need driver version 470.76 or later"
    echo ""
    echo "3. Verify WSL2 (not WSL1):"
    echo "   In PowerShell: wsl -l -v"
    echo "   Your distro should show VERSION 2"
    echo ""
    echo "4. Install latest NVIDIA drivers from:"
    echo "   https://www.nvidia.com/Download/index.aspx"
    echo "   Choose 'Windows 11' and your GPU model"
fi

echo ""
echo "🐍 Python GPU packages recommendation:"
echo "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"

echo ""
echo "✅ Setup complete! Run 'source ~/.bashrc' to apply changes."