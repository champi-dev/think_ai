#!/usr/bin/env python3
"""Test Ollama directly."""

import sys

import requests

# Test Ollama connection

# Check if Ollama is running
try:
    response = requests.get("http://localhost:11434/api/tags")
except Exception:
    sys.exit(1)

# Test generation

queries = [
    "What is passion?",
    "Hello, how are you?",
    "Explain love in one sentence.",
]

for query in queries:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": query,
                "stream": False,
                "options": {
                    "num_predict": 100,
                    "temperature": 0.7,
                },
            },
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
        else:
            pass

    except requests.exceptions.Timeout:
        pass
    except Exception:
        pass
