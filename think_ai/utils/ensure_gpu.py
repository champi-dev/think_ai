"""Ensure GPU usage when available."""

import os
import subprocess
from typing import Any, Dict


def ensure_gpu_usage() -> Dict[str, Any]:
    """Ensure GPU is used when available."""
    result = {"gpu_available": False, "device": "cpu", "env_vars_set": []}

    # Check for NVIDIA GPU
    try:
        nvidia_output = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if nvidia_output.returncode == 0:
            result["gpu_available"] = True
            result["device"] = "cuda"

            # Set CUDA environment variables
            if "CUDA_VISIBLE_DEVICES" not in os.environ:
                os.environ["CUDA_VISIBLE_DEVICES"] = "0"
                result["env_vars_set"].append("CUDA_VISIBLE_DEVICES=0")

            # Force GPU usage in Think AI
            os.environ["THINK_AI_DEVICE"] = "cuda"
            result["env_vars_set"].append("THINK_AI_DEVICE=cuda")

    except (FileNotFoundError, subprocess.SubprocessError):
        pass

    # Check for AMD GPU
    try:
        rocm_output = subprocess.run(["rocm-smi"], capture_output=True, text=True)
        if rocm_output.returncode == 0:
            result["gpu_available"] = True
            result["device"] = "cuda"  # ROCm uses CUDA interface
            os.environ["THINK_AI_DEVICE"] = "cuda"
            result["env_vars_set"].append("THINK_AI_DEVICE=cuda")
    except (FileNotFoundError, subprocess.SubprocessError):
        pass

    return result


# Auto-configure on import
gpu_config = ensure_gpu_usage()
