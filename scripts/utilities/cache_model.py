"""Cache the Qwen2.5 - Coder model for faster startup."""

from pathlib import Path

from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
import torch

cache_dir = Path.home() / ".cache" / "think_ai_models"
cache_dir.mkdir(parents=True, exist_ok=True)

model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

# Download and cache tokenizer
tokenizer = AutoTokenizer.from_pretrained(
model_name,
cache_dir=cache_dir,
local_files_only=False,
)

# Download and cache model
model = AutoModelForCausalLM.from_pretrained(
model_name,
cache_dir=cache_dir,
torch_dtype=torch.float16,
low_cpu_mem_usage=True,
local_files_only=False,
)
