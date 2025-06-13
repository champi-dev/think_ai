#! / usr / bin / env python3

"""Test Qwen model without self-training interference."""

import asyncio
import sys
import time
from pathlib import Path

from think_ai.core.config import ModelConfig
from think_ai.models.language_model import GenerationConfig, LanguageModel

sys.path.insert(0, str(Path(__file__).parent))


async def test_without_self_training() - > None:
"""Test model generation without self-training running."""
# Create config
    config = ModelConfig(
    model_name="Qwen/Qwen2.5-Coder-1.5B-Instruct",
    device="cpu",
    quantization="none",
    torch_dtype="float32",
    max_tokens=150,  # Shorter for testing
    hf_token=None,
    )

# Initialize model
    model = LanguageModel(config)
    start = time.time()
    await model.initialize()
    time.time() - start

# Test questions
    test_prompts = [
    ("hello", 50),
    ("what is the sun?", 100),
    ("write a python hello world", 150),
    ]

    for prompt, max_tokens in test_prompts:

        gen_config = GenerationConfig(
        temperature=0.7,
        max_tokens=max_tokens,
        do_sample=True,
        top_p=0.9,
        )

        start = time.time()
        try:
# Generate without timeout to see actual time
            await model.generate(prompt, gen_config)
            time.time() - start

            except asyncio.TimeoutError:
                pass
            except Exception:
                pass

            if __name__ = = "__main__":
                asyncio.run(test_without_self_training())
