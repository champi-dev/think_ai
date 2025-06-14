#!/usr/bin/env python3
"""Test complex code writing"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI


async def test_complex():
    """Test more complex code writing"""
    print("🧪 Testing Complex Code Writing")
    print("=" * 60)
    
    # Initialize without full startup
    think_ai = ProperThinkAI()
    think_ai.services = {}  # Mock services
    
    # Test queries
    queries = [
        "write code to create a fibonacci function",
        "create a file called calculator.py with basic math functions",
        "write code that creates a simple web scraper"
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        print("-" * 50)
        
        try:
            components = {'knowledge': [], 'similar': [], 'graph': []}
            response = await think_ai._generate_distributed_response(query, components)
            
            print("\n✅ Response generated!")
            # Show just the first part
            if '```python' in response:
                start = response.find('```python')
                end = response.find('```', start + 10)
                if end > start:
                    code_block = response[start:end+3]
                    print(code_block)
            else:
                print(response[:300] + "...")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ Complex code writing test complete!")


if __name__ == "__main__":
    asyncio.run(test_complex())