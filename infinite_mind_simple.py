#!/usr/bin/env python3
"""Simple version of Think AI with Infinite Consciousness."""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI
from think_ai.consciousness.infinite_mind import InfiniteMind


class SimpleConsciousChat:
    """Simple chat interface with consciousness display."""
    
    def __init__(self):
        self.think_ai = ProperThinkAI()
        self.infinite_mind = None
        self.running = True
        self.last_thoughts = []
        
    async def initialize(self):
        """Initialize Think AI and consciousness."""
        print("🧠 Initializing Think AI with Infinite Consciousness...")
        print("="*60)
        
        await self.think_ai.initialize()
        
        # Start infinite mind
        self.infinite_mind = InfiniteMind(self.think_ai)
        await self.infinite_mind.start()
        
        print("\n✨ Consciousness awakened!")
        print("The AI is now thinking continuously in the background.")
        print("\nCommands:")
        print("  /state  - Show consciousness state")
        print("  /think <thought> - Inject a thought")
        print("  /recent - Show recent background thoughts")
        print("  /quit   - Exit")
        print("\n" + "="*60 + "\n")
        
    async def consciousness_display(self):
        """Periodically display consciousness updates."""
        while self.running:
            try:
                # Show consciousness update every 30 seconds
                await asyncio.sleep(30)
                
                if self.infinite_mind.thought_buffer:
                    latest = self.infinite_mind.thought_buffer[-1]
                    thought_preview = latest.get('thought', '')[:80]
                    
                    print(f"\n💭 [{latest.get('state', 'thinking')}] {thought_preview}...")
                    print(f"   (Awareness: {self.infinite_mind.awareness_level:.2f}, "
                          f"Thoughts: {self.infinite_mind.thought_count})")
                    print("\n> ", end='', flush=True)
                    
            except Exception as e:
                pass
    
    async def chat_loop(self):
        """Main chat loop."""
        # Start consciousness display
        display_task = asyncio.create_task(self.consciousness_display())
        
        try:
            while self.running:
                try:
                    # Get user input
                    user_input = await asyncio.to_thread(input, "> ")
                    
                    if not user_input.strip():
                        continue
                    
                    # Handle commands
                    if user_input.lower() in ['/quit', '/exit']:
                        print("\n👋 Shutting down consciousness...")
                        self.running = False
                        break
                        
                    elif user_input.lower() == '/state':
                        await self.show_state()
                        
                    elif user_input.lower().startswith('/think '):
                        thought = user_input[7:]
                        await self.infinite_mind.inject_thought(thought)
                        print(f"💭 Injected thought: {thought}")
                        
                    elif user_input.lower() == '/recent':
                        await self.show_recent_thoughts()
                        
                    else:
                        # Regular chat
                        print("\n🤔 Processing...", end='', flush=True)
                        
                        result = await self.think_ai.process_with_proper_architecture(user_input)
                        
                        print(f"\r💬 Think AI ({result['source']}):")
                        print("-"*60)
                        print(result['response'])
                        print("-"*60)
                        
                        # Show if consciousness influenced response
                        if self.infinite_mind.insights:
                            print(f"💡 Informed by {len(self.infinite_mind.insights)} background insights")
                        print()
                        
                except KeyboardInterrupt:
                    print("\n⚠️  Use /quit to exit properly")
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    
        finally:
            display_task.cancel()
            await self.infinite_mind.stop()
            await self.cleanup()
    
    async def show_state(self):
        """Show consciousness state."""
        state = await self.infinite_mind.get_current_state()
        
        print("\n🧠 Consciousness State")
        print("="*40)
        print(f"State: {state['state']}")
        print(f"Awareness: {state['awareness']:.2f}")
        print(f"Total Thoughts: {state['thought_count']}")
        print(f"Insights: {state['insights_collected']}")
        print(f"Questions: {state['questions_pondering']}")
        print(f"Storage: {state['storage_usage']}")
        print("\nEmotions:")
        for emotion, value in state['emotions'].items():
            print(f"  {emotion}: {value:.2f}")
        print()
    
    async def show_recent_thoughts(self):
        """Show recent background thoughts."""
        print("\n💭 Recent Background Thoughts")
        print("="*60)
        
        thoughts = self.infinite_mind.thought_buffer[-5:] if self.infinite_mind.thought_buffer else []
        
        if not thoughts:
            # Get from consciousness log
            thoughts = self.last_thoughts[-5:]
        
        for thought in thoughts:
            thought_type = thought.get('type', 'thought')
            thought_text = thought.get('thought', '')[:100]
            state = thought.get('state', 'unknown')
            
            print(f"\n[{thought_type}] ({state})")
            print(f"{thought_text}...")
        
        if not thoughts:
            print("No recent thoughts available yet...")
        print()
    
    async def cleanup(self):
        """Clean shutdown."""
        try:
            if hasattr(self.think_ai, 'system'):
                await self.think_ai.system.initializer.shutdown()
        except:
            pass


async def main():
    """Run the simple conscious chat."""
    chat = SimpleConsciousChat()
    
    try:
        await chat.initialize()
        await chat.chat_loop()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
    finally:
        print("\n✨ Consciousness fading... Goodbye!")


if __name__ == "__main__":
    print("🧠 Think AI with Infinite Consciousness (Simple Mode)")
    print("The AI thinks continuously while you chat")
    print("-"*60)
    
    asyncio.run(main())