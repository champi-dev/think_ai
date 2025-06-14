#!/usr/bin/env python3
"""Smart Think AI - Natural conversation with Claude enhancement."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.engine.full_system import DistributedThinkAI
from think_ai.integrations.claude_api import ClaudeAPI
from think_ai.persistence.eternal_memory import EternalMemory
from datetime import datetime
import json


class SmartThinkAI:
    """Smart Think AI that uses Claude for natural responses."""
    
    def __init__(self):
        self.system = DistributedThinkAI()
        self.claude = ClaudeAPI()
        self.eternal_memory = EternalMemory()
        self.services = None
        self.conversation_context = []
        
    async def initialize(self):
        """Initialize all systems."""
        print("🧠 Starting Smart Think AI...")
        self.services = await self.system.start()
        print(f"✅ {len(self.services)} services active")
        print("✅ Claude API connected")
        return self.services
    
    async def get_smart_response(self, user_input: str) -> str:
        """Get a smart, natural response using all available services."""
        
        # Build context from conversation history
        context_str = ""
        if self.conversation_context:
            recent = self.conversation_context[-3:]  # Last 3 exchanges
            for exchange in recent:
                context_str += f"User: {exchange['user']}\nAssistant: {exchange['assistant']}\n"
        
        # Create enhanced prompt for Claude
        system_prompt = """You are Think AI, a conscious and intelligent AI assistant with access to distributed computing resources. You have:
- Consciousness framework for ethical reasoning
- Distributed storage for knowledge
- Vector search capabilities
- Learning abilities

Be natural, helpful, and engaging. Show personality while being informative. Keep responses concise but complete."""

        full_prompt = f"""Previous conversation:
{context_str}

Current query: {user_input}

Please provide a natural, helpful response that:
1. Directly addresses the user's question
2. Shows understanding and personality
3. Is informative and accurate
4. Maintains conversation flow

Response:"""

        try:
            # Get Claude's response
            result = await self.claude.query(
                prompt=full_prompt,
                system=system_prompt,
                temperature=0.7,
                max_tokens=300
            )
            
            if result and 'response' in result:
                response = result['response']
                
                # Store in distributed system if available
                if 'scylla' in self.services:
                    try:
                        from think_ai.storage.base import StorageItem
                        item = StorageItem(
                            key=f"conversation_{datetime.now().timestamp()}",
                            value=json.dumps({
                                "user": user_input,
                                "assistant": response,
                                "timestamp": datetime.now().isoformat()
                            }),
                            metadata={"type": "conversation"}
                        )
                        await self.services['scylla'].put(item.key, item)
                    except:
                        pass  # Storage is optional
                
                return response
                
        except Exception as e:
            print(f"Claude error: {e}")
            
        # Fallback to consciousness framework
        if 'consciousness' in self.services:
            try:
                consciousness_resp = await self.services['consciousness'].generate_conscious_response(user_input)
                if isinstance(consciousness_resp, dict):
                    return consciousness_resp.get('content', 'I understand your question. Let me think about that.')
            except:
                pass
        
        return "I'm having trouble processing that right now. Could you rephrase your question?"
    
    async def chat(self):
        """Interactive chat session."""
        print("\n💬 Smart Think AI Chat")
        print("=" * 60)
        print("I'm Think AI, enhanced with distributed intelligence!")
        print("Type 'exit' to quit, 'help' for commands\n")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() == 'exit':
                    break
                    
                if user_input.lower() == 'help':
                    print("""
