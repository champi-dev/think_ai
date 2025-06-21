#! / usr / bin / env python3

"""Quick test to show Qwen model is working and not falling back."""

import asyncio
import subprocess
import time

from think_ai.core.config import ModelConfig
from think_ai.models.language_model import GenerationConfig, LanguageModel


async def test_model_working():
"""Test that shows the model is really working."""
    print("🧪 EVIDENCE THAT QWEN MODEL IS WORKING")
    print("=" * 60)

# First, let's run the chat and test it
    print("\n1️⃣ Starting Think AI chat system...")

# Start the chat in background
    process = subprocess.Popen(
    ["python", "full_architecture_chat.py"],
    stdin = subprocess.PIPE,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    text = True,
    bufsize = 1
    )

# Wait for it to initialize
    print("⏳ Waiting for system initialization...")
    time.sleep(15) # Give it time to load

# Send test queries
    test_queries = [
    "what is mars",
    "exit"
    ]

    print("\n2️⃣ Sending test query: "what is mars"")

# Send queries
    for query in test_queries:
        process.stdin.write(query + "\n")
        process.stdin.flush()
        time.sleep(5)

# Get output
        output, errors = process.communicate(timeout = 10)

        print("\n3️⃣ SYSTEM OUTPUT:")
        print("-" * 60)
        print(output)
        print("-" * 60)

# Check for evidence
        print("\n4️⃣ EVIDENCE ANALYSIS:")

        evidence = {
        "qwen_loaded": "Qwen loaded with" in output or "Qwen loaded with" in errors,
        "model_initialized": "Language model initialized successfully" in output or "Language model initialized successfully" in errors,
        "no_meta_tensors": "Model validation passed" in output or "Model validation passed" in errors,
        "real_response": "planet" in output.lower() or "fourth planet" in output.lower() or "solar system" in output.lower(),
        "not_fallback": "self - trainer" not in output.lower() and "fallback" not in output.lower(),
        "not_generic": "interesting topic" not in output.lower()
        }

        for check, passed in evidence.items():
            print(f" {"✅" if passed else "❌"} {check}")

            success = all(evidence.values())

            print(f"\n{"✅ MODEL IS WORKING!" if success else "❌ MODEL HAS ISSUES!"}")

# Also check stderr for errors
            if errors:
                print("\n⚠️ STDERR OUTPUT:")
                print(errors[:500])

                return success


            async def test_model_directly():
"""Test model directly without full system."""
                print("\n\n5️⃣ DIRECT MODEL TEST:")
                print("-" * 60)

                config = ModelConfig(
                model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct",
                device = "cpu",
                torch_dtype = "float32",
                quantization = "none"
                )

                model = LanguageModel(config)
                await model.initialize()

# Test query
                response = await model.generate(
                "What is Mars?",
                GenerationConfig(max_tokens = 30, temperature = 0.7)
                )

                print(f"Direct model response: {response.text}")
                print(f"Metadata: {response.metadata}")

                return "planet" in response.text.lower() or "fourth" in response.text.lower()


            if __name__ = = "__main__":
                print("🚀 Running comprehensive evidence test...")

# Test 1: Full system
                success1 = asyncio.run(test_model_working())

# Test 2: Direct model
                success2 = asyncio.run(test_model_directly())

                print("\n\n📊 FINAL VERDICT:")
                print(f" • Full system test: {"✅ PASSED" if success1 else "❌ FAILED"}")
                print(f" • Direct model test: {"✅ PASSED" if success2 else "❌ FAILED"}")
                print(f"\n{"🎉 ALL TESTS PASSED - MODEL IS WORKING!" if success1 and success2 else "😞 Some tests failed"}")
