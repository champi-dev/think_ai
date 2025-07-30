#!/usr/bin/env python3
"""Test GPU usage configuration"""

import subprocess
import os

def check_gpu_availability():
    """Check if GPU is available and configured"""
    print("=== GPU Availability Check ===")
    
    # Check NVIDIA GPU
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ NVIDIA GPU detected")
            print(result.stdout.split('\n')[0:10])  # Print first 10 lines
        else:
            print("✗ No NVIDIA GPU detected")
    except FileNotFoundError:
        print("✗ nvidia-smi not found")
    
    # Check environment variables
    print("\n=== Environment Variables ===")
    gpu_vars = ['CUDA_VISIBLE_DEVICES', 'THINK_AI_GPU_ENABLED', 'CUDA_HOME']
    for var in gpu_vars:
        value = os.environ.get(var, 'Not set')
        print(f"{var}: {value}")
    
    # Check if GPU detection is working in the project
    print("\n=== Project GPU Detection ===")
    try:
        # Run the GPU detector test
        result = subprocess.run(
            ['cargo', 'test', 'test_gpu_detection', '--', '--nocapture'],
            cwd='/home/administrator/think_ai/think-ai-core',
            capture_output=True,
            text=True
        )
        print("GPU Detection Test Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Error running GPU detection test: {e}")

if __name__ == "__main__":
    check_gpu_availability()