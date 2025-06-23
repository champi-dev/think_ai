#!/usr/bin/env python3
"""Think AI Full System CLI - Complete Integration with All Components"""

import asyncio
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Import the full Think AI system components
try:
    from think_ai.core.engine import ThinkAIEngine, QueryResult
    from think_ai.core.config import Config
    from think_ai.utils.logging import configure_logging, get_logger

    FULL_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some Think AI components not available: {e}")
    FULL_SYSTEM_AVAILABLE = False

    # Create dummy logger
    class DummyLogger:
        def info(self, msg):
            print(f"[INFO] {msg}")

        def error(self, msg):
            print(f"[ERROR] {msg}")

        def warning(self, msg):
            print(f"[WARNING] {msg}")

    def get_logger(name):
        return DummyLogger()

    def configure_logging(log_level="INFO", log_file=None, json_logs=False):
        pass


# Setup logging
configure_logging()
logger = get_logger(__name__)


class ThinkAIFullCLI:
    """Interactive CLI using the full Think AI system"""

    def __init__(self):
        self.engine: Optional[ThinkAIEngine] = None
        self.running = True
        self.session_start = time.time()
        self.query_count = 0
        self.performance_metrics = []

    async def initialize(self):
        """Initialize the full Think AI engine"""
        if not FULL_SYSTEM_AVAILABLE:
            print("\n⚠️  Full Think AI system not available.")
            print("Running in demonstration mode with limited features.\n")
            return False

        print("\n⚡ Initializing Think AI Full System...")
        print("This may take a moment as we load all components...\n")

        try:
            # Create configuration
            config = Config.from_env()

            # Initialize the engine
            self.engine = ThinkAIEngine(config)
            await self.engine.initialize()

            print("✅ Think AI Engine initialized successfully!")
            print("✅ Components loaded:")

            # Check which components are available
            components = []
            if hasattr(self.engine, "consciousness") and self.engine.consciousness:
                components.append("🧠 Consciousness Framework")
            if hasattr(self.engine, "vector_db") and self.engine.vector_db:
                components.append("🔍 Vector Search (O(1) LSH)")
            if hasattr(self.engine, "knowledge_graph") and self.engine.knowledge_graph:
                components.append("🕸️ Knowledge Graph")
            if hasattr(self.engine, "storage") and self.engine.storage:
                components.append("💾 Distributed Storage")
            if hasattr(self.engine, "cache") and self.engine.cache:
                components.append("⚡ Redis Cache")
            if hasattr(self.engine, "constitutional_ai") and self.engine.constitutional_ai:
                components.append("⚖️ Constitutional AI")
            if hasattr(self.engine, "language_model") and self.engine.language_model:
                components.append("🤖 Language Model")

            for comp in components:
                print(f"   {comp}")

            if not components:
                print("   ⚠️  No advanced components loaded - using basic mode")

            return True

        except Exception as e:
            logger.error(f"Failed to initialize engine: {e}")
            print(f"❌ Error initializing Think AI: {e}")
            print("Falling back to basic mode...")
            return False

    def display_banner(self):
        """Display welcome banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════════╗
║              🧠 THINK AI FULL SYSTEM v5.0                         ║
╠═══════════════════════════════════════════════════════════════════╣
║  ⚡ O(1) Vector Search    │  🧠 Consciousness Framework          ║
║  🕸️  Knowledge Graph       │  ⚖️  Constitutional AI              ║
║  💾 Distributed Storage   │  🤖 Self-Training Intelligence      ║
╚═══════════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def display_help(self):
        """Display help information"""
        help_text = """
📚 Available Commands:
  • stats      - Show performance metrics
  • history    - Display recent conversation  
  • conscious  - Show consciousness state
  • knowledge  - Query knowledge graph
  • train      - Enable self-training mode
  • code       - Generate code for a task
  • clear      - Clear conversation history
  • help       - Show this help message
  • exit       - Exit the program
  
