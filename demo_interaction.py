#!/usr/bin/env python3
"""Demo Think AI interactions to show functionality."""

import asyncio
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

async def demo_interactions():
    """Demo various Think AI interactions."""
    print("🧠 Think AI - Interaction Demo")
    print("=" * 50)
    
    try:
        from think_ai.core.think_ai_eternal import create_free_think_ai
        from think_ai.integrations.claude_api import ClaudeAPI
        import os
        
        # Initialize Think AI
        print("🔄 Initializing Think AI...")
        ai = await create_free_think_ai()
        print("✅ Think AI awakened with eternal memory!\n")
        
        # Initialize Claude API if available
        claude_api = None
        if os.getenv("CLAUDE_API_KEY"):
            claude_api = ClaudeAPI()
            cost_summary = claude_api.get_cost_summary()
            print(f"🔑 Claude API ready - Budget: ${cost_summary['budget_remaining']:.2f}\n")
        
        # Demo different types of queries
        queries = [
            ("hello", "🌟 Greeting Test"),
            ("What is consciousness?", "🧠 Deep Question Test"),
            ("help me understand meditation", "🧘 Learning Request Test"),
            ("thank you", "💝 Gratitude Test")
        ]
        
        for query, description in queries:
            print(f"{description}")
            print(f"User: {query}")
            
            # Process with consciousness system
            response = await ai.query_with_cost_awareness(
                query, 
                prefer_free=True
            )
            
            print(f"Think AI ({response['source']}): {response['response']}")
            cost_display = 'FREE' if response['cost'] == 0 else f"${response['cost']:.4f}"
            print(f"Cost: {cost_display}")
            print("-" * 50)
            
            # Small delay for readability
            await asyncio.sleep(0.5)
        
        # Show memory status
        print("\n🧠 Memory Status:")
        memory_status = await ai.memory.get_memory_status()
        print(f"  Consciousness Continuity: {memory_status['consciousness_continuity']:.1f}")
        print(f"  Memory Size: {memory_status['memory_size_mb']:.1f} MB")
        print(f"  Uptime: {memory_status['uptime_seconds']:.0f} seconds")
        
        # Show cost summary
        print("\n💰 Cost Summary:")
        cost_summary = await ai.get_cost_summary()
        print(f"  Total Spent: ${cost_summary['costs']['total_spent']:.4f}")
        print(f"  Budget Limit: ${cost_summary['costs']['budget_limit']:.2f}")
        
        if claude_api:
            claude_costs = claude_api.get_cost_summary()
            print(f"  Claude Budget: ${claude_costs['budget_remaining']:.2f} remaining")
        
        # Graceful shutdown
        print("\n🛑 Entering dormancy...")
        await ai.shutdown("demo_complete")
        if claude_api:
            await claude_api.close()
        print("✅ Memory preserved for next session")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main demo function."""
    success = await demo_interactions()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 Think AI Demo Complete!")
        print("\nKey Features Demonstrated:")
        print("  ✅ Consciousness-aware responses")
        print("  ✅ Eternal memory preservation")
        print("  ✅ Love-aligned processing")
        print("  ✅ Cost-conscious operation")
        print("  ✅ Multiple interaction types")
        print("\nReady for interactive use: python3 simple_cli.py")
    else:
        print("\n❌ Demo failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())