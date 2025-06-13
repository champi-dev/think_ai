#! / usr / bin / env python3

"""Test fast generation with incremental approach."""

import asyncio
import sys
from pathlib import Path

from think_ai.core.config import ModelConfig
from think_ai.models.fast_language_model import FastGenerationConfig, FastLanguageModel

sys.path.insert(0, str(Path(__file__).parent))


async def test_fast_generation() - > None:
"""Test the fast generation approach."""
# Create config
    config = ModelConfig(
    model_name="Qwen/Qwen2.5-Coder-1.5B-Instruct",
    device="cpu",
    torch_dtype="float16",
    max_tokens=50,  # Small for testing
    )

# Initialize fast model
    model = FastLanguageModel(config)
    await model.initialize()

# Test prompts
    test_prompts = [
    "What is the sun?",
    "Hello, how are you today?",
    "Write a simple Python function",
    "Explain AI in one sentence",
    ]

    for prompt in test_prompts:

# Test incremental generation
        config1 = FastGenerationConfig(
        max_tokens=30,
        incremental=True,
        temperature=0.7,
        )
        await model.generate_fast(prompt, config1)

# Test standard generation
        config2 = FastGenerationConfig(
        max_tokens=30,
        incremental=False,
        temperature=0.7,
        )
        await model.generate_fast(prompt, config2)

# Compare

# Test cache
        await model.generate_fast(test_prompts[0], config1)

        if __name__ = = "__main__":
            asyncio.run(test_fast_generation())
