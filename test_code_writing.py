#!/usr/bin/env python3
"""Test the code writing capability of Think AI"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI


async def test_code_writing():
    """Test that Think AI can write code to files."""
    
    print("🧪 Testing Think AI Code Writing Capability")
    print("=" * 60)
    
    # Initialize Think AI
    think_ai = ProperThinkAI()
    await think_ai.initialize()
    
    # Test queries
    test_queries = [
        "Write code to create a hello world program",
        "Create a file called calculator.py with a simple calculator",
        "Write code that prints the fibonacci sequence"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 50)
        
        try:
            result = await think_ai.process_with_proper_architecture(query)
            response = result.get('response', '')
            
            print(f"✅ Response preview: {response[:200]}...")
            
            # Check if file was mentioned
            if 'saved to' in response or 'created' in response:
                print("✓ File creation detected in response!")
            else:
                print("⚠️  No file creation mentioned")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Cleanup
    await think_ai.shutdown()
    
    print("\n" + "=" * 60)
    print("✅ Code writing test complete!")
    print("Check the 'generated_code' directory for created files.")


if __name__ == "__main__":
    asyncio.run(test_code_writing())