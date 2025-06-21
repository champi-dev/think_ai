"""Test simplest possible Qwen generation to find the bottleneck."""
import time

from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
import torch


def test_simple_generation() -> None:
"""Test generation with minimal setup."""
    model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

# Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name,
    trust_remote_code=True)

# Load model with different configurations
    configs = [
    {"dtype": torch.float16,
    "device": "cpu",
    "name": "CPU float16"},
    {"dtype": torch.float32,
    "device": "cpu",
    "name": "CPU float32"},
    ]

    for config in configs:

# Load model
        start = time.time()
        model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=config["dtype"],
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        )
        model.eval()
        time.time() - start

# Test generation with very short output
        test_prompts = [
        ("Hello", 5),
        ("What is 2 + 2?", 10),
        ("The sun is", 20),
        ]

        for prompt,
        max_tokens in test_prompts:

# Tokenize
            inputs = tokenizer(prompt,
            return_tensors="pt")

# Generate with minimal settings
        start = time.time()
        with torch.no_grad():
            outputs = model.generate(
            inputs["input_ids"],
            max_new_tokens=max_tokens,

            do_sample=False,
# Greedy for speed
            use_cache=True,
            pad_token_id=tokenizer.eos_token_id,

            )

            time.time() - start

# Decode
            tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True)

# Cleanup
            del model
            torch.cuda.empty_cache()

# Give user option to continue
            if config != configs[-1]:
                input(
                "\nPress Enter to test next configuration...")

                if __name__ == "__main__":
                    test_simple_generation(
                    )
