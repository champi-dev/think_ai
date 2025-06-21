#!/usr / bin / env python3

"""Simple MPS test."""

import os

import time
import torch

os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"

print("MPS Backend Check:")
print(f"MPS Available: {torch.backends.mps.is_available()}")
print(f"MPS Built: {torch.backends.mps.is_built()}")

if torch.backends.mps.is_available():
# Simple computation test
    print("\nTesting MPS computation:")
    x = torch.randn(1000, 1000).to("mps")
    y = torch.randn(1000, 1000).to("mps")

    start = time.time()
    z = torch.matmul(x, y)
    torch.mps.synchronize()  # Wait for computation
    print(f"Matrix multiplication time: {time.time() - start:.4f}s")

# Test a simple model
    print("\nTesting simple model on MPS:")
    model = torch.nn.Linear(10, 10).to("mps")
    input_tensor = torch.randn(1, 10).to("mps")

    start = time.time()
    output = model(input_tensor)
    torch.mps.synchronize()
    print(f"Model forward pass time: {time.time() - start:.4f}s")
else:
    print("MPS not available!")
