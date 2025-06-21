#!/usr / bin / env python3

"""Simplest possible Mistral test."""

import os

from config import HUGGINGFACE_API_KEY
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"

# Import HF token
try:
    token = HUGGINGFACE_API_KEY
except Exception:
    token = os.getenv("HF_TOKEN")

print("Loading Mistral - 7B...")
model_name = "mistralai / Mistral - 7B - v0.1"

# Load from cache
cache_dir = os.path.expanduser("~/.cache / think_ai_models")
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, token=token)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=cache_dir,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
    token=token,
)

# Move to MPS
if torch.backends.mps.is_available():
    print("Moving to MPS...")
    model = model.to("mps")

print("Generating...")
inputs = tokenizer("Hello, I am", return_tensors="pt")
if torch.backends.mps.is_available():
    inputs = {k: v.to("mps") for k, v in inputs.items()}

# Generate with minimal tokens
outputs = model.generate(
    inputs.input_ids, max_new_tokens=5, temperature=0.7, do_sample=True  # Just 5 tokens
)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"Response: {response}")
