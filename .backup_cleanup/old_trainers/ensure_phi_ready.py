#!/usr/bin/env python3
"""Ensure Phi-3.5 Mini is ready to respond quickly."""

import subprocess
import time
from typing import Optional

import requests

def ensure_ollama_running() -> Optional[bool]:
    """Make sure Ollama is running."""
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        if response.status_code == 200:
            return True
    except Exception:
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        return True

def warm_up_phi() -> Optional[bool]:
    """Warm up Phi-3.5 with a test query."""
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
                    "temperature": 0.1,
                },
            },
            timeout=30,
        )

        return response.status_code == 200

    except Exception:
        return False

if __name__ == "__main__":

    if ensure_ollama_running():
        if warm_up_phi():
            pass
        else:
            pass

