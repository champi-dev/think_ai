#! / usr / bin / env python3

"""Clear evidence that the Qwen model is working."""

import asyncio

from think_ai.core.config import ModelConfig
from think_ai.models.language_model import GenerationConfig, LanguageModel


async def prove_model_works() - > None:
"""Prove that Qwen model works and generates real responses."""
# 1. Initialize model
    config = ModelConfig(
    model_name="Qwen/Qwen2.5-Coder-1.5B-Instruct",
    device="cpu",
    torch_dtype="float32",
    quantization="none",
    )

    model = LanguageModel(config)
    await model.initialize()

# 2. Test multiple questions

    test_cases = [
    ("What is Mars?", [
    "planet", "fourth", "solar system", "red"]), ("What is a black hole?", [
    "gravity", "space", "light", "escape"]), ("Explain artificial intelligence", [
    "computer", "learn", "intelligence", "system"]), ("Hello!", [
    "hello", "hi", "greet", "help"]), ]

    for question, expected_words in test_cases:

        response = await model.generate(
        question,
        GenerationConfig(max_tokens=50, temperature=0.7),
        )

# Check if response contains expected content
        response_lower = response.text.lower()
        found_words = [word for word in expected_words if word in response_lower]

        if found_words:
            pass
    else:
        pass

# Show it's not a fallback
    if "fallback" in str(response.metadata):
        pass
else:
    pass

# 3. Show model info
model_info = await model.get_model_info()
for _key, _value in model_info.items():
    pass

if __name__ = = "__main__":
    asyncio.run(prove_model_works())
