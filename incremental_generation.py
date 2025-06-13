#! / usr / bin / env python3

"""Incremental generation approach - build context word by word."""

import asyncio
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class IncrementalGenerator:
"""Generate text by building context incrementally."""

    def __init__(self, model_name="Qwen/Qwen2.5-Coder-1.5B-Instruct") - > None:
        self.model_name = model_name
        self.model = None
        self.tokenizer = None

        async def initialize(self) - > None:
"""Load model and tokenizer."""
            self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            )

            self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
            use_cache=True,  # Important for incremental!
            )
            self.model.eval()

            async def generate_incremental(self, prompt, max_new_tokens=50):
"""Generate response by building context incrementally."""
                words = prompt.split()

# Start with empty context
                context = ""
                past_key_values = None

# Build context word by word
                for i, word in enumerate(words):
                    if i = = 0:
                        context = word
                    else:
                        context + = " " + word

# Tokenize current context
                        inputs = self.tokenizer(context, return_tensors="pt")

# Use past key values for efficiency
                        with torch.no_grad():
                            outputs = self.model(
                            inputs["input_ids"],
                            past_key_values=past_key_values,
                            use_cache=True,
                            )
                            past_key_values = outputs.past_key_values

# Now generate the response with full context cached
                            start = time.time()

# Generate continuation
                            with torch.no_grad():
                                outputs = self.model.generate(
                                inputs["input_ids"],
                                past_key_values=past_key_values,
                                max_new_tokens=max_new_tokens,
                                do_sample=True,
                                temperature=0.7,
                                top_p=0.9,
                                use_cache=True,
                                pad_token_id=self.tokenizer.eos_token_id,
                                )

                                time.time() - start

# Decode only the generated part
                                return self.tokenizer.decode(
                            outputs[0][inputs["input_ids"].shape[1]:],
                            skip_special_tokens=True,
                            )

                            async def generate_standard(self, prompt, max_new_tokens=50):
"""Standard generation for comparison."""
                                inputs = self.tokenizer(prompt, return_tensors="pt")

                                start = time.time()
                                with torch.no_grad():
                                    outputs = self.model.generate(
                                    inputs["input_ids"],
                                    max_new_tokens=max_new_tokens,
                                    do_sample=True,
                                    temperature=0.7,
                                    top_p=0.9,
                                    use_cache=True,
                                    pad_token_id=self.tokenizer.eos_token_id,
                                    )
                                    time.time() - start

                                    return self.tokenizer.decode(
                                outputs[0][inputs["input_ids"].shape[1]:],
                                skip_special_tokens=True,
                                )


                                async def test_incremental() - > None:
"""Test incremental vs standard generation."""
                                    gen = IncrementalGenerator()
                                    await gen.initialize()

                                    test_prompts = [
                                    "What is the sun?",
                                    "Write a Python hello world program",
                                    "Explain artificial intelligence in simple terms",
                                    ]

                                    for prompt in test_prompts:

# Incremental approach
                                        await gen.generate_incremental(prompt, max_new_tokens=30)

# Standard approach
                                        await gen.generate_standard(prompt, max_new_tokens=30)

                                        if __name__ = = "__main__":
                                            asyncio.run(test_incremental())
