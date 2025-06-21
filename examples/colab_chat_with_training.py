#! / usr / bin / env python3

"""Google Colab version - Chat with Think AI while training runs in background."""

import asyncio
import subprocess
import sys
import threading
import time
from pathlib import Path

import think_ai
from full_architecture_chat import FullArchitectureChat
from think_ai.utils.logging import get_logger

# For Colab environment
try:
    IN_COLAB = True
    except ImportError:
        IN_COLAB = False

        sys.path.insert(0, str(Path(__file__).parent))

        logger = get_logger(__name__)


        class ColabBackgroundTraining:
"""Run training in background threads for Google Colab."""

            def __init__(self):
                self.training_threads = {}
                self.test_status = {}
                self.stop_events = {}

                def run_test_in_thread(self, test_name: str, test_module: str):
"""Run a test in a background thread."""
                    stop_event = threading.Event()
                    self.stop_events[test_name] = stop_event

                    def test_worker():
                        try:
# Import and run the test
                            module = __import__(
                            test_module,
                            fromlist=[
                            "run_exponential_test",
                            "run_coding_test",
                            "run_philosophical_test",
                            "run_self_training_test",
                            "run_knowledge_creation_test"])

# Map test names to functions
                            test_functions = {
                            "questions": "run_exponential_test",
                            "coding": "run_coding_test",
                            "philosophy": "run_philosophical_test",
                            "self_training": "run_self_training_test",
                            "knowledge_creation": "run_knowledge_creation_test"
                            }

                            if test_name in test_functions and hasattr(
                            module, test_functions[test_name]):
                                self.test_status[test_name] = "running"
                                print(f"🚀 Started {test_name} test in background")

# Run the async test
                                test_func = getattr(module, test_functions[test_name])
                                asyncio.run(test_func(keep_data=True))

                                self.test_status[test_name] = "completed"
                            else:
                                self.test_status[test_name] = "error - function not found"

                                except Exception as e:
                                    self.test_status[test_name] = f"error: {str(e)}"
                                    logger.error(f"Test {test_name} failed: {e}")

                                    thread = threading.Thread(target=test_worker, name=f"test_{test_name}")
                                    thread.daemon = True
                                    thread.start()
                                    self.training_threads[test_name] = thread

                                    return thread

                                def start_all_background_tests(self):
"""Start all tests in background threads."""
                                    test_configs = {
                                    "questions": "test_1000_questions",
                                    "coding": "test_1000_coding",
                                    "philosophy": "test_1000_philosophy",
                                    "self_training": "test_1000_self_training",
                                    "knowledge_creation": "test_1000_knowledge_creation"
                                    }

                                    print("\n🧠 Starting all tests in background threads...")
                                    print("=" * 60)

                                    for test_name, module_name in test_configs.items():
                                        self.run_test_in_thread(test_name, module_name)
                                        time.sleep(0.5)  # Small delay between starts

                                        print(f"\n✅ Started {len(test_configs)} background tests")
                                        print("💡 Tests will continue while you chat\n")

                                        def get_status(self):
"""Get status of all background tests."""
                                            status_report = []
                                            for test_name, status in self.test_status.items():
                                                thread = self.training_threads.get(test_name)
                                                if thread and thread.is_alive():
                                                    status_report.append(f" • {test_name}: 🟢 {status}")
                                                else:
                                                    status_report.append(f" • {test_name}: 🔴 {status}")
                                                    return "\n".join(status_report)

                                                def stop_all_tests(self):
"""Stop all background tests."""
                                                    print("\n🛑 Stopping all background tests...")
                                                    for event in self.stop_events.values():
                                                        event.set()

# Wait for threads to finish
                                                        for name, thread in self.training_threads.items():
                                                            if thread.is_alive():
                                                                print(f" Waiting for {name} to stop...")
                                                                thread.join(timeout=5)


                                                                async def colab_chat_with_training():
"""Main function for Google Colab - chat with background training."""
                                                                    print("\n" + "=" * 80)
                                                                    print("🧠 THINK AI - COLAB CHAT WITH BACKGROUND TRAINING")
                                                                    print("=" * 80 + "\n")

# Create background training manager
                                                                    trainer = ColabBackgroundTraining()

