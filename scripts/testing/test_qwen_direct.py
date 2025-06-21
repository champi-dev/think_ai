#! / usr / bin / env python3

"""Test Qwen model directly for simple questions."""

import asyncio
import sys
from pathlib import Path

import torch

from think_ai.core.config import ModelConfig
from think_ai.models.language_model import GenerationConfig, LanguageModel

sys.path.insert(0, str(Path(__file__).parent))


async def test_direct_response() - > None:
"""Test Qwen model with direct questions."""
# Create model config
    config = ModelConfig(
    model_name="Qwen/Qwen2.5-Coder-1.5B-Instruct",
    device="mps" if torch.backends.mps.is_available() else "cpu",
    quantization="none",
    max_tokens=512,
    hf_token=None,  # Qwen is public
    )

# Initialize model
    model = LanguageModel(config)
    await model.initialize()

# Test questions
    test_questions = [
    "What is the sun?",
    "Hello!",
    "What is 2 + 2?",
    "How are you?",
    "What can you do?",
    ]

    for question in test_questions:

        try:
# Generate response with optimized config
            gen_config = GenerationConfig(
            temperature=0.3,  # Lower for factual answers
            max_tokens=150,  # Reasonable length
            do_sample=False,  # Deterministic
            top_p=0.9,
            repetition_penalty=1.1,
            )

            await model.generate(question, gen_config)

            except Exception:
                pass

            if __name__ = = "__main__":
                asyncio.run(test_direct_response())
