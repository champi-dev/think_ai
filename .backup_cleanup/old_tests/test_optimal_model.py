#!/usr/bin/env python3
"""Test the optimal language model configuration for Think AI."""

import asyncio
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.core.config import ModelConfig
from think_ai.models.language_model import LanguageModel


async def test_model_performance() -> None:
    """Test the configured model's performance."""
    # Load configuration
    config = ModelConfig(
        model_name="microsoft/Phi-3.5-mini-instruct",  # Or your selected model
        device="mps" if torch.backends.mps.is_available() else "cpu",
        quantization="4bit",
        max_tokens=512,
    )

    # Initialize model
    model = LanguageModel()

    try:
        await model.initialize(config)

        # Get model info
        info = await model.get_model_info()

        # Test generation speed

        test_prompts = [
            "What is consciousness?",
            "Write a Python function to calculate fibonacci numbers:",
            "Explain quantum computing in simple terms:",
        ]

        for prompt in test_prompts:
            start_time = time.time()
            response = await model.generate(prompt, max_tokens=100)
            end_time = time.time()

            tokens_generated = len(response.text.split())
            time_taken = end_time - start_time
            tokens_per_second = tokens_generated / time_taken

        # Compare with expected performance

        if "Phi-3.5" in config.model_name or "Llama-3.2-3B" in config.model_name or "Mistral-7B" in config.model_name:
            pass

        # Test integration with Think AI

        # Test consciousness framework integration
        test_query = "Is it ethical to shut down an AI system?"

        response = await model.generate(
            f"From an ethical AI perspective: {test_query}",
            max_tokens=150,
        )

        if tokens_per_second < 2 or tokens_per_second > 10:
            pass
        else:
            pass

    except Exception:
        pass
    finally:
        if "model" in locals():
            # Cleanup
            pass


async def compare_with_gpt2() -> None:
    """Compare new model with current GPT-2."""
    # Load GPT-2 (current)
    gpt2_config = ModelConfig(
        model_name="gpt2",
        device="mps" if torch.backends.mps.is_available() else "cpu",
        max_tokens=100,
    )

    gpt2_model = LanguageModel()
    await gpt2_model.initialize(gpt2_config)

    # Test prompt
    prompt = "The future of artificial intelligence is"

    # GPT-2 response
    start = time.time()
    await gpt2_model.generate(prompt)
    time.time() - start

    # New model response (simulate)


async def main() -> None:
    """Run all tests."""
    await test_model_performance()
    await compare_with_gpt2()


if __name__ == "__main__":
    asyncio.run(main())
