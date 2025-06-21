#!/usr/bin/env python3
"""Test GPU availability in WSL environment."""

import os
import subprocess
import sys

print("🔍 GPU Detection Test for WSL")
print("=" * 50)

# Check if we're in WSL
is_wsl = os.path.exists("/proc/version") and "microsoft" in open("/proc/version").read().lower()
print(f"Running in WSL: {is_wsl}")

# Check WSL GPU passthrough
if os.path.exists("/dev/dxg"):
    print("✅ /dev/dxg exists - WSL2 GPU passthrough available")
else:
    print("❌ /dev/dxg not found - WSL2 GPU passthrough not available")

# Check CUDA
print("\n🔧 CUDA Check:")
cuda_check = subprocess.run(["which", "nvcc"], capture_output=True, text=True)
if cuda_check.returncode == 0:
    print(f"✅ CUDA found: {cuda_check.stdout.strip()}")
    # Get CUDA version
    cuda_version = subprocess.run([cuda_check.stdout.strip(), "--version"], capture_output=True, text=True)
    if cuda_version.returncode == 0:
        print(cuda_version.stdout.split("\n")[-2])
else:
    print("❌ CUDA not found in PATH")

# Check nvidia-smi
print("\n🎮 NVIDIA Driver Check:")
nvidia_smi = subprocess.run(["which", "nvidia-smi"], capture_output=True, text=True)
if nvidia_smi.returncode == 0:
    print(f"✅ nvidia-smi found: {nvidia_smi.stdout.strip()}")
    # Run nvidia-smi
    gpu_info = subprocess.run(
        ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
        capture_output=True,
        text=True,
    )
    if gpu_info.returncode == 0:
        print(f"   GPU: {gpu_info.stdout.strip()}")
else:
    print("❌ nvidia-smi not found")
    print("   This usually means NVIDIA drivers are not installed on Windows host")
    print("   or WSL2 GPU support is not properly configured.")

# Try to import and use PyTorch
print("\n🐍 PyTorch Check:")
try:
    import torch

    print(f"✅ PyTorch version: {torch.__version__}")
    print(f"   CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   CUDA version: {torch.version.cuda}")
        print(f"   GPU count: {torch.cuda.device_count()}")
        print(f"   GPU name: {torch.cuda.get_device_name(0)}")
    else:
        print("   ⚠️ CUDA not available in PyTorch")
        print("   This could mean:")
        print("   - PyTorch CPU-only version is installed")
        print("   - NVIDIA drivers not properly installed")
        print("   - CUDA toolkit version mismatch")
except ImportError:
    print("❌ PyTorch not installed")
    print(
        "   Install with: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
    )

# Environment variables
print("\n🌍 Environment Variables:")
cuda_visible = os.environ.get("CUDA_VISIBLE_DEVICES", "not set")
print(f"   CUDA_VISIBLE_DEVICES: {cuda_visible}")

ld_library_path = os.environ.get("LD_LIBRARY_PATH", "not set")
if "cuda" in ld_library_path.lower():
    print(f"   LD_LIBRARY_PATH includes CUDA: ✅")
else:
    print(f"   LD_LIBRARY_PATH: {ld_library_path}")
    if ld_library_path == "not set":
        print("   ⚠️ Consider adding CUDA to LD_LIBRARY_PATH")

# WSL-specific recommendations
if is_wsl:
    print("\n💡 WSL GPU Setup Instructions:")
    print("1. Ensure you have Windows 11 or Windows 10 21H2+")
    print("2. Install latest NVIDIA GPU drivers on Windows (not in WSL)")
    print("3. The Windows driver should include WSL2 support")
    print("4. Do NOT install NVIDIA drivers inside WSL")
    print("5. CUDA toolkit can be installed in WSL")
    print("\nFor more info: https://docs.nvidia.com/cuda/wsl-user-guide/index.html")
