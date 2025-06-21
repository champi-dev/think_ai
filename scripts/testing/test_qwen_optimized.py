#! / usr / bin / env python3

"""Test Qwen with optimizations for M1 Mac."""

import asyncio
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


async def test_optimized_qwen() - > None:
"""Test Qwen with various optimizations."""
    model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

# Test different configurations
    configs = [
    {"device": "cpu", "dtype": torch.float32, "name": "CPU Float32"},
    {"device": "cpu", "dtype": torch.float16, "name": "CPU Float16"},
    ]

# Add MPS if available
    if torch.backends.mps.is_available():
        configs.append({"device": "mps",
        "dtype": torch.float16,
        "name": "MPS Float16"})

        for config in configs:

            try:
# Load model
                start = time.time()
                tokenizer = AutoTokenizer.from_pretrained(
                model_name, trust_remote_code=True)

                model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=config["dtype"],
                low_cpu_mem_usage=True,
                trust_remote_code=True,
                )

# Move to device
                if config["device"] ! = "cpu":
                    model = model.to(config["device"])

                    model.eval()
                    time.time() - start

# Test generation
                    test_prompt = "What is the sun?"
                    inputs = tokenizer(test_prompt, return_tensors="pt")

# Move inputs to device
                    if config["device"] ! = "cpu":
                        inputs = {k: v.to(config["device"]) for k, v in inputs.items()}

# Generate with optimizations
                        start = time.time()
                        with torch.no_grad():
                            outputs = model.generate(
                            inputs["input_ids"],
                            max_new_tokens=50,  # Short for testing
                            temperature=0.3,
                            do_sample=False,  # Deterministic
                            use_cache=True,  # Enable KV cache
                            num_beams=1,  # Greedy decoding
                            )

                            time.time() - start

# Decode
                            tokenizer.decode(
                            outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

# Cleanup
                            del model
                            if config["device"] = = "mps":
                                torch.mps.empty_cache()
                                torch.cuda.empty_cache() if torch.cuda.is_available() else None

                                except Exception:
                                    pass

                                if __name__ = = "__main__":
                                    asyncio.run(test_optimized_qwen())
