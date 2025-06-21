#! / usr / bin / env python3

"""Test script to verify meta tensor fix for Qwen model loading."""

from pathlib import Path
import asyncio
import sys

import traceback
from think_ai.core.config import ModelConfig
from think_ai.models.language_model import GenerationConfig, LanguageModel
from think_ai.utils.logging import get_logger
import torch

sys.path.insert(0, str(Path(__file__).parent))

logger = get_logger(__name__)


async def test_model_loading():
"""Test that Qwen model loads without meta tensors."""

    print("🧪 Testing Meta Tensor Fix for Qwen Model")
    print("=" * 60)

# Create config for Qwen model
    config = ModelConfig(
    model_name="Qwen/Qwen2.5-Coder-1.5B-Instruct",
    device="cpu",
    torch_dtype="float32",
    max_tokens=512
    )

    print("✅ Config created:")
    print(f" Device: {config.device}")
    print(f" Dtype: {config.torch_dtype}")
    print(f" Model: {config.model_name}")

# Initialize model
    print("\n⏳ Initializing Qwen model...")
    model = LanguageModel(config)

    try:
        await model.initialize()
        print("✅ Model initialized successfully")

# Check for meta tensors
        meta_count = 0
        total_params = 0
        materialized_params = 0

        print("\n🔍 Checking for meta tensors...")
        for name, param in model.model.named_parameters():
            total_params + = 1
            if param.is_meta:
                meta_count + = 1
                print(f"❌ Meta tensor found: {name}")
            else:
                materialized_params + = 1

                print("\n📊 Model Statistics:")
                print(f" Total parameters: {total_params}")
                print(f" Materialized parameters: {materialized_params}")
                print(f" Meta tensors: {meta_count}")

                if meta_count = = 0:
                    print("\n✅ SUCCESS: No meta tensors found! Model loaded correctly.")

# Test generation
                    print("\n🔤 Testing generation...")
                    gen_config = GenerationConfig(
                    temperature=0.7,
                    max_tokens=50,
                    do_sample=True
                    )
                    response = await model.generate("Hello, how are you?", gen_config)
                    print(f"✅ Generated response: {response.text}")
                    print(f" Generation time: {response.generation_time:.2f}s")
                    print(f" Tokens generated: {response.tokens_generated}")

# Check parameter cache
                    print("\n🗄️ Parameter cache stats:")
                    print(f" Cached params: {len(model._param_cache)}")
                    print(f" Cached layers: {len(model._layer_cache)}")
                    if model._param_cache:
                        print(" Model config from cache:")
                        for key, value in model._param_cache.items():
                            print(f" - {key}: {value}")

# Verify O(1) access
                            print("\n⚡ Testing O(1) parameter access:")
                            if "input_embeddings" in model._layer_cache:
                                embed = model._layer_cache["input_embeddings"]
                                print(f" ✅ Input embeddings cached: {embed.__class__.__name__}")
                                if "vocab_size" in model._param_cache:
                                    print(f" ✅ Vocab size (O(1) lookup): {model._param_cache["vocab_size"]}")

                                    print("\n🎉 All tests passed! Meta tensor issue is FIXED!")
                                    return True
                            else:
                                print(f"\n❌ FAILURE: Found {meta_count} meta tensors!")
                                print("\nDebugging info:")
                                print(f"- Config device: {config.device}")
                                print(f"- Config dtype: {config.torch_dtype}")
                                print(f"- PyTorch version: {torch.__version__}")
                                return False

                            except Exception as e:
                                print(f"\n❌ Test failed with error: {e}")
                                traceback.print_exc()
                                return False

                            if __name__ = = "__main__":
                                success = asyncio.run(test_model_loading())
                                sys.exit(0 if success else 1)
