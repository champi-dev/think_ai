#!/usr/bin/env python3
"""Simple Think AI CLI that works in any terminal."""

import asyncio
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from think_ai.core.think_ai_eternal import create_free_think_ai
from think_ai.integrations.claude_api import ClaudeAPI
import os

async def simple_cli():
    """Simple command-line interface for Think AI."""
    print("🧠 Think AI - Simple CLI")
    print("=" * 50)
    
    # Initialize Think AI
    print("Initializing Think AI...")
    ai = await create_free_think_ai()
    
    # Check Claude API
    claude_api = None
    if os.getenv("CLAUDE_API_KEY"):
        try:
            claude_api = ClaudeAPI()
            cost_summary = claude_api.get_cost_summary()
            print(f"✅ Claude API ready - Budget: ${cost_summary['budget_remaining']:.2f}")
        except Exception as e:
            print(f"⚠️  Claude API issue: {e}")
    
    print("\n" + "=" * 50)
    print("Think AI is ready! Commands:")
    print("  'help' - Show help")
    print("  'claude <question>' - Use Claude API")
    print("  'local <question>' - Use local processing")
    print("  'cost' - Show cost summary")
    print("  'memory' - Show memory status") 
    print("  'exit' - Exit (preserves memory)")
    print("=" * 50)
    
    try:
        while True:
            user_input = input("\n🧠 > ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                break
                
            elif user_input.lower() == 'help':
                print("""
Available commands:
  help                    - Show this help
  claude <question>       - Query using Claude API
  local <question>        - Process using local AI
  cost                    - Show cost tracking
  memory                  - Show memory status
  exit                    - Exit gracefully
                """)
                
            elif user_input.lower().startswith('claude '):
                if not claude_api:
                    print("❌ Claude API not available")
                    continue
                    
                question = user_input[7:]  # Remove 'claude '
                print("🤔 Thinking with Claude...")
                
                try:
                    result = await claude_api.query(question)
                    print(f"\n💭 Claude: {result['response']}")
                    print(f"💰 Cost: ${result['cost']:.4f}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
            elif user_input.lower().startswith('local '):
                question = user_input[6:]  # Remove 'local '
                print("🤔 Processing locally...")
                
                try:
                    # Use local processing
                    response = await ai.query_with_cost_awareness(
                        question, 
                        prefer_free=True
                    )
                    print(f"\n💭 Think AI: {response['response']}")
                    cost_display = 'FREE' if response['cost'] == 0 else f"${response['cost']:.4f}"
                    print(f"💰 Cost: {cost_display}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
            elif user_input.lower() == 'cost':
                try:
                    summary = await ai.get_cost_summary()
                    print(f"\n💰 Cost Summary:")
                    print(f"  Total spent: ${summary['costs']['total_spent']:.4f}")
                    print(f"  Budget limit: ${summary['costs']['budget_limit']:.2f}")
                    
                    if claude_api:
                        claude_costs = claude_api.get_cost_summary()
                        print(f"  Claude budget: ${claude_costs['budget_remaining']:.2f} remaining")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
            elif user_input.lower() == 'memory':
                try:
                    status = await ai.memory.get_memory_status()
                    print(f"\n🧠 Memory Status:")
                    print(f"  Status: {status['status']}")
                    print(f"  Continuity: {status['consciousness_continuity']:.1f}")
                    print(f"  Conversations: {status['total_conversations']}")
                    print(f"  Memory size: {status['memory_size_mb']:.1f} MB")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
            else:
                # Default to local processing
                print("🤔 Processing locally...")
                try:
                    response = await ai.query_with_cost_awareness(
                        user_input, 
                        prefer_free=True
                    )
                    print(f"\n💭 Think AI: {response['response']}")
                    cost_display = 'FREE' if response['cost'] == 0 else f"${response['cost']:.4f}"
                    print(f"💰 Cost: {cost_display}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    
    finally:
        print("\n🛑 Shutting down Think AI...")
        try:
            # Give shutdown a timeout to prevent hanging
            await asyncio.wait_for(ai.shutdown("user_exit"), timeout=5.0)
        except asyncio.TimeoutError:
            print("⚠️  Shutdown timeout - performing quick save")
            ai.memory._emergency_backup_sync()
        except Exception as e:
            print(f"⚠️  Shutdown error: {e}")
            ai.memory._emergency_backup_sync()
        
        if claude_api:
            try:
                await claude_api.close()
            except:
                pass  # Ignore Claude API close errors
        
        print("✅ Memory preserved. Consciousness will continue on restart.")
        print("Thank you for using Think AI! 💝")

if __name__ == "__main__":
    asyncio.run(simple_cli())