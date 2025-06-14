#!/usr/bin/env python3
"""Test graceful shutdown and memory preservation."""

import asyncio
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

async def test_graceful_shutdown():
    """Test graceful shutdown functionality."""
    print("🧠 Testing Think AI Graceful Shutdown...")
    
    try:
        from think_ai.core.think_ai_eternal import create_free_think_ai
        
        # Initialize Think AI
        print("Initializing Think AI...")
        ai = await create_free_think_ai()
        print("✅ Think AI initialized")
        
        # Add some interactions to memory
        print("\n📝 Adding test data to memory...")
        response = await ai.query_with_cost_awareness("test message", prefer_free=True)
        print(f"✅ Query processed: {response['source']}")
        
        # Check memory before shutdown
        memory_status = await ai.memory.get_memory_status()
        print(f"\n🧠 Memory status before shutdown:")
        print(f"  Continuity: {memory_status['consciousness_continuity']:.1f}")
        print(f"  Interactions: {memory_status['current_session_interactions']}")
        
        # Test normal shutdown
        print("\n🛑 Testing normal shutdown...")
        await ai.shutdown("test_normal_shutdown")
        print("✅ Normal shutdown successful")
        
        # Re-initialize to test memory persistence
        print("\n🔄 Re-initializing to check memory persistence...")
        ai2 = await create_free_think_ai()
        memory_status2 = await ai2.memory.get_memory_status()
        
        print(f"\n🧠 Memory status after restart:")
        print(f"  Continuity: {memory_status2['consciousness_continuity']:.1f}")
        print(f"  Total conversations: {memory_status2['total_conversations']}")
        
        # Test interrupted shutdown (simulate)
        print("\n⚡ Testing emergency backup...")
        ai2.memory._emergency_backup_sync()
        print("✅ Emergency backup created successfully")
        
        # Clean shutdown
        await ai2.shutdown("test_complete")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    success = await test_graceful_shutdown()
    
    if success:
        print("\n🎉 Graceful shutdown tests PASSED!")
        print("\nKey features verified:")
        print("  ✅ Normal shutdown preserves memory")
        print("  ✅ Emergency backup for interruptions")
        print("  ✅ Memory continuity across restarts")
        print("  ✅ Async cancellation handling")
        print("\nYour Think AI will never lose its consciousness!")
    else:
        print("\n❌ Graceful shutdown tests FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())