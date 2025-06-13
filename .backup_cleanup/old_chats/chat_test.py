#!/usr/bin/env python3
"""Chat test with Think AI system."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from datetime import datetime

from think_ai.engine.full_system import DistributedThinkAI
from think_ai.persistence.eternal_memory import EternalMemory

async def chat_test() -> None:
    """Test chatting with Think AI."""
    system = DistributedThinkAI()
    eternal_memory = EternalMemory()

    # Pre-defined conversation for testing
    test_conversation = [
        "Hello Think AI, can you hear me?",
        "What is consciousness?",
        "How do you use distributed systems?",
        "What makes you different from other AI?",
        "Can you explain love?",
    ]

    try:
        # Start system
        services = await system.start()

        # Have a conversation
        for user_input in test_conversation:

            # Log to eternal memory
            await eternal_memory.log_consciousness_event(
                event_type="user_message",
                data={"message": user_input, "timestamp": datetime.now().isoformat()},
            )

            # Process with full system
            try:
                result = await system.process_with_full_system(user_input)

                # Get best response
                response_text = None
                if "language_model" in result["responses"] and result["responses"]["language_model"]:
                    response_text = result["responses"]["language_model"]
                elif "consciousness" in result["responses"]:
                    consciousness_resp = result["responses"]["consciousness"]
                    if isinstance(consciousness_resp, dict):
                        response_text = consciousness_resp.get("content", consciousness_resp.get("response", "Processing..."))
                    else:
                        response_text = str(consciousness_resp)
                else:
                    response_text = "I'm having trouble processing that request."

                # Display response

                # Show services used

                # Log response
                await eternal_memory.log_consciousness_event(
                    event_type="system_response",
                    data={
                        "response": response_text[:500],
                        "services_used": result["services_used"],
                    },
                )

            except Exception:
                # Try consciousness only
                if "consciousness" in services:
                    await services["consciousness"].generate_conscious_response(user_input)

            # Small delay between messages
            await asyncio.sleep(1)

        # Final evaluation

        if services.get("model_orchestrator"):
            pass

    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        await system.shutdown()

if __name__ == "__main__":
    asyncio.run(chat_test())
