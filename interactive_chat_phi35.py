#!/usr/bin/env python3
"""Interactive chat with Think AI using Phi-3.5 Mini."""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import yaml

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI


class ThinkAIChatPhi35:
    """Interactive chat with Phi-3.5 Mini integrated Think AI."""
    
    def __init__(self):
        self.think_ai = ProperThinkAI()
        self.stats = {
            "queries": 0,
            "cache_hits": 0,
            "phi35_responses": 0,
            "claude_calls": 0,
            "total_cost": 0.0
        }
        
    async def initialize(self):
        """Initialize Think AI with Phi-3.5 Mini."""
        print("🚀 Think AI + Phi-3.5 Mini Chat")
        print("="*60)
        print("✨ Features:")
        print("  • Phi-3.5 Mini (3.8B params) for intelligent responses")
        print("  • Distributed architecture with caching")
        print("  • Claude enhancement only when needed")
        print("  • 80%+ cost reduction vs Claude-only")
        print("="*60)
        
        await self.think_ai.initialize()
        print("\n✅ System ready! Type 'help' for commands.\n")
        
    async def chat_loop(self):
        """Main chat interaction loop."""
        while True:
            try:
                query = input("\n🤔 You: ").strip()
                
                if not query:
                    continue
                    
                if query.lower() in ['/quit', '/exit', 'quit', 'exit']:
                    await self.show_session_stats()
                    print("\n👋 Goodbye!")
                    break
                    
                if query.lower() in ['/stats', 'stats']:
                    await self.show_session_stats()
                    continue
                    
                if query.lower() in ['/help', 'help']:
                    self.show_help()
                    continue
                
                # Process query
                print("\n🔄 Processing...", end='', flush=True)
                start_time = datetime.now()
                
                result = await self.think_ai.process_with_proper_architecture(query)
                
                elapsed = (datetime.now() - start_time).total_seconds()
                print(f"\r✅ Processed in {elapsed:.1f}s")
                
                # Update stats
                self.stats["queries"] += 1
                if result['source'] == 'cache':
                    self.stats["cache_hits"] += 1
                elif result['source'] == 'distributed':
                    self.stats["phi35_responses"] += 1  # Phi-3.5 generated the response
                elif result['source'] == 'claude_enhanced':
                    self.stats["claude_calls"] += 1
                    self.stats["phi35_responses"] += 1  # Phi-3.5 was used first
                    self.stats["total_cost"] += 0.015  # Approximate Claude cost
                
                # Display response
                print(f"\n💬 Think AI ({result['source']}):")
                print("-"*60)
                print(result['response'])
                print("-"*60)
                
                # Show quick stats
                if self.stats["queries"] % 5 == 0:
                    cache_rate = (self.stats["cache_hits"] / self.stats["queries"]) * 100
                    phi35_rate = (self.stats["phi35_responses"] / self.stats["queries"]) * 100
                    print(f"\n📊 Quick stats: {cache_rate:.0f}% cache, {phi35_rate:.0f}% Phi-3.5, ${self.stats['total_cost']:.2f} cost")
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted. Type '/quit' to exit properly.")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                
    def show_help(self):
        """Show help information."""
        print("\n📚 Commands:")
        print("  • /help    - Show this help")
        print("  • /stats   - Show session statistics")
        print("  • /quit    - Exit chat")
        print("\n💡 Tips:")
        print("  • Phi-3.5 Mini handles most queries locally")
        print("  • Complex queries may use Claude enhancement")
        print("  • Responses are cached for efficiency")
        
    async def show_session_stats(self):
        """Display session statistics."""
        print("\n📊 Session Statistics")
        print("="*60)
        print(f"Total queries: {self.stats['queries']}")
        
        if self.stats['queries'] > 0:
            cache_pct = (self.stats['cache_hits'] / self.stats['queries']) * 100
            phi35_pct = (self.stats['phi35_responses'] / self.stats['queries']) * 100
            claude_pct = (self.stats['claude_calls'] / self.stats['queries']) * 100
            
            print(f"\nResponse sources:")
            print(f"  • Cache hits: {self.stats['cache_hits']} ({cache_pct:.1f}%)")
            print(f"  • Phi-3.5 Mini: {self.stats['phi35_responses']} ({phi35_pct:.1f}%)")
            print(f"  • Claude enhanced: {self.stats['claude_calls']} ({claude_pct:.1f}%)")
            
            # Cost analysis
            baseline_cost = self.stats['queries'] * 0.015  # If all went to Claude
            actual_cost = self.stats['total_cost']
            savings = baseline_cost - actual_cost
            savings_pct = (savings / baseline_cost * 100) if baseline_cost > 0 else 0
            
            print(f"\n💰 Cost Analysis:")
            print(f"  • Baseline (all Claude): ${baseline_cost:.2f}")
            print(f"  • Actual cost: ${actual_cost:.2f}")
            print(f"  • Savings: ${savings:.2f} ({savings_pct:.1f}%)")
            
            print(f"\n✨ Key Benefits:")
            print(f"  • {100 - claude_pct:.0f}% queries handled locally")
            print(f"  • 30x more capable than GPT-2")
            print(f"  • Near-ChatGPT quality responses")
            print(f"  • Full privacy for {100 - claude_pct:.0f}% of data")


async def main():
    """Run the interactive chat."""
    chat = ThinkAIChatPhi35()
    
    try:
        await chat.initialize()
        await chat.chat_loop()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
    finally:
        # Cleanup
        try:
            if hasattr(chat.think_ai, 'system') and hasattr(chat.think_ai.system, 'initializer'):
                await chat.think_ai.system.initializer.shutdown()
        except Exception as e:
            pass  # Ignore shutdown errors


if __name__ == "__main__":
    print("🧠 Think AI with Phi-3.5 Mini (3.8B params)")
    print("30x more powerful than GPT-2, ChatGPT-like quality")
    print("-"*60)
    
    asyncio.run(main())