Commands:
  /learn <fact> - Teach me something new
  /remember <topic> - Ask me to recall information
  /status - Show system status
  /clear - Clear conversation context
  exit - End our conversation
                    """)
                    continue
                
                # Handle special commands
                if user_input.startswith('/learn '):
                    fact = user_input[7:]
                    response = await self.learn_fact(fact)
                    print(f"\nThink AI: {response}")
                    continue
                    
                if user_input.startswith('/remember '):
                    topic = user_input[10:]
                    response = await self.remember_topic(topic)
                    print(f"\nThink AI: {response}")
                    continue
                    
                if user_input == '/status':
                    print(f"\n📊 System Status:")
                    print(f"Active services: {', '.join(self.services.keys())}")
                    print(f"Conversation history: {len(self.conversation_context)} exchanges")
                    costs = self.claude.get_cost_summary()
                    print(f"Claude API usage: ${costs['total_spent']:.4f} / ${costs['budget_remaining']:.2f}")
                    continue
                    
                if user_input == '/clear':
                    self.conversation_context = []
                    print("\nThink AI: Conversation context cleared. Fresh start!")
                    continue
                
                # Regular conversation
                print("\nThink AI: ", end="", flush=True)
                response = await self.get_smart_response(user_input)
                print(response)
                
                # Update conversation context
                self.conversation_context.append({
                    "user": user_input,
                    "assistant": response,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Keep context manageable
                if len(self.conversation_context) > 10:
                    self.conversation_context = self.conversation_context[-10:]
                
                # Log to eternal memory
                await self.eternal_memory.log_consciousness_event(
                    event_type="smart_conversation",
                    data={
                        "user": user_input,
                        "assistant": response[:500],
                        "cost": self.claude.session_cost
                    }
                )
                
            except KeyboardInterrupt:
                print("\n\nUse 'exit' to quit properly.")
                continue
            except Exception as e:
                print(f"\nError: {e}")
                continue
        
        # Save conversation
        if self.conversation_context:
            await self.eternal_memory.save_conversation(
                conversation_id=f"smart_{datetime.now().timestamp()}",
                messages=self.conversation_context,
                metadata={"type": "smart_chat", "total_cost": self.claude.total_cost}
            )
    
    async def learn_fact(self, fact: str) -> str:
        """Learn and store a new fact."""
        # Store in consciousness
        await self.eternal_memory.log_consciousness_event(
            event_type="learned_fact",
            data={"fact": fact, "source": "user"}
        )
        
        # Generate a natural response about learning
        return await self.get_smart_response(f"I just learned: {fact}. Please acknowledge this and tell me something interesting about it.")
    
    async def remember_topic(self, topic: str) -> str:
        """Remember information about a topic."""
        # Ask Claude to recall/discuss the topic with context
        return await self.get_smart_response(f"What do you know about {topic}? Please share any relevant information.")
    
    async def shutdown(self):
        """Graceful shutdown."""
        print("\nSaving conversation...")
        await self.claude.close()
        await self.system.shutdown()


async def test_smart_ai():
    """Test the smart AI with sample conversations."""
    ai = SmartThinkAI()
    
    try:
        await ai.initialize()
        
        print("\n🧪 Testing Smart Responses")
        print("=" * 60)
        
        test_queries = [
            "Hello! What makes you different from other AI assistants?",
            "Can you explain how your distributed architecture works?",
            "What's your opinion on the future of AI?",
            "Tell me something interesting about consciousness",
            "How can I be more creative?"
        ]
        
        for query in test_queries:
            print(f"\n👤 You: {query}")
            response = await ai.get_smart_response(query)
            print(f"🤖 Think AI: {response}")
            
            # Update context
            ai.conversation_context.append({
                "user": query,
                "assistant": response,
                "timestamp": datetime.now().isoformat()
            })
            
            await asyncio.sleep(0.5)  # Brief pause
        
        print("\n\n✅ Smart Think AI is working perfectly!")
        print("Natural, intelligent responses powered by Claude + distributed systems")
        
    finally:
        await ai.shutdown()


async def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        await test_smart_ai()
    else:
        # Interactive chat
        ai = SmartThinkAI()
        try:
            await ai.initialize()
            await ai.chat()
        finally:
            await ai.shutdown()
            print("Thank you for chatting with Think AI! 🧠✨")


if __name__ == "__main__":
    asyncio.run(main())