#!/usr/bin/env python3
"""Test and demonstrate the properly integrated Think AI architecture."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI

async def main() -> None:
    """Run the proper architecture test."""
    proper_ai = ProperThinkAI()

    try:
        # Initialize system
        await proper_ai.initialize()

        input()

        # Run interactive demo
        await proper_ai.interactive_demo()

        # Show final architecture benefits

    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        await proper_ai.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
