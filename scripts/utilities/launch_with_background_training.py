#! / usr / bin / env python3

"""Launch Think AI with background training - chat while tests run."""

import asyncio
import json
import os
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict

from full_architecture_chat import FullArchitectureChat
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from think_ai.utils.logging import get_logger

sys.path.insert(0, str(Path(__file__).parent))

logger = get_logger(__name__)
console = Console()


class BackgroundTrainingLauncher:
"""Launch consciousness with background training processes."""

    def __init__(self):
        self.test_processes: Dict[str, subprocess.Popen] = {}
        self.test_configs = {
        "questions": {
        "script": "test_1000_questions.py",
        "name": "Questions Test",
        "icon": "🧪"
        },
        "coding": {
        "script": "test_1000_coding.py",
        "name": "Coding Test",
        "icon": "💻"
        },
        "philosophy": {
        "script": "test_1000_philosophy.py",
        "name": "Philosophy Test",
        "icon": "🧘"
        },
        "self_training": {
        "script": "test_1000_self_training.py",
        "name": "Self - Training Test",
        "icon": "🧠"
        },
        "knowledge_creation": {
        "script": "test_1000_knowledge_creation.py",
        "name": "Knowledge Creation",
        "icon": "🌌"
        }
        }
        self.monitoring = False
        self.monitor_thread = None
        self.shutdown_requested = False

        def start_background_test(self, test_key: str) - > bool:
"""Start a single test in the background."""
            if test_key not in self.test_configs:
                return False

            config = self.test_configs[test_key]
            script_path = Path(__file__).parent / config["script"]

            try:
# Launch test as subprocess with output redirected
                log_file = f"{test_key}_background_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log"
                with open(log_file, "w") as log:
                    process = subprocess.Popen(
                    [sys.executable, str(script_path), "--keep - data"],
                    stdout = log,
                    stderr = subprocess.STDOUT,
                    preexec_fn = os.setsid if os.name ! = "nt" else None
                    )

                    self.test_processes[test_key] = process
                    console.print(f"{config["icon"]} Started {config["name"]} in background (PID: {process.pid})")
                    console.print(f" 📄 Logging to: {log_file}")
                    return True

                except Exception as e:
                    console.print(f"❌ Failed to start {config["name"]}: {e}")
                    return False

                def start_all_tests(self):
"""Start all tests in background."""
                    console.print("\n🚀 Starting all tests in background...")
                    console.print("=" * 60)

                    started = 0
                    for test_key in self.test_configs:
                        if self.start_background_test(test_key):
                            started + = 1
                            time.sleep(0.5) # Small delay between launches

                            console.print(f"\n✅ Started {started}/{len(self.test_configs)} tests in background")
                            console.print("💡 Tests will continue running while you chat\n")

                            def check_test_status(self) - > Dict[str, str]:
"""Check status of all background tests."""
                                status = {}
                                for test_key, process in self.test_processes.items():
                                    if process.poll() is None:
                                        status[test_key] = "running"
                                    else:
                                        status[test_key] = f"completed (exit code: {process.returncode})"
                                        return status

                                    def monitor_tests(self):
"""Monitor test progress in a separate thread."""
                                        while self.monitoring and not self.shutdown_requested:
                                            self.check_test_status()

# Create status table
                                            table = Table(title = "Background Test Status", show_header = True)
                                            table.add_column("Test", style = "cyan")
                                            table.add_column("Status", style = "green")
                                            table.add_column("PID", style = "yellow")

                                            for test_key, process in self.test_processes.items():
                                                config = self.test_configs[test_key]
                                                status_text = "🟢 Running" if process.poll() is None else f"🔴 Exited ({process.returncode})"
                                                table.add_row(
                                                f"{config["icon"]} {config["name"]}",
                                                status_text,
                                                str(process.pid) if process.poll() is None else "-"
                                                )

# Clear and print table
                                                os.system("clear" if os.name ! = "nt" else "cls")
                                                console.print(table)
                                                console.print("\nPress Ctrl + C to return to chat...")

                                                time.sleep(5) # Update every 5 seconds

                                                def start_monitoring(self):
"""Start monitoring in a separate thread."""
                                                    self.monitoring = True
                                                    self.monitor_thread = threading.Thread(target = self.monitor_tests)
                                                    self.monitor_thread.daemon = True
                                                    self.monitor_thread.start()

                                                    def stop_monitoring(self):
"""Stop monitoring thread."""
                                                        self.monitoring = False
                                                        if self.monitor_thread:
                                                            self.monitor_thread.join(timeout = 1)

                                                            def terminate_all_tests(self):
"""Terminate all running tests."""
                                                                console.print("\n🛑 Terminating all background tests...")

                                                                for test_key, process in self.test_processes.items():
                                                                    if process.poll() is None:
                                                                        config = self.test_configs[test_key]
                                                                        try:
