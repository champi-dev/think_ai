#!/usr/bin/env python3
"""Ensure Phi-3.5 Mini is ready to respond quickly."""

import requests
import time
import subprocess


def ensure_ollama_running():
    """Make sure Ollama is running."""
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
    except:
        print("⚠️  Ollama not running. Starting...")
        subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        return True


def warm_up_phi():
    """Warm up Phi-3.5 with a test query."""
    print("🔥 Warming up Phi-3.5 Mini...")
    
    try:
        # Simple test query
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": "Hello",
                "stream": False,
                "options": {
                    "num_predict": 5,
                    "temperature": 0.1
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Phi-3.5 Mini is ready!")
            return True
        else:
            print(f"❌ Phi-3.5 error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Could not warm up Phi-3.5: {e}")
        print("   Try: ollama run phi3:mini")
        return False


if __name__ == "__main__":
    print("🚀 Preparing Phi-3.5 Mini for Think AI...")
    
    if ensure_ollama_running():
        if warm_up_phi():
            print("\n✨ Phi-3.5 is ready for fast responses!")
        else:
            print("\n⚠️  Phi-3.5 may be slow on first queries")
    
    print("\nYou can now run: python chat_while_training.py")