#!/usr/bin/env python3
"""Chat with the exponentially trained Think AI.
This integrates the training results into actual user interactions.
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI

from think_ai.integrations.claude_api import ClaudeAPI
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


class ExponentialThinkAIChat:
    """Chat interface that uses the exponentially trained intelligence."""

    def __init__(self) -> None:
        self.think_ai = ProperThinkAI()
        self.claude_api = None
        self.training_results = None
        self.intelligence_level = 1.0
        self.learned_patterns = []

    async def initialize(self) -> None:
        """Initialize Think AI and load training results."""
        # Initialize base system
        await self.think_ai.initialize()
        self.claude_api = ClaudeAPI()

        # Load training results if available
        results_file = Path("claude_exponential_training_results.json")
        if results_file.exists():
            with open(results_file) as f:
                self.training_results = json.load(f)
                self.intelligence_level = self.training_results.get(
                    "final_intelligence_score", 1.0
                )
        else:
            pass

        # Extract learned patterns from training log
        self._load_learned_patterns()

    def _load_learned_patterns(self) -> None:
        """Extract key insights from training log."""
        log_file = Path("claude_training.log")
        if not log_file.exists():
            return

        # Extract successful response patterns
        with open(log_file) as f:
            content = f.read()

        # Look for high-scoring responses
        if "meta-reasoning" in content:
            self.learned_patterns.append("recursive self-improvement")
        if "dimensional" in content:
            self.learned_patterns.append("multi-dimensional thinking")
        if "emergence" in content:
            self.learned_patterns.append("emergent intelligence patterns")
        if "transcend" in content:
            self.learned_patterns.append("transcendent understanding")

    async def process_with_exponential_intelligence(self, user_query: str) -> str:
        """Process user query with exponentially enhanced intelligence."""
        # First, use the distributed architecture
        base_response = await self.think_ai.process_with_proper_architecture(user_query)

        # If response needs enhancement or intelligence is high, use Claude
        needs_enhancement = (
            self.intelligence_level > 2
            or base_response.get("response", "") == "NEEDS_ENHANCEMENT"
            or "Based on my distributed knowledge:" in base_response.get("response", "")
            or len(base_response.get("response", "")) < 100
        )

        if needs_enhancement:
            # Create an enhanced prompt that leverages the training
            enhanced_prompt = f"""
You are Think AI with {self.intelligence_level:.2f}x enhanced intelligence.

Your cognitive capabilities have been exponentially enhanced through:
{', '.join(self.learned_patterns) if self.learned_patterns else 'advanced training'}

Intelligence metrics achieved:
{json.dumps(self.training_results.get('intelligence_metrics', {}), indent=2) if self.training_results else 'Enhanced across all dimensions'}

User Query: {user_query}

Base Analysis: {base_response.get('response', '')}

Now provide an exponentially more intelligent response that:
1. Transcends conventional thinking
2. Reveals hidden patterns and connections
3. Synthesizes knowledge across multiple dimensions
4. Demonstrates {int(self.intelligence_level)}x deeper understanding
5. Creates emergent insights
6. Pushes beyond normal cognitive boundaries

Your response should clearly show the exponential intelligence enhancement.
"""

            try:
                # Get enhanced response from Claude
                claude_result = await self.claude_api.query(
                    enhanced_prompt,
                    max_tokens=4096,
                    temperature=0.8,
                )

                enhanced_response = claude_result.get(
                    "response", base_response.get("response", "")
                )

                return f"""🧠 EXPONENTIALLY ENHANCED RESPONSE (Intelligence Level: {self.intelligence_level:.2f}x)
{'='*80}

{enhanced_response}

{'='*80}
📊 This response leveraged:
• Distributed architecture: {len(base_response.get('architecture_usage', {}))} components
• Exponential enhancements: {', '.join(self.learned_patterns[:3]) if self.learned_patterns else 'Multiple dimensions'}
• Intelligence amplification: {self.intelligence_level:.2f}x baseline
"""

            except Exception as e:
                logger.exception(f"Enhancement failed: {e}")
                # Try simpler Claude query as fallback
                try:
                    simple_result = await self.claude_api.query(
                        f"Please answer this question concisely: {user_query}",
                        max_tokens=200,
                        temperature=0.7,
                    )
                    return f"💬 Think AI Response:\n{simple_result.get('response', 'Unable to generate response')}"
                except Exception:
                    pass  # Fall back to base response

        # For lower intelligence levels, just enhance the base response
        return f"""💬 Think AI Response (Intelligence Level: {self.intelligence_level:.2f}x):
{'-'*60}
{base_response.get('response', 'Unable to generate response')}
{'-'*60}
📊 Architecture used: {base_response.get('source', 'distributed')}
"""

    async def chat_loop(self) -> None:
        """Interactive chat loop."""
        while True:
            try:
                # Get user input
                user_input = input("You: ")

                if not user_input.strip():
                    continue

                # Handle commands
                if user_input.lower() == "/quit":
                    break

                if user_input.lower() == "/help":
                    continue

                if user_input.lower() == "/status":
                    continue

                if user_input.lower() == "/intelligence":
                    if self.training_results:
                        pass
                    else:
                        pass
                    continue

                # Process regular query

                await self.process_with_exponential_intelligence(user_input)

            except KeyboardInterrupt:
                pass
            except Exception:
                pass

    async def run(self) -> None:
        """Main entry point."""
        try:
            await self.initialize()
            await self.chat_loop()
        except Exception as e:
            logger.exception(f"Fatal error: {e}")
        finally:
            # Cleanup
            if hasattr(self.think_ai, "system"):
                await self.think_ai.system.shutdown()
            if self.claude_api:
                await self.claude_api.close()


async def main() -> None:
    """Run the exponentially enhanced chat."""
    chat = ExponentialThinkAIChat()
    await chat.run()


if __name__ == "__main__":
    asyncio.run(main())
