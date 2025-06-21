#!/usr/bin/env python3
"""Test Phi-3.5 Mini on macOS without bitsandbytes."""

import asyncio
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


async def test_phi35_mac() -> None:
    """Test Phi-3.5 Mini model on macOS."""
    # Load model without quantization for macOS
    start = time.time()

    try:
        # For macOS, we'll use float16 without quantization
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3.5-mini-instruct",
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            attn_implementation="eager",  # Avoid flash attention issues
        )

        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3.5-mini-instruct",
            trust_remote_code=True,
        )

        time.time() - start

        # Check memory usage
        if torch.backends.mps.is_available():
            pass

        # Test generation
        prompts = [
            "What is consciousness?",
            "Write a Python function to calculate factorial:",
            "Explain machine learning in simple terms:",
        ]

        for prompt in prompts:
            messages = [{"role": "user", "content": prompt}]
            inputs = tokenizer.apply_chat_template(
                messages,
                return_tensors="pt",
                add_generation_prompt=True,
            )

            if torch.backends.mps.is_available():
                inputs = inputs.to("mps")

            start = time.time()
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_new_tokens=100,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                )

            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract just the assistant's response
            if "<|assistant|>" in response:
                response = response.split("<|assistant|>")[-1].strip()

            gen_time = time.time() - start
            tokens = len(outputs[0]) - len(inputs[0])
            tokens / gen_time

        # Memory usage estimate
        sum(p.numel() * p.element_size() for p in model.parameters()) / (1024**3)

    except Exception:
        pass


if __name__ == "__main__":
    asyncio.run(test_phi35_mac())
