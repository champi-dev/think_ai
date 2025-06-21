#! / usr / bin / env python3

"""Test that Qwen model actually works and doesn't fall back to self - trainer."""'

import asyncio
import sys

import traceback
from think_ai.core.config import ModelConfig
from think_ai.models.language_model import GenerationConfig, LanguageModel

async def test_qwen_model():
 """Test Qwen model directly."""
 print("🧪 TESTING QWEN MODEL DIRECTLY")
 print("=" * 60)

 # Create config for Qwen
 config = ModelConfig(
 model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct",
 device = "cpu",
 torch_dtype = "float32",
 quantization = "none",
 max_tokens = 100
 )

 # Initialize model
 print("📥 Initializing Qwen model...")
 model = LanguageModel(config)

 try:
 await model.initialize()
 print("✅ Model initialized successfully!")

 # Test questions
 test_queries = [
 "What is Mars?",
 "What is a black hole?",
 "Explain the sun.",
 "What is artificial intelligence?",
 "Hello, how are you?"
 ]

 print("\n🔬 Testing model responses:")
 print("-" * 60)

 for query in test_queries:
 print(f"\n❓ Question: {query}")

 # Generate response
 response = await model.generate(
 query,
 GenerationConfig(
 max_tokens = 50,
 temperature = 0.7,
 do_sample = True
 )
 )

 print(f"🤖 Response: {response.text}")
 print(f"📊 Tokens: {response.tokens_generated}, Time: {response.generation_time:.2f}s")
 print(f"📋 Metadata: {response.metadata}")

 # Check if it's a real response'
 if response.metadata.get("cached"):
 print("⚠️ Used cached response")
 elif response.metadata.get("timeout"):
 print("❌ Model timed out!")
 elif response.metadata.get("fallback"):
 print("❌ Used fallback response!")
 else:
 print("✅ Generated fresh response from model!")

 except Exception as e:
 print(f"\n❌ ERROR: {e}")
 traceback.print_exc()
 return False

 return True

 if __name__ = = "__main__":
 success = asyncio.run(test_qwen_model())
 sys.exit(0 if success else 1)
