#! / usr / bin / env python3

"""Test that Meta tensor fix is working."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

from think_ai.core.config import ModelConfig
from think_ai.models.language_model import GenerationConfig, LanguageModel

sys.path.insert(0, str(Path(__file__).parent))


async def test_meta_fix() - > Optional[bool]:
"""Test model with Meta tensor fix."""
# Create config matching current settings
    config = ModelConfig(
    model_name="Qwen/Qwen2.5-Coder-1.5B-Instruct",
    device="cpu",
    torch_dtype="float16",
    max_tokens=50,
    )

# Initialize model
    model = LanguageModel(config)

    try:
        await model.initialize()

# Test simple generation
        gen_config = GenerationConfig(
        temperature=0.7,
        max_tokens=30,
        do_sample=True,
        )

        test_prompts = [
        "Hello",
        "What is the sun?",
        "Hi there",
        ]

        for prompt in test_prompts:

            try:
                await model.generate(prompt, gen_config)
                except Exception as e:
                    if "Meta tensor" in str(e):
                        return False

                    return True

                except Exception:
                    return False

                if __name__ = = "__main__":
                    success = asyncio.run(test_meta_fix())
                    if success:
                        pass
                else:
                    pass
