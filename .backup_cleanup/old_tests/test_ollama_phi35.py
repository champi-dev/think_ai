#!/usr/bin/env python3
"""Test Ollama Phi-3.5 Mini integration with Think AI."""

import asyncio
import time

import httpx


class OllamaModel:
    """Simple Ollama wrapper for testing."""

    def __init__(self) -> None:
        self.base_url = "http://localhost:11434"
        self.model = "phi3:mini"

    async def test_connection(self):
        """Test if Ollama is running."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
            except Exception:
                return False

    async def generate(self, prompt: str):
        """Generate response using Ollama."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                start = time.time()

                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": 100,
                        },
                    },
                )

                result = response.json()
                time.time() - start

                text = result.get("response", "")
                result.get("eval_count", 0)

                return text

            except Exception:
                return None


async def main() -> None:
    """Test Ollama Phi-3.5 Mini."""
    model = OllamaModel()

    # Check connection
    connected = await model.test_connection()

    if not connected:
        return

    # Test queries

    test_prompts = [
        "What is consciousness in one sentence?",
        "Write a Python function to reverse a string.",
        "Explain quantum computing simply.",
    ]

    for prompt in test_prompts:
        await model.generate(prompt)


if __name__ == "__main__":
    asyncio.run(main())
