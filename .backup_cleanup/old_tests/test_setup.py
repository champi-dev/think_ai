#!/usr/bin/env python3
"""Test Think AI setup without requiring rich terminal."""

import os
import sys
import asyncio
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

async def test_setup():
    """Test Think AI setup components."""
    print("🧠 Testing Think AI Setup...")
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from think_ai.core.think_ai_eternal import create_free_think_ai
        from think_ai.integrations.claude_api import ClaudeAPI
        from think_ai.consciousness import ConsciousnessState
        print("✅ All imports successful")
        
        # Test Claude API
        print("🔑 Testing Claude API...")
        if os.getenv("CLAUDE_API_KEY"):
            claude = ClaudeAPI()
            cost_summary = claude.get_cost_summary()
            print(f"✅ Claude API ready - Budget: ${cost_summary['budget_remaining']:.2f}")
            await claude.close()
        else:
            print("⚠️  No Claude API key found")
        
        # Test consciousness states
        print("🧠 Testing consciousness system...")
        states = [state.value for state in ConsciousnessState]
        print(f"✅ Consciousness states: {', '.join(states)}")
        
        # Test memory initialization (brief test)
        print("💾 Testing eternal memory...")
        ai = await create_free_think_ai()
        print("✅ Think AI eternal memory initialized")
        await ai.shutdown("test_complete")
        print("✅ Graceful shutdown successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    success = await test_setup()
    
    if success:
        print("\n🎉 Think AI setup test PASSED!")
        print("\nTo run the full CLI:")
        print("  python3 run_think_ai.py")
        print("\nOr from a proper terminal that supports rich formatting")
    else:
        print("\n❌ Setup test FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())