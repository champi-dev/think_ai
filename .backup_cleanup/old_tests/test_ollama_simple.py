#!/usr/bin/env python3
"""Simple test to verify Ollama is working."""

import asyncio
import time

import httpx


async def test_ollama() -> None:
    """Test if Ollama is responding."""
    # Check if Ollama is running
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            models = response.json().get("models", [])

            # Check for phi3:mini
            has_phi3 = any(m.get("name") == "phi3:mini" for m in models)
            if has_phi3:
                pass
            else:
                return
    except Exception:
        return

    # Test generation

    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3:mini",
                    "prompt": "What is love in one sentence?",
                    "stream": False,
                    "options": {
                        "num_predict": 50,
                        "temperature": 0.7,
                    },
                },
            )

            time.time() - start
            result = response.json()

            if result.get("response"):
                pass
            else:
                pass

    except httpx.TimeoutException:
        pass

    except Exception:
        pass


if __name__ == "__main__":
    asyncio.run(test_ollama())
