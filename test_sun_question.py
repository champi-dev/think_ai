#! / usr / bin / env python3

"""Specific test for 'What is the sun?' question."""

from pathlib import Path
import asyncio
import sys

import time
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

sys.path.insert(0, str(Path(__file__).parent))


async def test_sun_question():
"""Test the specific sun question with minimal overhead."""
    print("☀️ Testing "What is the sun?" with Qwen2.5 - Coder - 1.5B - Instruct")
    print("=" * 60)

    model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

# Load model with optimizations
    print("\n⏳ Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(
    model_name, trust_remote_code=True)

# Use best config for M1
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.float16 if device = = "mps" else torch.float32

    model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=dtype,
    low_cpu_mem_usage=True,
    trust_remote_code=True,
    use_cache=True  # Enable KV cache
    )

    if device = = "mps":
        model = model.to("mps")

        model.eval()
        print(f"✅ Model loaded on {device} with {dtype}")

# Test the exact question
        questions = [
        "What is the sun?",
        "what is the sun??",  # User"s exact format"
        "The sun is",  # Completion style
        ]

        for question in questions:
            print(f"\n\n{" = "*40}")
            print(f"❓ Question: {question}")
            print(f"{" = "*40}")

# Try different prompt formats
            prompts = [
            question,  # Direct
            f"Q: {question}\nA:",  # Q&A format
            f"User: {question}\nAssistant:",  # Chat format
            f"{question}\nAnswer:",  # Simple format
            ]

            for i, prompt in enumerate(prompts):
                print(f"\n📝 Prompt format {i + 1}: {repr(prompt)}")

# Tokenize
                inputs = tokenizer(prompt, return_tensors="pt")
                if device = = "mps":
                    inputs = {k: v.to("mps") for k, v in inputs.items()}

# Generate
                    start = time.time()

                    with torch.no_grad():
                        outputs = model.generate(
                        inputs["input_ids"],
                        max_new_tokens=100,
                        temperature=0.1,  # Very low for consistent output
                        do_sample=False,  # Deterministic
                        use_cache=True,
                        num_beams=1,
                        pad_token_id=tokenizer.eos_token_id,
                        early_stopping=True
                        )

                        gen_time = time.time() - start

# Decode full output and just the generated part
                        tokenizer.decode(outputs[0], skip_special_tokens=True)
                        generated_only = tokenizer.decode(
                        outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

                        print(f"⏱️ Time: {gen_time:.2f}s")
                        print(f"📄 Generated: {generated_only}")

# Check if it's a direct answer about the sun'
                        sun_keywords = [
                        "star",
                        "solar",
                        "plasma",
                        "fusion",
                        "center",
                        "heat",
                        "light"]
                        has_good_answer = any(word in generated_only.lower()
                        for word in sun_keywords)
                        print(f"✅ Direct answer: {"Yes" if has_good_answer else "No"}")

                        if has_good_answer:
                            print("\n🎯 GOOD ANSWER FOUND!")
                            print(f"Format that worked: {repr(prompt)}")
                            break

                        if __name__ = = "__main__":
                            asyncio.run(test_sun_question())
