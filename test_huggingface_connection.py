#!/usr/bin/env python3
"""Test Hugging Face API connection"""

import os
import sys

from huggingface_hub import list_models, whoami
from transformers import AutoTokenizer


def test_connection():
    """Test HF API with O(1) verification"""
    token = os.getenv("HF_TOKEN")

    if not token:
        print("❌ No HF_TOKEN found in environment")
        return False

    print(f"✅ Token found: {token[:8]}...")

    try:
        # Test API access
        user_info = whoami(token=token)
        print(f"✅ Authenticated as: {user_info['name']}")

        # Test model listing (limit to 1 for speed)
        models = list(list_models(limit=1))
        print(f"✅ Can access models: {len(models)} found")

        # Test tokenizer download
        AutoTokenizer.from_pretrained("bert-base-uncased")
        print("✅ Successfully downloaded tokenizer")

        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing Hugging Face connection...")
    success = test_connection()
    sys.exit(0 if success else 1)
