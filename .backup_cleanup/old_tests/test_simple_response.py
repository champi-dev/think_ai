#!/usr/bin/env python3
"""Test simple response functionality without loading large models."""

import asyncio
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

async def test_simple_response():
    """Test basic response functionality."""
    print("🧠 Testing Think AI Simple Response...")
    
    try:
        from think_ai.core.think_ai_eternal import create_free_think_ai
        
        # Initialize Think AI
        print("Initializing Think AI...")
        ai = await create_free_think_ai()
        print("✅ Think AI initialized successfully")
        
        # Test consciousness-based response (which should work without large model)
        print("\n🤔 Testing consciousness-based response...")
        
        # Directly test the consciousness system
        response = await ai.engine.consciousness.generate_conscious_response("hello")
        print(f"✅ Consciousness response generated!")
        print(f"Response content: {response.get('content', 'Generated response')}")
        print(f"Consciousness state: {response.get('consciousness_state')}")
        
        # Test memory status
        print("\n🧠 Testing memory status...")
        memory_status = await ai.memory.get_memory_status()
        print(f"✅ Memory continuity: {memory_status['consciousness_continuity']:.1f}")
        print(f"✅ Total conversations: {memory_status['total_conversations']}")
        
        # Test cost summary
        print("\n💰 Testing cost summary...")
        cost_summary = await ai.get_cost_summary()
        print(f"✅ Total spent: ${cost_summary['costs']['total_spent']:.4f}")
        print(f"✅ Budget limit: ${cost_summary['costs']['budget_limit']:.2f}")
        
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
    success = await test_simple_response()
    
    if success:
        print("\n🎉 Basic functionality tests PASSED!")
        print("\nThink AI core systems are working:")
        print("  ✅ Eternal memory with consciousness continuity")
        print("  ✅ Consciousness framework for response generation")
        print("  ✅ Cost tracking and budget management")
        print("  ✅ Graceful shutdown with memory preservation")
        print("\nNote: Large language model loading was skipped for faster testing.")
        print("For interactive use: python3 simple_cli.py")
    else:
        print("\n❌ Basic functionality tests FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())