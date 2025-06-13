#! / usr / bin / env python3

"""Test Qwen model in CPU mode after MPS fix."""

import asyncio
import sys
from pathlib import Path

from think_ai.core.config import ModelConfig
from think_ai.models.language_model import GenerationConfig, LanguageModel

sys.path.insert(0, str(Path(__file__).parent))


async def test_cpu_mode() - > None:
"""Test model in CPU mode."""
# Load config
    config = ModelConfig(
    model_name="Qwen/Qwen2.5-Coder-1.5B-Instruct",
    device="cpu",  # Force CPU
    quantization="none",
    torch_dtype="float32",  # Stable dtype
    max_tokens=512,
    hf_token=None,
    )

# Initialize
    model = LanguageModel(config)

    try:
        await model.initialize()

# Test generation
        test_prompts = [
        "What is the sun?",
        "Hello!",
        "Write a Python hello world program",
        ]

        for prompt in test_prompts:

            gen_config = GenerationConfig(
            temperature=0.7,
            max_tokens=150,
            do_sample=True,
            )

            await model.generate(prompt, gen_config)

            except Exception:
                pass

            if __name__ = = "__main__":
                asyncio.run(test_cpu_mode())
