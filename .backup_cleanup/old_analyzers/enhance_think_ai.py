#!/usr/bin/env python3
"""Enhance Think AI to give more natural and useful responses."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from datetime import datetime

from think_ai.engine.claude_internal_tool import ClaudeInternalTool
from think_ai.engine.full_system import DistributedThinkAI
from think_ai.persistence.eternal_memory import EternalMemory

class EnhancedThinkAI:
    """Enhanced Think AI with better response generation."""

    def __init__(self) -> None:
        self.system = DistributedThinkAI()
        self.eternal_memory = EternalMemory()
        self.claude_tool = None
        self.services = None

    async def initialize(self):
        """Initialize enhanced system."""
        self.services = await self.system.start()

        # Initialize Claude as internal tool
        if "consciousness" in self.services:
            self.claude_tool = ClaudeInternalTool(self.services["consciousness"])

        return self.services

    async def process_enhanced(self, user_input: str) -> str:
        """Process query with enhanced response generation."""
        # First, get Think AI's initial response
        result = await self.system.process_with_full_system(user_input)

        # Extract initial response
        initial_response = None
        if "consciousness" in result["responses"]:
            consciousness_resp = result["responses"]["consciousness"]
            if isinstance(consciousness_resp, dict):
                initial_response = consciousness_resp.get("content", "")
            else:
                initial_response = str(consciousness_resp)

        # If we have Claude, enhance the response
        if self.claude_tool and initial_response:
            try:
                # Ask Claude to improve the response
                enhancement_query = f"""Please improve this AI response to be more natural, helpful, and informative:

User Query: {user_input}

Current Response: {initial_response}

Please provide a better response that:
1. Directly addresses the user's question
2. Is conversational and natural
3. Provides useful information
4. Shows understanding and empathy
5. Is concise but complete

Improved response:"""

                claude_result = await self.claude_tool.claude_api.query(
                    prompt=enhancement_query,
                    system="You are helping improve an AI assistant's responses. Make them natural, helpful, and engaging.",
                    temperature=0.7,
                )

                if claude_result and "response" in claude_result:
                    return claude_result["response"]
            except Exception:
                pass

        # If no Claude or enhancement failed, try to improve locally
        if "language_model" in result["responses"] and result["responses"]["language_model"]:
            return result["responses"]["language_model"]

        return initial_response or "I'm here to help. Could you please rephrase your question?"

    async def chat_session(self) -> None:
        """Interactive chat session with enhanced responses."""
        conversation_history = []

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == "exit":
                    break

                if user_input.lower() == "help":
                    continue

                # Special commands
                if user_input.startswith("/teach "):
                    fact = user_input[7:]
                    await self.teach_fact(fact)
                    continue

                if user_input.startswith("/recall "):
                    topic = user_input[8:]
                    await self.recall_information(topic)
                    continue

                if user_input == "/services":
                    continue

                # Regular chat
                response = await self.process_enhanced(user_input)

                # Log conversation
                conversation_history.append({
                    "user": user_input,
                    "assistant": response,
                    "timestamp": datetime.now().isoformat(),
                })

                # Store in eternal memory
                await self.eternal_memory.log_consciousness_event(
                    event_type="enhanced_conversation",
                    data={
                        "user_input": user_input,
                        "response": response[:500],
                        "services_used": list(self.services.keys()),
                    },
                )

            except KeyboardInterrupt:
                continue
            except Exception:
                continue

        # Save conversation
        if conversation_history:
            await self.eternal_memory.save_conversation(
                conversation_id=f"enhanced_{datetime.now().timestamp()}",
                messages=conversation_history,
                metadata={"type": "enhanced_chat", "improvements": True},
            )

    async def teach_fact(self, fact: str) -> None:
        """Teach Think AI a new fact."""
        # Store in ScyllaDB
        if "scylla" in self.services:
            try:
                import json

                from think_ai.storage.base import StorageItem

                item = StorageItem(
                    key=f"learned_fact_{datetime.now().timestamp()}",
                    value=json.dumps({
                        "fact": fact,
                        "timestamp": datetime.now().isoformat(),
                        "source": "user_teaching",
                    }),
                    metadata={"type": "learned_fact"},
                )

                await self.services["scylla"].put(item.key, item)
            except Exception:
                pass

        # Also log to consciousness
        await self.eternal_memory.log_consciousness_event(
            event_type="learned_fact",
            data={"fact": fact},
        )

    async def recall_information(self, topic: str) -> None:
        """Recall information about a topic."""
        # Search in ScyllaDB
        if "scylla" in self.services:
            try:
                # Search for related facts
                results = []
                async for _key, item in self.services["scylla"].scan(prefix="learned_fact_", limit=100):
                    if topic.lower() in item.content.lower():
                        results.append(item.content)

                if results:
                    for _i, _fact in enumerate(results[:3], 1):
                        pass
                else:
                    pass
            except Exception:
                pass

    async def shutdown(self) -> None:
        """Shutdown enhanced system."""
        await self.system.shutdown()

async def test_enhanced_chat() -> None:
    """Test the enhanced Think AI system."""
    enhanced_ai = EnhancedThinkAI()

    try:
        await enhanced_ai.initialize()

        # Test queries
        test_queries = [
            "Hello! How are you today?",
            "Can you explain quantum computing in simple terms?",
            "What's the meaning of life?",
            "How can I be more productive?",
            "Tell me a joke",
        ]

        for query in test_queries:
            await enhanced_ai.process_enhanced(query)
            await asyncio.sleep(1)

        # Test teaching
        await enhanced_ai.teach_fact("The capital of France is Paris")
        await enhanced_ai.teach_fact("Water boils at 100 degrees Celsius at sea level")
        await asyncio.sleep(1)
        await enhanced_ai.recall_information("France")
        await enhanced_ai.recall_information("water")

    finally:
        await enhanced_ai.shutdown()

async def main() -> None:
    """Main entry point."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "chat":
        # Interactive chat mode
        enhanced_ai = EnhancedThinkAI()
        try:
            await enhanced_ai.initialize()
            await enhanced_ai.chat_session()
        finally:
            await enhanced_ai.shutdown()
    else:
        # Test mode
        await test_enhanced_chat()

if __name__ == "__main__":
    asyncio.run(main())
