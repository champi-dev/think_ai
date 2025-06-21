#! / usr / bin / env python3

"""Direct test of Mistral - 7B generation."""

import asyncio
import contextlib
import os
import sys
from pathlib import Path

from think_ai.core.config import ModelConfig
from think_ai.models.language_model import GenerationConfig, LanguageModel

sys.path.insert(0, str(Path(__file__).parent))


async def test_mistral() - > None:
"""Test Mistral - 7B directly."""
# Set MPS memory fix
    os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"

# Create config
    config = ModelConfig(
    model_name="mistralai / Mistral - 7B - v0.1",
    device="mps",
    quantization="none",  # Use "none" instead of False
    max_tokens=2048,
    )

# Initialize model
    model = LanguageModel(config, None)
    await model.initialize()

# Test queries
    test_queries = [
    "hello",
    "What is 2 + 2?",
    "Tell me a joke",
    "What is consciousness?",
    ]

    for query in test_queries:

# Generate with ultra - fast config
        config = GenerationConfig(
        temperature=0.7,
        max_tokens=10,  # Ultra short for instant response
        do_sample=True,
        top_p=0.9,
        )

        with contextlib.suppress(Exception):
            await model.generate(query, config)

            if __name__ = = "__main__":
                asyncio.run(test_mistral())
