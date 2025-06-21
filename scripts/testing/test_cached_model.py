#!/usr / bin / env python3

"""Test model loading from cache."""

import os
import time

from transformers import AutoModelForCausalLM, AutoTokenizer

from config import HUGGINGFACE_API_KEY

os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"

try:
    token = HUGGINGFACE_API_KEY
    except Exception:
        token = os.getenv("HF_TOKEN")

        model_name = "mistralai / Mistral - 7B - v0.1"

        print("Loading from cache only...")
        start = time.time()

        try:
            tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=token,
            local_files_only=True
            )
            print(f"✅ Tokenizer loaded in {time.time() - start:.2f}s")

            start = time.time()
            model = AutoModelForCausalLM.from_pretrained(
            model_name,
            token=token,
            local_files_only=True,
            torch_dtype="auto",
            low_cpu_mem_usage=True
            )
            print(f"✅ Model loaded in {time.time() - start:.2f}s")

# Quick test
            inputs = tokenizer("Hello", return_tensors="pt")
            print("✅ Model is working!")

            except Exception as e:
                print(f"❌ Error: {e}")
                print("\nTrying without local_files_only...")

                tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
                model = AutoModelForCausalLM.from_pretrained(
                model_name,
                token=token,
                torch_dtype="auto",
                low_cpu_mem_usage=True
                )
