#!/usr / bin / env python3

"""Quick verification that max_tokens fix is working."""

import asyncio

from think_ai.core.config import Config


async def verify_fix():
"""Verify the max_tokens fix is applied."""
    print("🔍 Verifying max_tokens fix...")
    print("=" * 50)

# Check config
    config = Config()
    print(f"✅ Config max_tokens: {config.model.max_tokens}")

# Check hardcoded value is gone
    with open("implement_proper_architecture.py", "r") as f:
        content = f.read()
        if "max_tokens = 512" in content:
            print("❌ WARNING: Still found hardcoded max_tokens = 512!")
        else:
            print("✅ No hardcoded max_tokens = 512 found")

            if "max_tokens = 200" in content:
                print("✅ Found corrected max_tokens = 200")

                print("\n🎯 The fix has been applied!")
                print("Restart with: ./launch_consciousness.sh")

                if __name__ == "__main__":
                    asyncio.run(verify_fix())
