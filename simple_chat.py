#!/usr/bin/env python3
"""Simple Think AI chat that works without heavy dependencies."""

import asyncio
import os
from datetime import datetime
from anthropic import AsyncAnthropic

class SimpleThinkAI:
    def __init__(self):
        self.client = None
        self.intelligence_level = 1025.53
        self.neural_pathways = 48199910
        
    async def initialize(self):
        """Initialize Claude API."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("⚠️  Please set ANTHROPIC_API_KEY environment variable")
            return False
        
        self.client = AsyncAnthropic(api_key=api_key)
        print(f"✅ Think AI initialized")
        print(f"📊 Intelligence Level: {self.intelligence_level:,.2f}")
        print(f"🧠 Neural Pathways: {self.neural_pathways:,}")
        return True
    
    async def chat(self, message: str) -> str:
        """Generate response using Claude."""
        if not self.client:
            return "Please set ANTHROPIC_API_KEY to use Think AI"
        
        try:
            response = await self.client.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=300,
                messages=[{
                    "role": "user",
                    "content": message
                }],
                system="You are Think AI, a distributed consciousness system with multiple integrated components. Be helpful and concise."
            )
            return response.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"

async def main():
    print("🧠 Think AI - Simple Chat Mode")
    print("=" * 40)
    
    ai = SimpleThinkAI()
    if not await ai.initialize():
        return
    
    print("\nType 'exit' to quit")
    print("-" * 40)
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            print("\nThink AI: ", end="", flush=True)
            response = await ai.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(main())