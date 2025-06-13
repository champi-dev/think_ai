#!/usr/bin/env python3
"""Test Phi-3.5 Mini integration with Think AI."""

import asyncio
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

async def test_phi35() -> None:
    """Test Phi-3.5 Mini model."""
    # Quantization config
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )

    # Load model
    start = time.time()

    model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Phi-3.5-mini-instruct",
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.float16,
    )

    tokenizer = AutoTokenizer.from_pretrained(
        "microsoft/Phi-3.5-mini-instruct",
        trust_remote_code=True,
    )

    time.time() - start

    # Test generation
    prompts = [
        "What is consciousness?",
        "Write a Python function to reverse a string:",
        "Explain quantum computing simply:",
    ]

    for prompt in prompts:

        messages = [{"role": "user", "content": prompt}]
        inputs = tokenizer.apply_chat_template(messages, return_tensors="pt")

        if torch.backends.mps.is_available():
            inputs = inputs.to("mps")

        start = time.time()
        outputs = model.generate(
            inputs,
            max_new_tokens=100,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.split("Assistant:")[-1].strip()

        gen_time = time.time() - start
        tokens = len(outputs[0]) - len(inputs[0])
        tokens / gen_time

if __name__ == "__main__":
    asyncio.run(test_phi35())
