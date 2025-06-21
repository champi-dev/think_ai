#!/usr/bin/env python3
"""Setup optimal language model for Think AI based on latest 2024-2025 research."""

import os
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).parent))


def check_system_compatibility():
    """Check if system meets requirements."""
    # Check RAM
    import psutil

    ram_gb = psutil.virtual_memory().total / (1024**3)

    # Check for Apple Silicon
    if torch.backends.mps.is_available():
        pass
    else:
        pass

    # Check disk space
    disk_usage = psutil.disk_usage("/")
    disk_usage.free / (1024**3)

    return ram_gb >= 4  # Minimum 4GB for small models


def install_optimal_model() -> None:
    """Install and configure the optimal model."""
    # Install required packages
    os.system("pip install transformers accelerate bitsandbytes sentencepiece protobuf")

    choice = input("\nSelect model [1-3, default=1]: ").strip() or "1"

    model_configs = {
        "1": {
            "name": "microsoft/Phi-3.5-mini-instruct",
            "config": "phi3_5_mini",
        },
        "2": {
            "name": "meta-llama/Llama-3.2-3B-Instruct",
            "config": "llama3_2_3b",
        },
        "3": {
            "name": "mistralai/Mistral-7B-Instruct-v0.3",
            "config": "mistral_7b",
        },
    }

    selected = model_configs.get(choice, model_configs["1"])

    # Update config
    config_content = f"""# Auto-configured optimal model for Think AI
system_mode: "full_distributed"

model:
  name: "{selected['name']}"
  device: "mps"
  quantization: "4bit"
  load_in_4bit: true
  max_tokens: 4096

  # Memory optimization for 16GB system
  max_memory: {{0: "8GB"}}  # Leave 8GB for OS and other services

  # Performance settings
  torch_dtype: "float16"
  low_cpu_mem_usage: true

# ScyllaDB settings
scylladb:
  enabled: true
  hosts: ["localhost"]

# Vector database
vector_db:
  enabled: true
  provider: "milvus"

# Claude integration
claude:
  enhancement_threshold: 0.7  # Only use Claude when local model confidence < 70%
"""

    with open("config/optimal_model.yaml", "w") as f:
        f.write(config_content)

    # Test model loading
    test_model_loading(selected["name"])


def test_model_loading(model_name) -> None:
    """Test if the model can be loaded."""
    try:
        from transformers import AutoTokenizer

        # For testing, just check if model exists
        AutoTokenizer.from_pretrained(model_name)

        if "Phi-3.5" in model_name or "Llama-3.2-3B" in model_name or "Mistral-7B" in model_name:
            pass

    except Exception:
        pass


def setup_ollama_alternative() -> None:
    """Setup Ollama as an alternative."""
    use_ollama = input("\nSetup Ollama? [y/N]: ").strip().lower() == "y"

    if use_ollama:
        os.system("brew install ollama")
        os.system("ollama pull phi3:3.5")


def main() -> None:
    """Main setup process."""
    if not check_system_compatibility():
        return

    install_optimal_model()

    setup_ollama = input("\n\nSetup Ollama as alternative? [y/N]: ").strip().lower() == "y"
    if setup_ollama:
        setup_ollama_alternative()


if __name__ == "__main__":
    main()
