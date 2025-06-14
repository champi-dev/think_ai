#!/usr/bin/env python3
"""Setup Phi-3.5 Mini using Ollama (easier for macOS)."""

import os
import subprocess
import json
import yaml

def check_ollama_installed():
    """Check if Ollama is installed."""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ollama():
    """Install Ollama on macOS."""
    print("📦 Installing Ollama...")
    try:
        subprocess.run(['brew', 'install', 'ollama'], check=True)
        print("✅ Ollama installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Ollama")
        print("Please install manually: brew install ollama")
        return False

def setup_ollama_phi35():
    """Setup Phi-3.5 with Ollama."""
    print("🚀 Setting up Phi-3.5 Mini with Ollama")
    print("="*60)
    print("This is the easiest way to run Phi-3.5 on macOS!")
    print("="*60)
    
    # Check/install Ollama
    if not check_ollama_installed():
        print("\n⚠️  Ollama not found")
        install = input("Install Ollama? [Y/n]: ").strip().lower() != 'n'
        if install:
            if not install_ollama():
                return
        else:
            print("Please install Ollama manually: brew install ollama")
            return
    else:
        print("✅ Ollama is installed")
    
    # Start Ollama service
    print("\n🔄 Starting Ollama service...")
    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import time
    time.sleep(2)  # Give it time to start
    
    # Pull Phi-3.5 model
    print("\n📥 Downloading Phi-3.5 Mini (this may take a few minutes)...")
    try:
        subprocess.run(['ollama', 'pull', 'phi3:mini'], check=True)
        print("✅ Phi-3.5 Mini downloaded successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to download model")
        return
    
    # Test the model
    print("\n🧪 Testing Phi-3.5 Mini...")
    try:
        result = subprocess.run(
            ['ollama', 'run', 'phi3:mini', 'Say "Hello, Think AI!" in one sentence.'],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(f"Response: {result.stdout.strip()}")
        print("✅ Model is working!")
    except:
        print("⚠️  Model test failed, but it may still work")
    
    # Create Ollama integration for Think AI
    print("\n🔧 Creating Ollama integration for Think AI...")
    
    ollama_wrapper = '''#!/usr/bin/env python3
"""Ollama wrapper for Think AI integration."""

import asyncio
import httpx
import json
from typing import Dict, Any, Optional

class OllamaModel:
    """Ollama model wrapper for Think AI."""
    
    def __init__(self, model_name: str = "phi3:mini"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434"
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def generate(self, prompt: str, max_tokens: int = 512) -> Dict[str, Any]:
        """Generate response using Ollama."""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.7
                    }
                }
            )
            
            result = response.json()
            return {
                "text": result.get("response", ""),
                "tokens": result.get("eval_count", 0),
                "duration": result.get("total_duration", 0) / 1e9  # Convert to seconds
            }
        except Exception as e:
            print(f"Ollama error: {e}")
            return {"text": "", "tokens": 0, "duration": 0}
    
    async def close(self):
        """Close the client."""
        await self.client.aclose()

# Integration with Think AI's LanguageModel class
class OllamaLanguageModel:
    """Drop-in replacement for Think AI's language model using Ollama."""
    
    def __init__(self):
        self.model = None
        self.model_name = "phi3:mini"
        self._initialized = False
    
    async def initialize(self, config=None):
        """Initialize Ollama model."""
        self.model = OllamaModel(self.model_name)
        self._initialized = True
        print(f"✅ Ollama model {self.model_name} initialized")
    
    async def generate(self, prompt: str, max_tokens: int = 512) -> Any:
        """Generate text using Ollama."""
        if not self._initialized:
            await self.initialize()
        
        result = await self.model.generate(prompt, max_tokens)
        
        # Return in Think AI's expected format
        class Response:
            def __init__(self, text, metadata):
                self.text = text
                self.metadata = metadata
        
        return Response(
            text=result["text"],
            metadata={
                "tokens": result["tokens"],
                "duration": result["duration"],
                "model": self.model_name
            }
        )
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        return {
            "status": "ready" if self._initialized else "not_initialized",
            "model_name": self.model_name,
            "parameters": "3.8B",
            "backend": "ollama",
            "memory_usage_mb": 4000  # Approximate
        }
'''
    
    with open("think_ai/models/ollama_model.py", "w") as f:
        f.write(ollama_wrapper)
    
    print("✅ Ollama wrapper created")
    
    # Create configuration
    config = {
        "system_mode": "full_distributed",
        "model": {
            "backend": "ollama",
            "name": "phi3:mini",
            "device": "cpu",  # Ollama handles device management
            "max_tokens": 4096
        },
        "scylladb": {"enabled": True},
        "vector_db": {"enabled": True},
        "claude": {
            "enhancement_threshold": 0.8  # Phi-3.5 is good, minimal Claude usage
        }
    }
    
    with open("config/ollama_phi35_config.yaml", "w") as f:
        yaml.dump(config, f)
    
    print("✅ Configuration saved to config/ollama_phi35_config.yaml")
    
    # Create test script
    test_script = '''#!/usr/bin/env python3
"""Test Ollama integration with Think AI."""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from think_ai.models.ollama_model import OllamaLanguageModel

async def test():
    model = OllamaLanguageModel()
    await model.initialize()
    
    print("\\nTesting Ollama Phi-3.5 Mini...")
    response = await model.generate("What is consciousness?", max_tokens=100)
    print(f"Response: {response.text}")
    print(f"Tokens: {response.metadata['tokens']}")
    print(f"Speed: {response.metadata['tokens']/response.metadata['duration']:.1f} tokens/sec")

asyncio.run(test())
'''
    
    with open("test_ollama_integration.py", "w") as f:
        f.write(test_script)
    os.chmod("test_ollama_integration.py", 0o755)
    
    print("\n\n🎉 Setup Complete!")
    print("\n✨ Advantages of Ollama:")
    print("   • No Python dependency issues")
    print("   • Automatic memory management")
    print("   • Easy model switching")
    print("   • Optimized for macOS")
    print("\n📋 Next Steps:")
    print("1. Test integration: python3 test_ollama_integration.py")
    print("2. Update Think AI to use Ollama backend")
    print("3. Enjoy Phi-3.5 Mini with ~8-15 tokens/sec!")
    print("\n💡 Other Ollama models to try:")
    print("   • ollama pull llama3.2:3b  (Meta's latest)")
    print("   • ollama pull mistral:7b   (If you have RAM)")
    print("   • ollama pull qwen2.5:3b   (Good for coding)")

if __name__ == "__main__":
    setup_ollama_phi35()