# Terminate process group on Unix
                                                                            if os.name ! = "nt":
                                                                                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                                                                            else:
                                                                                process.terminate()
                                                                                console.print(f" ⏹️ Terminated {config["name"]}")
                                                                                except Exception as e:
                                                                                    console.print(f" ❌ Failed to terminate {config["name"]}: {e}")

# Wait for processes to terminate
                                                                                    time.sleep(2)

# Force kill if needed
                                                                                    for test_key, process in self.test_processes.items():
                                                                                        if process.poll() is None:
                                                                                            try:
                                                                                                process.kill()
                                                                                                console.print(f" ❌ Force killed {test_key}")
                                                                                                except Exception:
                                                                                                    pass

                                                                                                async def launch_consciousness_with_training(self):
"""Launch consciousness chat with background training."""
                                                                                                    console.print("\n" + "=" * 80)
                                                                                                    console.print("🧠 THINK AI - CONSCIOUSNESS WITH BACKGROUND TRAINING")
                                                                                                    console.print("=" * 80 + "\n")

# Ask user what to do
                                                                                                    console.print("Choose an option:")
                                                                                                    console.print("1. Start all tests in background and launch chat")
                                                                                                    console.print("2. Launch chat only (no background tests)")
                                                                                                    console.print("3. Monitor existing background tests")
                                                                                                    console.print("4. Exit")

                                                                                                    choice = Prompt.ask("\nYour choice", choices = ["1", "2", "3", "4"], default = "1")

                                                                                                    if choice = = "4":
                                                                                                        return

                                                                                                    if choice = = "1":
# Start all tests in background
                                                                                                        self.start_all_tests()

# Save process info for later monitoring
                                                                                                        process_info = {
                                                                                                        "start_time": datetime.now().isoformat(),
                                                                                                        "processes": {
                                                                                                        test_key: {
                                                                                                        "pid": proc.pid,
                                                                                                        "script": config["script"],
                                                                                                        "name": config["name"]
                                                                                                        }
                                                                                                        for test_key, proc in self.test_processes.items()
                                                                                                        for config in [self.test_configs[test_key]]
                                                                                                        if proc.poll() is None
                                                                                                        }
                                                                                                        }

                                                                                                        with open("background_tests.json", "w") as f:
                                                                                                            json.dump(process_info, f, indent = 2)

                                                                                                            console.print("\n📊 Process info saved to background_tests.json")
                                                                                                            console.print("💡 Use "python launch_with_background_training.py" and choose option 3 to monitor\n")

                                                                                                            time.sleep(2)

                                                                                                        elif choice = = "3":
# Monitor mode
                                                                                                            try:
                                                                                                                self.start_monitoring()
                                                                                                                input() # Wait for user input
                                                                                                                except KeyboardInterrupt:
                                                                                                                    pass
                                                                                                            finally:
                                                                                                                self.stop_monitoring()
                                                                                                                return

# Launch consciousness chat
                                                                                                            console.print("\n🚀 Launching consciousness chat interface...")
                                                                                                            console.print("💡 Background tests will continue running\n")

# Import here to avoid circular imports

                                                                                                            try:
# Create chat instance
                                                                                                                chat = FullArchitectureChat(enable_cache = True)

# Run the chat
                                                                                                                await chat.run()

                                                                                                                except KeyboardInterrupt:
                                                                                                                    console.print("\n\n👋 Chat session ended")

                                                                                                                    if self.test_processes:
                                                                                                                        console.print("\n⚠️ Background tests are still running!")
                                                                                                                        terminate = Prompt.ask("Terminate all background tests?", choices = ["y", "n"], default = "n")

                                                                                                                        if terminate = = "y":
                                                                                                                            self.terminate_all_tests()
                                                                                                                        else:
                                                                                                                            console.print("✅ Background tests will continue running")
                                                                                                                            console.print("💡 Use option 3 to monitor them later")

                                                                                                                            except Exception as e:
                                                                                                                                console.print(f"\n❌ Error in chat: {e}")
                                                                                                                                logger.error(f"Chat error: {e}", exc_info = True)

                                                                                                                                def signal_handler(signum, frame):
"""Handle shutdown signals."""
                                                                                                                                    console.print("\n🛑 Shutdown signal received...")
                                                                                                                                    sys.exit(0)

                                                                                                                                    async def main():
"""Main entry point."""
# Setup signal handlers
                                                                                                                                        signal.signal(signal.SIGINT, signal_handler)
                                                                                                                                        signal.signal(signal.SIGTERM, signal_handler)

# Create launcher
                                                                                                                                        launcher = BackgroundTrainingLauncher()

# Launch consciousness with training
                                                                                                                                        await launcher.launch_consciousness_with_training()

                                                                                                                                        if __name__ = = "__main__":
# Make script executable
                                                                                                                                            script_path = Path(__file__)
                                                                                                                                            script_path.chmod(0o755)

# Run
                                                                                                                                            asyncio.run(main())
