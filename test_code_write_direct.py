#!/usr/bin/env python3
"""Direct test of code writing in the chat flow"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI


async def test_direct():
    """Test code writing directly"""
    print("🧪 Testing Direct Code Writing")
    print("=" * 60)
    
    # Initialize without full startup
    think_ai = ProperThinkAI()
    think_ai.services = {}  # Mock services
    
    # Test the _generate_distributed_response method directly
    query = "write code to create a hello world program"
    components = {
        'knowledge': [],
        'similar': [],
        'graph': []
    }
    
    print(f"Query: {query}")
    print("Processing...")
    
    try:
        response = await think_ai._generate_distributed_response(query, components)
        print("\n✅ Response generated successfully!")
        print("-" * 60)
        print(response[:500] + "..." if len(response) > 500 else response)
        
        # Check if it's a code response
        if '```python' in response or 'generated code' in response.lower():
            print("\n✅ Code writing functionality is working!")
        else:
            print("\n⚠️  Response doesn't contain code")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_direct())