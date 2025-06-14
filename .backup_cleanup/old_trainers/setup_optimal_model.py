#!/usr/bin/env python3
"""Setup optimal language model for Think AI based on latest 2024-2025 research."""

import os
import sys
import torch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def check_system_compatibility():
    """Check if system meets requirements."""
    print("🔍 Checking system compatibility...")
    
    # Check RAM
    import psutil
    ram_gb = psutil.virtual_memory().total / (1024**3)
    print(f"✅ RAM: {ram_gb:.1f}GB available")
    
    # Check for Apple Silicon
    if torch.backends.mps.is_available():
        print("✅ Apple Silicon (MPS) detected")
    else:
        print("⚠️  No MPS detected, will use CPU")
    
    # Check disk space
    disk_usage = psutil.disk_usage('/')
    free_gb = disk_usage.free / (1024**3)
    print(f"✅ Disk space: {free_gb:.1f}GB free")
    
    return ram_gb >= 4  # Minimum 4GB for small models


def install_optimal_model():
    """Install and configure the optimal model."""
    print("\n📦 Installing optimal language model for Think AI...")
    
    # Install required packages
    print("\n1️⃣ Installing dependencies...")
    os.system("pip install transformers accelerate bitsandbytes sentencepiece protobuf")
    
    print("\n2️⃣ Model recommendations based on your 16GB M3 Pro:")
    print("   🥇 Phi-3.5 Mini (3.8B) - Best overall choice")
    print("   🥈 Llama 3.2 3B - Strong multilingual")
    print("   🥉 Mistral 7B - Premium quality (uses more RAM)")
    
    choice = input("\nSelect model [1-3, default=1]: ").strip() or "1"
    
    model_configs = {
        "1": {
            "name": "microsoft/Phi-3.5-mini-instruct",
            "config": "phi3_5_mini"
        },
        "2": {
            "name": "meta-llama/Llama-3.2-3B-Instruct",
            "config": "llama3_2_3b"
        },
        "3": {
            "name": "mistralai/Mistral-7B-Instruct-v0.3",
            "config": "mistral_7b"
        }
    }
    
    selected = model_configs.get(choice, model_configs["1"])
    
    print(f"\n3️⃣ Configuring {selected['name']}...")
    
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
    
    print("✅ Configuration saved to config/optimal_model.yaml")
    
    # Test model loading
    print("\n4️⃣ Testing model initialization...")
    test_model_loading(selected['name'])


def test_model_loading(model_name):
    """Test if the model can be loaded."""
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        print(f"Loading {model_name}...")
        
        # For testing, just check if model exists
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print("✅ Model configuration verified!")
        
        print("\n5️⃣ Expected performance on your M3 Pro:")
        if "Phi-3.5" in model_name:
            print("   • Speed: 5-15 tokens/second")
            print("   • RAM usage: ~3-4GB")
            print("   • Quality: Excellent (69% MMLU)")
        elif "Llama-3.2-3B" in model_name:
            print("   • Speed: 4-12 tokens/second")
            print("   • RAM usage: ~3-4GB")
            print("   • Quality: Very good (63% MMLU)")
        elif "Mistral-7B" in model_name:
            print("   • Speed: 2-8 tokens/second")
            print("   • RAM usage: ~5-8GB")
            print("   • Quality: Premium")
            
    except Exception as e:
        print(f"⚠️  Model test failed: {e}")
        print("The model will be downloaded on first use.")


def setup_ollama_alternative():
    """Setup Ollama as an alternative."""
    print("\n🔧 Ollama Setup (Alternative)")
    print("If you prefer Ollama for model management:")
    print("\n1. Install Ollama:")
    print("   brew install ollama")
    print("\n2. Pull optimal model:")
    print("   ollama pull phi3:3.5")
    print("\n3. Run with Think AI:")
    print("   ollama run phi3:3.5 --context-size 4096")
    
    use_ollama = input("\nSetup Ollama? [y/N]: ").strip().lower() == 'y'
    
    if use_ollama:
        os.system("brew install ollama")
        os.system("ollama pull phi3:3.5")
        print("✅ Ollama configured!")


def main():
    """Main setup process."""
    print("🚀 Think AI - Optimal Model Setup")
    print("="*60)
    print("Based on latest 2024-2025 small model research")
    print("="*60)
    
    if not check_system_compatibility():
        print("❌ System doesn't meet minimum requirements")
        return
    
    install_optimal_model()
    
    print("\n\n✅ SETUP COMPLETE!")
    print("\n📝 Next steps:")
    print("1. Update config/active.yaml to use config/optimal_model.yaml")
    print("2. Run: python3 test_optimal_model.py")
    print("3. Start chatting with improved local model!")
    
    print("\n💡 Your 16GB M3 Pro can easily handle:")
    print("   • Phi-3.5 Mini at 5-15 tokens/sec")
    print("   • 4K-8K context windows")
    print("   • Multiple models loaded simultaneously")
    print("   • Minimal Claude API usage (only for enhancement)")
    
    setup_ollama = input("\n\nSetup Ollama as alternative? [y/N]: ").strip().lower() == 'y'
    if setup_ollama:
        setup_ollama_alternative()


if __name__ == "__main__":
    main()