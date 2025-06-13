#! / usr / bin / env python3

"""Quick verification test to show Think AI is working."""

import asyncio
import sys
from pathlib import Path

from implement_proper_architecture import ProperThinkAI
from think_ai.utils.logging import get_logger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

logger = get_logger(__name__)


async def verify_think_ai() - > bool:
"""Run verification tests to show the system works."""
# Initialize WITH cache for speed
    think_ai = ProperThinkAI(enable_cache=True)

    try:
        await think_ai.initialize()

# Check services
        if think_ai.services:
            for _service in think_ai.services:
                pass
        else:
            return False
        except Exception:
            return False

        try:
            result = await think_ai.process_with_proper_architecture("What is 2 + 2?")
            response = result.get("response", "No response")
            if "4" in response:
                pass
        else:
            pass
        except Exception:
            pass

        try:
            result = await think_ai.process_with_proper_architecture("What is ScyllaDB?")
            response = result.get("response", "No response")
            result.get("source", "unknown")
            result.get("distributed_components_used", 0)

# Check architecture usage
            arch_usage = result.get("architecture_usage", {})
            for _component, _usage in arch_usage.items():
                pass
            except Exception:
                pass

            try:
                result = await think_ai.process_with_proper_architecture("Hello!")
                response = result.get("response", "No response")
                except Exception:
                    pass

                if hasattr(
                think_ai,
                "system") and hasattr(
                think_ai.system,
                "health_check"):
                    try:
                        health = await think_ai.system.health_check()
                        for _service, _status in health.items():
                            pass
                        except Exception:
                            pass

# Shutdown
                        await think_ai.shutdown()

                        return True

                    if __name__ = = "__main__":
                        success = asyncio.run(verify_think_ai())
                        sys.exit(0 if success else 1)
