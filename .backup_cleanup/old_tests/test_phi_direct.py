#!/usr/bin/env python3
"""Test Phi-3.5 Mini directly."""

import time

import requests

def test_phi(prompt, max_tokens=50) -> None:
    """Test Phi-3.5 with a prompt."""
    start_time = time.time()

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.7,
                    "top_k": 40,
                    "top_p": 0.9,
                },
            },
            timeout=15,
        )

        time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            result.get("response", "")
        else:
            pass

    except requests.exceptions.Timeout:
        pass
    except Exception:
        pass

if __name__ == "__main__":

    # Test queries
    test_phi("Hello", max_tokens=20)
    test_phi("What is love?", max_tokens=50)
    test_phi("Question: What is 2+2?\nAnswer:", max_tokens=10)

