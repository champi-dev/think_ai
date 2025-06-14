#!/usr/bin/env python3
"""Simple test of Think AI chat."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI


async def test_chat():
    """Test Think AI responses."""
    ai = ProperThinkAI()
    await ai.initialize()
    
    print("\n" + "="*60)
    print("Testing Think AI responses with Ollama enabled")
    print("="*60 + "\n")
    
    queries = [
        "What is passion?",
        "Are you ok?",
        "Hello"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 40)
        
        try:
            result = await ai.process_with_proper_architecture(query)
            print(f"Response: {result.get('response', 'No response')}")
            print(f"Source: {result.get('source', 'unknown')}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Cleanup
    await ai.system.shutdown()


if __name__ == "__main__":
    asyncio.run(test_chat())