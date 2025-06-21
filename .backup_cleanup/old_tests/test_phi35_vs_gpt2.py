#!/usr/bin/env python3
"""Compare Phi-3.5 Mini vs GPT-2 for Think AI."""

import asyncio
import time

import httpx
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class ModelComparison:
    """Compare language models."""

    def __init__(self) -> None:
        self.ollama_url = "http://localhost:11434"
        self.gpt2_model = None
        self.gpt2_tokenizer = None

    async def test_phi35(self, prompt: str):
        """Test Phi-3.5 Mini via Ollama."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            start = time.time()
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "phi3:mini",
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 100},
                },
            )
            elapsed = time.time() - start
            result = response.json()
            return {
                "text": result.get("response", ""),
                "tokens": result.get("eval_count", 0),
                "time": elapsed,
                "model": "Phi-3.5 Mini (3.8B)",
            }

    def test_gpt2(self, prompt: str):
        """Test GPT-2."""
        if not self.gpt2_model:
            self.gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
            self.gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")
            self.gpt2_tokenizer.pad_token = self.gpt2_tokenizer.eos_token

        start = time.time()
        inputs = self.gpt2_tokenizer(prompt, return_tensors="pt", padding=True)

        with torch.no_grad():
            outputs = self.gpt2_model.generate(
                inputs.input_ids,
                max_new_tokens=100,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.gpt2_tokenizer.eos_token_id,
            )

        elapsed = time.time() - start
        response = self.gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response[len(prompt) :].strip()

        return {
            "text": response,
            "tokens": len(outputs[0]) - len(inputs.input_ids[0]),
            "time": elapsed,
            "model": "GPT-2 (124M)",
        }

    async def compare_models(self) -> None:
        """Run comprehensive comparison."""
        test_prompts = [
            {
                "category": "Code Generation",
                "prompt": "Write a Python function to find the nth Fibonacci number:",
            },
            {
                "category": "Reasoning",
                "prompt": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly? Explain:",
            },
            {
                "category": "Knowledge",
                "prompt": "What are the main differences between machine learning and deep learning?",
            },
            {
                "category": "Creative",
                "prompt": "Write a haiku about artificial intelligence:",
            },
            {
                "category": "Technical Explanation",
                "prompt": "Explain how a hash table works in simple terms:",
            },
        ]

        results = []

        for test in test_prompts:
            # Test Phi-3.5
            phi35_result = await self.test_phi35(test["prompt"])

            # Test GPT-2
            gpt2_result = self.test_gpt2(test["prompt"])

            # Quality comparison (simple length and coherence check)
            phi35_quality = len(phi35_result["text"].split()) / max(1, phi35_result["tokens"])
            gpt2_quality = len(gpt2_result["text"].split()) / max(1, gpt2_result["tokens"])

            results.append(
                {
                    "category": test["category"],
                    "phi35_speed": phi35_result["tokens"] / phi35_result["time"],
                    "gpt2_speed": gpt2_result["tokens"] / gpt2_result["time"],
                    "phi35_quality": phi35_quality,
                    "gpt2_quality": gpt2_quality,
                }
            )

        # Summary

        sum(r["phi35_speed"] for r in results) / len(results)
        sum(r["gpt2_speed"] for r in results) / len(results)
        sum(r["phi35_quality"] for r in results) / len(results)
        sum(r["gpt2_quality"] for r in results) / len(results)


async def main() -> None:
    """Run the comparison."""
    tester = ModelComparison()
    await tester.compare_models()


if __name__ == "__main__":
    asyncio.run(main())
