import asyncio

from implement_proper_architecture import ProperArchitectureDemo

"""Quick test of the sun question in main architecture."""

import asyncio

from implement_proper_architecture import ProperArchitectureDemo


async def quick_test() -> None:
    demo = ProperArchitectureDemo()
    await demo.initialize_complete_architecture()

    await demo.process_with_proper_architecture("what is the sun??")

    if __name__ == "__main__":
        asyncio.run(quick_test())