💬 Just type naturally to chat with the full Think AI system!
        """
        print(help_text)

    async def process_query(self, query: str) -> Tuple[str, float]:
        """Process query using the full engine"""
        start_time = time.perf_counter()

        if not self.engine:
            # Fallback response if engine not initialized
            response = "Think AI engine not initialized. Using basic response mode."
            response_time = (time.perf_counter() - start_time) * 1000
            return response, response_time

        try:
            # First, try to find relevant knowledge in the cache/vector store
            query_result = await self.engine.query_knowledge(query)

            # Extract and format the response
            if query_result and query_result.results:
                # Format the results into a response
                response_text = f"Found {len(query_result.results)} results:\n"
                for i, result in enumerate(query_result.results[:3], 1):
                    content = result.get("content", "")
                    if isinstance(content, dict):
                        content = content.get("text", str(content))
                    response_text += f"{i}. {content[:100]}...\n"
            else:
                # No cached results found - use language model to generate response
                if hasattr(self.engine, "language_model") and self.engine.language_model:
                    logger.info(f"No cached results for '{query}', generating response...")
                    try:
                        # Generate response using the language model
                        response = await self.engine.language_model.generate(
                            prompt=query, generation_config={"temperature": 0.7, "max_length": 200, "top_p": 0.9}
                        )

                        # Extract text from response object
                        if hasattr(response, "text"):
                            response_text = response.text
                        else:
                            response_text = str(response)

                        # Optionally store the generated response for future queries
                        if response_text:
                            await self.engine.store_knowledge(
                                key=f"query_{hash(query)}",
                                content={"text": response_text, "query": query},
                                metadata={"source": "generated", "timestamp": datetime.now().isoformat()},
                            )

                    except Exception as e:
                        logger.error(f"Error generating response: {e}")
                        response_text = "I'm having trouble generating a response. Please try again."
                else:
                    response_text = "No language model available. Cannot generate response."

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            response_text = f"Error processing query: {str(e)}"

        response_time = (time.perf_counter() - start_time) * 1000
        self.query_count += 1
        self.performance_metrics.append(response_time)

        return response_text, response_time

    def display_stats(self):
        """Display performance statistics"""
        if not self.performance_metrics:
            print("\n📊 No queries processed yet.")
            return

        import numpy as np

        elapsed = time.time() - self.session_start

        print("\n📊 PERFORMANCE METRICS (Full System)")
        print("=" * 60)
        print(f"💭 Queries Processed: {self.query_count}")
        print(f"⏱️  Session Time: {elapsed:.2f}s")
        print(f"⚡ Avg Response: {np.mean(self.performance_metrics):.3f}ms")
        print(f"🏃 Min Response: {np.min(self.performance_metrics):.3f}ms")
        print(f"🐌 Max Response: {np.max(self.performance_metrics):.3f}ms")
        print(f"📈 Median Response: {np.median(self.performance_metrics):.3f}ms")
        print(f"🧠 Query Rate: {self.query_count / elapsed:.1f} queries/sec")

        if self.engine:
            print("\n🔧 System Components Active:")
            if self.engine.consciousness:
                print("   ✅ Consciousness Framework")
            if self.engine.vector_db:
                print("   ✅ O(1) Vector Search")
            if self.engine.knowledge_graph:
                print("   ✅ Knowledge Graph")
            if self.engine.storage:
                print("   ✅ Distributed Storage")
        print("=" * 60)

    async def display_consciousness_state(self):
        """Display current consciousness state"""
        if not self.engine or not hasattr(self.engine, "consciousness") or not self.engine.consciousness:
            print("\n🧠 Consciousness framework not available.")
            return

        try:
            # Check if get_state method exists
            if hasattr(self.engine.consciousness, "get_state"):
                state = await self.engine.consciousness.get_state()
            else:
                # Fallback to accessing attributes directly
                state = {
                    "awareness_level": getattr(self.engine.consciousness, "awareness_level", "Unknown"),
                    "active_thoughts": getattr(self.engine.consciousness, "active_thoughts", 0),
                    "neural_pathways": getattr(self.engine.consciousness, "neural_pathways", 0),
                    "wisdom": getattr(self.engine.consciousness, "wisdom", 0),
                }

            print("\n🧠 CONSCIOUSNESS STATE")
            print("=" * 60)
            print(f"Awareness Level: {state.get('awareness_level', 'Unknown')}")
            print(f"Active Thoughts: {state.get('active_thoughts', 0)}")
            print(f"Neural Pathways: {state.get('neural_pathways', 0)}")
            print(f"Wisdom Points: {state.get('wisdom', 0)}")
            print("=" * 60)
        except Exception as e:
            print(f"\n❌ Error accessing consciousness state: {e}")

    async def run(self):
        """Main CLI loop"""
        self.display_banner()

        # Initialize the full engine
        initialized = await self.initialize()

        if initialized:
            print("\n💭 Full Think AI system ready! Type 'help' for commands.\n")
        else:
            print("\n💭 Running in basic mode. Type 'help' for commands.\n")

        while self.running:
            try:
                # Get user input
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Handle commands
                command = user_input.lower()

                if command == "exit":
                    print("\n👋 Thank you for using Think AI Full System!")
                    self.running = False
                    break
                elif command == "help":
                    self.display_help()
                    continue
                elif command == "stats":
                    self.display_stats()
                    continue
                elif command == "conscious":
                    await self.display_consciousness_state()
                    continue
                elif command == "clear":
                    self.performance_metrics.clear()
                    self.query_count = 0
                    print("\n🧹 Session data cleared.")
                    continue

                # Process regular query with full system
                response, response_time = await self.process_query(user_input)
                print(f"\nThink AI: {response}")
                print(f"[⚡ {response_time:.3f}ms]")

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                self.running = False
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'exit' to quit.")


def main():
    """Main entry point"""
    try:
        # Create and run the CLI
        cli = ThinkAIFullCLI()
        asyncio.run(cli.run())
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
