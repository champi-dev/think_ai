#!/usr/bin/env python3
"""Test Ollama directly."""

import requests
import json

# Test Ollama connection
print("Testing Ollama connection...")

# Check if Ollama is running
try:
    response = requests.get("http://localhost:11434/api/tags")
    print(f"Ollama status: {response.status_code}")
    print(f"Models: {response.json()}")
except Exception as e:
    print(f"Error connecting to Ollama: {e}")
    exit(1)

# Test generation
print("\nTesting generation...")

queries = [
    "What is passion?",
    "Hello, how are you?",
    "Explain love in one sentence."
]

for query in queries:
    print(f"\n{'='*50}")
    print(f"Query: {query}")
    print(f"{'='*50}")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": query,
                "stream": False,
                "options": {
                    "num_predict": 100,
                    "temperature": 0.7
                }
            },
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result.get('response', 'No response')}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.Timeout:
        print("Timeout after 30 seconds")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")