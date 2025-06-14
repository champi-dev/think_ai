#!/usr/bin/env python3
"""Interactive chat with Think AI using proper architecture."""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


async def interactive_chat():
    """Run interactive chat session with proper architecture."""
    print("\n🚀 THINK AI - PROPER ARCHITECTURE CHAT")
    print("="*60)
    print("This uses the REAL distributed architecture!")
    print("- ScyllaDB for knowledge and caching")
    print("- Local language model for basic responses")
    print("- Claude only when truly needed")
    print("="*60)
    
    ai = ProperThinkAI()
    
    try:
        print("\n📦 Initializing distributed components...")
        await ai.initialize()
        
        print("\n✅ System ready! You can now chat.")
        print("\n📝 Commands:")
        print("  /cost     - Show current costs")
        print("  /stats    - Show system statistics")
        print("  /learn    - Teach Think AI a fact")
        print("  /recall   - Test knowledge recall")
        print("  /clear    - Clear response cache")
        print("  /help     - Show this help")
        print("  /quit     - Exit chat")
        print("\n💡 Try asking the same question twice to see caching!")
        print("-"*60)
        
        conversation_start = datetime.now()
        query_count = 0
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() == '/quit':
                    break
                    
                elif user_input.lower() == '/help':
                    print("\n📝 Commands:")
                    print("  /cost     - Show current costs")
                    print("  /stats    - Show system statistics")
                    print("  /learn    - Teach Think AI a fact")
                    print("  /recall   - Test knowledge recall")
                    print("  /clear    - Clear response cache")
                    print("  /quit     - Exit chat")
                    continue
                    
                elif user_input.lower() == '/cost':
                    costs = ai.claude.get_cost_summary()
                    print(f"\n💰 Cost Summary:")
                    print(f"  Total cost: ${costs['total_cost']:.4f}")
                    print(f"  Claude API calls: {costs['request_count']}")
                    print(f"  Budget remaining: ${costs['budget_remaining']:.2f}")
                    print(f"  Average per query: ${costs['average_cost_per_request']:.4f}")
                    continue
                    
                elif user_input.lower() == '/stats':
                    # Count various stored items
                    cache_count = 0
                    interaction_count = 0
                    
                    try:
                        async for key, _ in ai.services['scylla'].scan(prefix="cache_", limit=100):
                            cache_count += 1
                        async for key, _ in ai.services['scylla'].scan(prefix="interaction_", limit=100):
                            interaction_count += 1
                    except:
                        pass
                    
                    print(f"\n📊 System Statistics:")
                    print(f"  Session duration: {datetime.now() - conversation_start}")
                    print(f"  Queries processed: {query_count}")
                    print(f"  Knowledge entries: {len(ai.knowledge_base)}")
                    print(f"  Cached responses: {cache_count}")
                    print(f"  Stored interactions: {interaction_count}")
                    print(f"  Active services: {', '.join(ai.services.keys())}")
                    continue
                    
                elif user_input.lower().startswith('/learn'):
                    fact = user_input[6:].strip()
                    if not fact:
                        print("\n❓ Usage: /learn <fact>")
                        print("Example: /learn The Earth orbits the Sun")
                        continue
                    
                    # Store the fact
                    from think_ai.storage.base import StorageItem
                    import json
                    
                    key = f"knowledge_user_{datetime.now().timestamp()}"
                    content = {
                        "domain": "user_taught",
                        "fact": fact,
                        "confidence": 1.0,
                        "source": "user",
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    item = StorageItem.create(
                        content=json.dumps(content),
                        metadata={"type": "fact", "domain": "user_taught"}
                    )
                    
                    await ai.services['scylla'].put(key, item)
                    ai.knowledge_base[key] = fact
                    
                    print(f"\n✅ Learned: {fact}")
                    print("Try asking about it!")
                    continue
                    
                elif user_input.lower().startswith('/recall'):
                    topic = user_input[7:].strip()
                    if not topic:
                        print("\n❓ Usage: /recall <topic>")
                        print("Example: /recall consciousness")
                        continue
                    
                    # Search knowledge base
                    found = []
                    for key, fact in ai.knowledge_base.items():
                        if topic.lower() in fact.lower():
                            found.append(fact)
                    
                    if found:
                        print(f"\n🧠 Knowledge about '{topic}':")
                        for i, fact in enumerate(found[:5], 1):
                            print(f"  {i}. {fact}")
                    else:
                        print(f"\n❌ No knowledge found about '{topic}'")
                        print("Try /learn to teach me!")
                    continue
                    
                elif user_input.lower() == '/clear':
                    # Clear cache
                    cleared = 0
                    try:
                        async for key, _ in ai.services['scylla'].scan(prefix="cache_", limit=100):
                            await ai.services['scylla'].delete(key)
                            cleared += 1
                    except:
                        pass
                    
                    print(f"\n🧹 Cleared {cleared} cached responses")
                    continue
                
                # Regular query processing
                query_count += 1
                
                # Show processing indicator
                print("\n🤖 Think AI: ", end="", flush=True)
                
                # Track Claude usage
                claude_before = ai.claude.request_count
                
                # Process query
                result = await ai.process_with_proper_architecture(user_input)
                
                # Check if Claude was used
                claude_after = ai.claude.request_count
                claude_used = claude_after > claude_before
                
                # Display response
                print(result['response'])
                
                # Show architecture usage
                print(f"\n📊 [", end="")
                if result['architecture_usage']['cache'] == 'hit':
                    print("CACHE HIT! ", end="")
                if 'facts' in result['architecture_usage']['knowledge_base']:
                    kb_info = result['architecture_usage']['knowledge_base']
                    print(f"Knowledge: {kb_info} | ", end="")
                if claude_used:
                    print("Claude: Enhanced", end="")
                else:
                    print("Claude: Not needed", end="")
                print("]")
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Use /quit to exit properly")
                continue
            except Exception as e:
                print(f"\n❌ Error: {e}")
                logger.error(f"Chat error: {e}", exc_info=True)
                continue
        
        # Final summary
        print("\n\n" + "="*60)
        print("📊 SESSION SUMMARY")
        print("="*60)
        
        costs = ai.claude.get_cost_summary()
        print(f"\n🎯 Performance:")
        print(f"  Total queries: {query_count}")
        print(f"  Claude API calls: {costs['request_count']}")
        print(f"  Cache/distributed responses: {query_count - costs['request_count']}")
        if query_count > 0:
            print(f"  API reduction: {((query_count - costs['request_count']) / query_count * 100):.0f}%")
        
        print(f"\n💰 Cost Analysis:")
        print(f"  Total cost: ${costs['total_cost']:.4f}")
        if query_count > 0:
            print(f"  Average per query: ${costs['total_cost']/query_count:.4f}")
            print(f"  Traditional cost would be: ~${0.02 * query_count:.4f}")
            print(f"  You saved: ${(0.02 * query_count) - costs['total_cost']:.4f}!")
        
        print(f"\n⏱️  Session duration: {datetime.now() - conversation_start}")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔄 Shutting down...")
        try:
            await ai.shutdown()
        except Exception:
            pass  # Ignore shutdown errors
        print("👋 Goodbye!")


async def main():
    """Main entry point."""
    await interactive_chat()


if __name__ == "__main__":
    print("\n🚀 Starting Think AI with Proper Architecture...")
    print("This may take a moment to initialize all distributed components...")
    asyncio.run(main())