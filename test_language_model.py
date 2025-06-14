#!/usr/bin/env python3
"""Test the language model fixes."""

import asyncio
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

async def test_language_model():
    """Test the language model functionality."""
    print("🧠 Testing Think AI Language Model...")
    
    try:
        from think_ai.core.think_ai_eternal import create_free_think_ai
        
        # Initialize Think AI
        print("Initializing Think AI...")
        ai = await create_free_think_ai()
        print("✅ Think AI initialized successfully")
        
        # Test basic query processing
        print("\n🤔 Testing local query processing...")
        
        # Test with a simple query
        response = await ai.query_with_cost_awareness(
            "hello", 
            prefer_free=True
        )
        
        print(f"✅ Query processed successfully!")
        print(f"Response: {response['response']}")
        print(f"Source: {response['source']}")
        cost_display = 'FREE' if response['cost'] == 0 else f"${response['cost']:.4f}"
        print(f"Cost: {cost_display}")
        
        # Test memory status
        print("\n🧠 Testing memory status...")
        memory_status = await ai.memory.get_memory_status()
        print(f"✅ Memory continuity: {memory_status['consciousness_continuity']:.1f}")
        
        # Test cost summary
        print("\n💰 Testing cost summary...")
        cost_summary = await ai.get_cost_summary()
        print(f"✅ Total spent: ${cost_summary['costs']['total_spent']:.4f}")
        
        # Clean shutdown
        print("\n🛑 Testing graceful shutdown...")
        await ai.shutdown("test_complete")
        print("✅ Shutdown successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    success = await test_language_model()
    
    if success:
        print("\n🎉 All language model tests PASSED!")
        print("\nThink AI is ready for interactive use:")
        print("  python3 simple_cli.py")
    else:
        print("\n❌ Language model tests FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())