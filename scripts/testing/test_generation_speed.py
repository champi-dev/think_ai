#!/usr / bin / env python3

"""Test generation speed on MPS."""

import os
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import HUGGINGFACE_API_KEY

os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"

try:
    token = HUGGINGFACE_API_KEY
    except Exception:
        token = os.getenv("HF_TOKEN")

        model_name = "mistralai / Mistral - 7B - v0.1"

        print("Loading model...")
        tokenizer = AutoTokenizer.from_pretrained(
        model_name, token=token, local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained(
        model_name,
        token=token,
        local_files_only=True,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
        )

# Test on different devices
        devices = ["cpu"]
        if torch.backends.mps.is_available():
            devices.append("mps")

            for device in devices:
                print(f"\n{" = "*50}")
                print(f"Testing on {device.upper()}")
                print("="*50)

                model = model.to(device)

                test_prompts = [
                ("Hello", 5),
                ("What is 2 + 2?", 10),
                ("Tell me about AI", 20)
                ]

                for prompt, max_tokens in test_prompts:
                    print(f"\nPrompt: "{prompt}" (max_tokens={max_tokens})")

                    inputs = tokenizer(prompt, return_tensors="pt")
                    inputs = {k: v.to(device) for k, v in inputs.items()}

# Warmup
                    with torch.no_grad():
                        _ = model.generate(inputs["input_ids"], max_new_tokens=1, do_sample=False)

# Timed generation
                        start = time.time()
                        with torch.no_grad():
                            outputs = model.generate(
                            inputs["input_ids"],
                            max_new_tokens=max_tokens,
                            do_sample=True,
                            temperature=0.7,
                            top_p=0.9
                            )
                            elapsed = time.time() - start

                            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                            tokens_per_sec = max_tokens / elapsed

                            print(f"Response: {response}")
                            print(f"Time: {elapsed:.2f}s ({tokens_per_sec:.1f} tokens / sec)")
