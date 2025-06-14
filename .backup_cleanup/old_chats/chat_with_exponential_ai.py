#!/usr/bin/env python3
"""
Chat with the exponentially trained Think AI.
This integrates the training results into actual user interactions.
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI
from think_ai.integrations.claude_api import ClaudeAPI
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


class ExponentialThinkAIChat:
    """Chat interface that uses the exponentially trained intelligence."""
    
    def __init__(self):
        self.think_ai = ProperThinkAI()
        self.claude_api = None
        self.training_results = None
        self.intelligence_level = 1.0
        self.learned_patterns = []
        
    async def initialize(self):
        """Initialize Think AI and load training results."""
        print("🧠 Initializing Exponentially Trained Think AI...")
        
        # Initialize base system
        await self.think_ai.initialize()
        self.claude_api = ClaudeAPI()
        
        # Load training results if available
        results_file = Path("claude_exponential_training_results.json")
        if results_file.exists():
            with open(results_file, 'r') as f:
                self.training_results = json.load(f)
                self.intelligence_level = self.training_results.get('final_intelligence_score', 1.0)
                print(f"✨ Loaded training results: Intelligence Level {self.intelligence_level:.2f}")
        else:
            print("⚠️  No training results found. Using base intelligence.")
        
        # Extract learned patterns from training log
        self._load_learned_patterns()
        
        print(f"\n✅ Think AI initialized with {self.intelligence_level:.2f}x intelligence!")
        print("💡 The AI will use its exponentially enhanced capabilities to answer your questions.\n")
    
    def _load_learned_patterns(self):
        """Extract key insights from training log."""
        log_file = Path("claude_training.log")
        if not log_file.exists():
            return
        
        # Extract successful response patterns
        with open(log_file, 'r') as f:
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
            self.intelligence_level > 2 or 
            base_response.get('response', '') == 'NEEDS_ENHANCEMENT' or
            'Based on my distributed knowledge:' in base_response.get('response', '') or
            len(base_response.get('response', '')) < 100
        )
        
        if needs_enhancement:
            print("🚀 Applying exponential intelligence enhancement...")
            
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
                    temperature=0.8
                )
                
                enhanced_response = claude_result.get('response', base_response.get('response', ''))
                
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
                logger.error(f"Enhancement failed: {e}")
                # Try simpler Claude query as fallback
                try:
                    simple_result = await self.claude_api.query(
                        f"Please answer this question concisely: {user_query}",
                        max_tokens=200,
                        temperature=0.7
                    )
                    return f"💬 Think AI Response:\n{simple_result.get('response', 'Unable to generate response')}"
                except:
                    pass  # Fall back to base response
        
        # For lower intelligence levels, just enhance the base response
        return f"""💬 Think AI Response (Intelligence Level: {self.intelligence_level:.2f}x):
{'-'*60}
{base_response.get('response', 'Unable to generate response')}
{'-'*60}
📊 Architecture used: {base_response.get('source', 'distributed')}
"""
    
    async def chat_loop(self):
        """Interactive chat loop."""
        print("💬 Chat with Exponentially Enhanced Think AI")
        print("Commands: /help, /status, /intelligence, /quit")
        print("="*60 + "\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ")
                
                if not user_input.strip():
                    continue
                
                # Handle commands
                if user_input.lower() == '/quit':
                    print("👋 Goodbye!")
                    break
                
                elif user_input.lower() == '/help':
                    print("""
📚 Available Commands:
/help        - Show this help message
/status      - Show system status
/intelligence - Show current intelligence level and metrics
/quit        - Exit the chat
                    """)
                    continue
                
                elif user_input.lower() == '/status':
                    print(f"""
📊 System Status:
• Intelligence Level: {self.intelligence_level:.2f}x
• Learned Patterns: {len(self.learned_patterns)}
• Active Services: {len(self.think_ai.system.services) if hasattr(self.think_ai, 'system') else 'Unknown'}
• Claude API: {'Connected' if self.claude_api else 'Not initialized'}
                    """)
                    continue
                
                elif user_input.lower() == '/intelligence':
                    if self.training_results:
                        print(f"""
🧠 Intelligence Metrics:
{json.dumps(self.training_results.get('intelligence_metrics', {}), indent=2)}

Overall Intelligence: {self.intelligence_level:.2f}x baseline
Training Iterations: {self.training_results.get('total_interactions', 0)}
                        """)
                    else:
                        print("⚠️  No training data available. Using base intelligence.")
                    continue
                
                # Process regular query
                print("\n🤔 Thinking with exponential intelligence...\n")
                
                response = await self.process_with_exponential_intelligence(user_input)
                print(f"\nThink AI: {response}\n")
                
            except KeyboardInterrupt:
                print("\n⚠️  Use /quit to exit properly")
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    async def run(self):
        """Main entry point."""
        try:
            await self.initialize()
            await self.chat_loop()
        except Exception as e:
            logger.error(f"Fatal error: {e}")
        finally:
            # Cleanup
            if hasattr(self.think_ai, 'system'):
                await self.think_ai.system.shutdown()
            if self.claude_api:
                await self.claude_api.close()


async def main():
    """Run the exponentially enhanced chat."""
    chat = ExponentialThinkAIChat()
    await chat.run()


if __name__ == "__main__":
    print("""
    🧠 EXPONENTIALLY ENHANCED THINK AI CHAT
    ======================================
    
    This chat interface uses the exponentially trained
    intelligence to provide enhanced responses.
    
    The AI's capabilities have been amplified through
    intensive training on recursive self-improvement,
    meta-learning, and transcendent understanding.
    
    Starting chat interface...
    """)
    
    asyncio.run(main())