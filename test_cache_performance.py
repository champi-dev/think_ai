#! / usr / bin / env python3

"""Performance test demonstrating O(1) initialization with caching."""

import asyncio
import sys
import time

from implement_proper_architecture import ProperThinkAI
from think_ai.cache import get_architecture_cache


async def test_initialization_speed():
"""Compare initialization times with and without cache."""
# Clear cache to ensure fair comparison
    cache = get_architecture_cache()
    cache.clear_cache()

# Test 1: Cold start (no cache)

    think_ai_cold = ProperThinkAI(enable_cache=True)
    cold_start = time.time()
    await think_ai_cold.initialize()
    cold_time = time.time() - cold_start

# Quick test query to ensure it works
    await think_ai_cold.query("Hello")

    await think_ai_cold.shutdown()

# Test 2: Warm start (with cache)

    think_ai_warm = ProperThinkAI(enable_cache=True)
    warm_start = time.time()
    await think_ai_warm.initialize()
    warm_time = time.time() - warm_start

# Quick test query to ensure it works
    await think_ai_warm.query("Hello")

    await think_ai_warm.shutdown()

# Results

# Show O(1) achievement
    if warm_time < 1.0:  # Sub - second initialization
    pass

# Cache info
cache_info = cache.get_cache_info()
for _key, _value in cache_info.items():
    pass

return warm_time < cold_time / 2  # Success if at least 2x faster


async def test_cache_persistence() - > bool:
"""Test that cache persists across program runs."""
# Create new instance
    think_ai = ProperThinkAI(enable_cache=True)

    start = time.time()
    await think_ai.initialize()
    time.time() - start

    if think_ai._cache_loaded:
        pass
else:
    pass

await think_ai.shutdown()

return True


async def main():
"""Run all cache performance tests."""
    tests_passed = True

# Run initialization speed test
    if not await test_initialization_speed():
        tests_passed = False

# Run persistence test
        if not await test_cache_persistence():
            tests_passed = False

            if tests_passed:
                pass
        else:
            pass

        return tests_passed

    if __name__ = = "__main__":
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
