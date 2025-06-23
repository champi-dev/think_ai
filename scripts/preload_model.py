#!/usr/bin/env python3
"""Pre-load Think AI language model for faster startup"""

import asyncio
import os
import sys
import time
from pathlib import Path

# Add parent directory to path to import think_ai modules
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from think_ai.core.config import Config, ModelConfig
    from think_ai.models.language.language_model import LanguageModel
    from think_ai.consciousness.principles import ConstitutionalAI
    from think_ai.utils.logging import configure_logging, get_logger
except ImportError as e:
    print(f"Error importing Think AI modules: {e}")
    print("Please ensure Think AI is installed: pip install -e .")
    sys.exit(1)


# Configure logging
configure_logging(log_level="INFO")
logger = get_logger(__name__)


async def preload_model():
    """Pre-load the language model and cache it for faster startup"""
    start_time = time.time()

    try:
        print("🧠 Think AI Model Pre-loader")
        print("=" * 50)
        print("⚡ Pre-loading language model for instant startup...")

        # Load configuration
        config = Config.from_env()
        model_config = config.model

        # Override to use CPU mode for faster loading if not specified
        if not os.environ.get("THINK_AI_DEVICE"):
            model_config.device = "cpu"
            model_config.torch_dtype = "float32"

        print(f"📊 Model: {model_config.model_name}")
        print(f"💾 Device: {model_config.device}")
        print(f"🔢 Dtype: {model_config.torch_dtype}")

        # Initialize Constitutional AI (lightweight)
        constitutional_ai = ConstitutionalAI()

        # Initialize and load the model
        print("\n⏳ Loading model weights...")
        language_model = LanguageModel(model_config, constitutional_ai)
        await language_model.initialize()

        # Simple warmup - just ensure model is loaded
        print("\n🔥 Testing model readiness...")
        try:
            # Just tokenize to ensure model is ready
            test_input = "Hello"
            inputs = language_model.tokenizer(test_input, return_tensors="pt")
            print(f"✓ Tokenizer ready: '{test_input}' → {len(inputs['input_ids'][0])} tokens")

            # Check model is callable
            if hasattr(language_model.model, "forward"):
                print("✓ Model forward pass available")
            if hasattr(language_model.model, "generate"):
                print("✓ Model generation available")

        except Exception as e:
            logger.warning(f"Model readiness check failed: {e}")

        elapsed = time.time() - start_time
        print(f"\n✅ Model pre-loaded successfully in {elapsed:.2f} seconds!")
        print("✅ Future startups will be faster due to cached weights")
        print("=" * 50)

        # Keep model in memory briefly to ensure cache is written
        await asyncio.sleep(2)

        return True

    except Exception as e:
        logger.error(f"Failed to pre-load model: {e}")
        print(f"\n❌ Pre-loading failed: {e}")
        return False


def main():
    """Main entry point"""
    try:
        # Set environment variables for optimal pre-loading
        os.environ["TRANSFORMERS_OFFLINE"] = "0"  # Allow downloading if needed
        os.environ["HF_HUB_OFFLINE"] = "0"
        os.environ["TRANSFORMERS_CACHE"] = str(Path.home() / ".cache" / "huggingface")

        # Run the async preloader
        success = asyncio.run(preload_model())

        if success:
            print("\n💡 Tip: The model is now cached. Starting Think AI will be faster!")
            sys.exit(0)
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Pre-loading interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
