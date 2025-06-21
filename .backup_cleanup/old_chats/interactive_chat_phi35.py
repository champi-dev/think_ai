#!/usr/bin/env python3
"""Interactive chat with Think AI using Phi-3.5 Mini."""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI


class ThinkAIChatPhi35:
    """Interactive chat with Phi-3.5 Mini integrated Think AI."""

    def __init__(self) -> None:
        self.think_ai = ProperThinkAI()
        self.stats = {
            "queries": 0,
            "cache_hits": 0,
            "phi35_responses": 0,
            "claude_calls": 0,
            "total_cost": 0.0,
        }

    async def initialize(self) -> None:
        """Initialize Think AI with Phi-3.5 Mini."""
        await self.think_ai.initialize()

    async def chat_loop(self) -> None:
        """Main chat interaction loop."""
        while True:
            try:
                query = input("\n🤔 You: ").strip()

                if not query:
                    continue

                if query.lower() in ["/quit", "/exit", "quit", "exit"]:
                    await self.show_session_stats()
                    break

                if query.lower() in ["/stats", "stats"]:
                    await self.show_session_stats()
                    continue

                if query.lower() in ["/help", "help"]:
                    self.show_help()
                    continue

                # Process query
                start_time = datetime.now()

                result = await self.think_ai.process_with_proper_architecture(query)

                (datetime.now() - start_time).total_seconds()

                # Update stats
                self.stats["queries"] += 1
                if result["source"] == "cache":
                    self.stats["cache_hits"] += 1
                elif result["source"] == "distributed":
                    self.stats["phi35_responses"] += 1  # Phi-3.5 generated the response
                elif result["source"] == "claude_enhanced":
                    self.stats["claude_calls"] += 1
                    self.stats["phi35_responses"] += 1  # Phi-3.5 was used first
                    self.stats["total_cost"] += 0.015  # Approximate Claude cost

                # Display response

                # Show quick stats
                if self.stats["queries"] % 5 == 0:
                    (self.stats["cache_hits"] / self.stats["queries"]) * 100
                    (self.stats["phi35_responses"] / self.stats["queries"]) * 100

            except KeyboardInterrupt:
                pass
            except Exception:
                pass

    def show_help(self) -> None:
        """Show help information."""

    async def show_session_stats(self) -> None:
        """Display session statistics."""
        if self.stats["queries"] > 0:
            (self.stats["cache_hits"] / self.stats["queries"]) * 100
            (self.stats["phi35_responses"] / self.stats["queries"]) * 100
            (self.stats["claude_calls"] / self.stats["queries"]) * 100

            # Cost analysis
            baseline_cost = self.stats["queries"] * 0.015  # If all went to Claude
            actual_cost = self.stats["total_cost"]
            savings = baseline_cost - actual_cost
            (savings / baseline_cost * 100) if baseline_cost > 0 else 0


async def main() -> None:
    """Run the interactive chat."""
    chat = ThinkAIChatPhi35()

    try:
        await chat.initialize()
        await chat.chat_loop()
    except Exception:
        pass
    finally:
        # Cleanup
        try:
            if hasattr(chat.think_ai, "system") and hasattr(chat.think_ai.system, "initializer"):
                await chat.think_ai.system.initializer.shutdown()
        except Exception:
            pass  # Ignore shutdown errors


if __name__ == "__main__":
    asyncio.run(main())
