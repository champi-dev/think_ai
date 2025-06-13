#! / usr / bin / env python3

"""Debug why Mistral - 7B is timing out."""

import asyncio
import os
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import HUGGINGFACE_API_KEY

os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"


async def debug_generation():
    print("🔍 DEBUGGING MISTRAL - 7B TIMEOUT")
    print("=" * 50)

# Import token
    try:
        token = HUGGINGFACE_API_KEY
        except Exception:
            token = os.getenv("HF_TOKEN")

            cache_dir = os.path.expanduser("~/.cache / think_ai_models")
            model_name = "mistralai / Mistral - 7B - v0.1"

            print("1. Loading tokenizer...")
            start = time.time()
            tokenizer = AutoTokenizer.from_pretrained(
            model_name, cache_dir=cache_dir, token=token)
            print(f" ✅ Tokenizer loaded in {time.time() - start:.2f}s")

            print("\n2. Loading model...")
            start = time.time()
            model = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            token=token
            )
            print(f" ✅ Model loaded in {time.time() - start:.2f}s")

# Check device
            print("\n3. Device check:")
            print(f" - MPS available: {torch.backends.mps.is_available()}")
            print(" - Current device: CPU")

            if torch.backends.mps.is_available():
                print("\n4. Moving to MPS...")
                start = time.time()
                model = model.to("mps")
                print(f" ✅ Moved to MPS in {time.time() - start:.2f}s")

# Test generation
                print("\n5. Testing generation...")
                test_prompt = "Hello, I am"
                print(f" Prompt: "{test_prompt}"")

# Tokenize
                start = time.time()
                inputs = tokenizer(test_prompt, return_tensors="pt")
                if torch.backends.mps.is_available():
                    inputs = {k: v.to("mps") for k, v in inputs.items()}
                    print(f" ✅ Tokenized in {time.time() - start:.2f}s")

# Try different generation configs
                    configs = [
                    {"max_new_tokens": 5, "do_sample": False},
                    {"max_new_tokens": 5, "do_sample": True, "temperature": 0.7},
                    {"max_new_tokens": 10, "do_sample": True, "temperature": 0.7, "top_p": 0.9}
                    ]

                    for i, config in enumerate(configs):
                        print(f"\n6.{i + 1} Generating with config: {config}")
                        start = time.time()

                        try:
# Use asyncio timeout
                            outputs = await asyncio.wait_for(
                            asyncio.get_event_loop().run_in_executor(
                            None,
                            lambda: model.generate(inputs.input_ids, * * config)
                            ),
                            timeout=15.0
                            )

                            elapsed = time.time() - start
                            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                            print(f" ✅ Generated in {elapsed:.2f}s: "{response}"")

                            except asyncio.TimeoutError:
                                print(" ❌ TIMEOUT after 15 seconds!")
                                except Exception as e:
                                    print(f" ❌ ERROR: {e}")

# Test CPU generation
                                    print("\n7. Testing CPU generation as comparison...")
                                    model_cpu = model.to("cpu")
                                    inputs_cpu = tokenizer(test_prompt, return_tensors="pt")

                                    start = time.time()
                                    try:
                                        outputs = model_cpu.generate(
                                        inputs_cpu.input_ids,
                                        max_new_tokens=5,
                                        do_sample=False)
                                        elapsed = time.time() - start
                                        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                                        print(f" ✅ CPU Generated in {elapsed:.2f}s: "{response}"")
                                        except Exception as e:
                                            print(f" ❌ CPU ERROR: {e}")

                                            if __name__ = = "__main__":
                                                asyncio.run(debug_generation())