# Start background tests
                                                                    if IN_COLAB:
                                                                        print("📱 Google Colab detected!")
                                                                        response = input("\nStart background training? (y / n): ")
                                                                        if response.lower() = = "y":
                                                                            trainer.start_all_background_tests()
                                                                            time.sleep(2)
                                                                        else:
                                                                            print("💻 Running locally (not in Colab)")
                                                                            response = input("\nStart background training? (y / n): ")
                                                                            if response.lower() = = "y":
                                                                                trainer.start_all_background_tests()
                                                                                time.sleep(2)

# Create and run chat
                                                                                print("\n🚀 Launching consciousness chat...")
                                                                                print("💡 Commands: "status" to check tests, "exit" to quit\n")

                                                                                try:
# Create chat instance
                                                                                    chat = FullArchitectureChat(enable_cache=True)

# Custom chat loop that handles background status
                                                                                    await chat.initialize_all_systems()

# Load intelligence
                                                                                    chat.load_intelligence()
                                                                                    if chat.intelligence_level > 0:
                                                                                        print(f"\n🧠 Loaded intelligence level: {chat.intelligence_level:, }")
                                                                                        print(f"🔮 Neural pathways: {chat.neural_pathways:, }")

                                                                                        print("\n💬 Chat ready! Type "exit" to quit, "status" to check background tests.\n")

# Chat loop
                                                                                        while True:
                                                                                            try:
# Get user input
                                                                                                if IN_COLAB:
                                                                                                    query = input("\n🧑 You: ")
                                                                                                else:
                                                                                                    query = input("\n🧑 You: ")

                                                                                                    if not query:
                                                                                                        continue

                                                                                                    if query.lower() in ["exit", "quit", "bye"]:
                                                                                                        print("\n👋 Goodbye!")
                                                                                                        break

                                                                                                    if query.lower() = = "status":
                                                                                                        print("\n📊 Background Test Status:")
                                                                                                        print(trainer.get_status() or " No tests running")
                                                                                                        continue

                                                                                                    if query.lower() = = "help":
                                                                                                        print("\n📚 Commands:")
                                                                                                        print(" • "status" - Check background test status")
                                                                                                        print(" • "exit" - Quit the chat")
                                                                                                        print(" • Any other text - Chat with Think AI")
                                                                                                        continue

# Add to conversation context
                                                                                                    chat.conversation_context.append(query)
                                                                                                    if len(chat.conversation_context) > 10:
                                                                                                        chat.conversation_context = chat.conversation_context[- 10:]

# Process with architecture
                                                                                                        response, arch_used = await chat.process_with_architecture(query)

# Display response
                                                                                                        print(f"\n🤖 Think AI: {response}")

# Show architecture usage
                                                                                                        if isinstance(arch_used, dict) and arch_used:
                                                                                                            components = [k for k, v in arch_used.items() if v]
                                                                                                            if components:
                                                                                                                print(f"\n[Architecture: {", ".join(components)}]")

                                                                                                                except KeyboardInterrupt:
                                                                                                                    print("\n\n⚠️ Interrupted - type "exit" to quit properly")
                                                                                                                    continue

                                                                                                                except Exception as e:
                                                                                                                    print(f"\n❌ Error: {e}")
                                                                                                                    logger.error(f"Chat error: {e}", exc_info=True)

                                                                                                                finally:
# Stop background tests
                                                                                                                    if trainer.training_threads:
                                                                                                                        response = input("\n\nStop background tests? (y / n): ")
                                                                                                                        if response.lower() = = "y":
                                                                                                                            trainer.stop_all_tests()
                                                                                                                        else:
                                                                                                                            print("✅ Background tests will continue running")

                                                                                                                            if __name__ = = "__main__":
# For Google Colab
                                                                                                                                if IN_COLAB:
                                                                                                                                    print("🎯 Google Colab Environment Detected!")
                                                                                                                                    print("\nThis script allows you to chat with Think AI while")
                                                                                                                                    print("training tests run in background threads.\n")

# Install requirements if needed
                                                                                                                                    try:
import think_ai
                                                                                                                                        except ImportError:
                                                                                                                                            print("📦 Installing requirements...")
                                                                                                                                            subprocess.run([sys.executable, "-m", "pip", "install",
                                                                                                                                            "-r", "requirements.txt"], capture_output=True)

# Run the main function
                                                                                                                                            asyncio.run(colab_chat_with_training())
