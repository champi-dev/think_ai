#! / usr / bin / env python3

"""Run all Think AI tests in parallel with optimal resource allocation."""

import asyncio
import json
import multiprocessing as mp
import os
import resource
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import psutil
from {config["module"]} import {config["function"]}

from think_ai.utils.logging import get_logger

sys.path.insert(0, str(Path(__file__).parent))

logger = get_logger(__name__)


class ParallelTestOrchestrator:
"""Orchestrate parallel test execution with O(1) resource management."""

    def __init__(self):
# Test configurations with priority weighting
        self.tests = {
        "questions": {
        "module": "test_1000_questions",
        "function": "run_exponential_test",
        "priority": 1.0,
        "cpu_weight": 0.2,
        "memory_weight": 0.2,
        "description": "🧪 Exponential Question Test"
        },
        "coding": {
        "module": "test_1000_coding",
        "function": "run_coding_test",
        "priority": 0.9,
        "cpu_weight": 0.25,
        "memory_weight": 0.25,
        "description": "💻 Exponential Coding Test"
        },
        "philosophy": {
        "module": "test_1000_philosophy",
        "function": "run_philosophical_test",
        "priority": 0.8,
        "cpu_weight": 0.15,
        "memory_weight": 0.15,
        "description": "🧘 Philosophical Depth Test"
        },
        "self_training": {
        "module": "test_1000_self_training",
        "function": "run_self_training_test",
        "priority": 1.0,
        "cpu_weight": 0.2,
        "memory_weight": 0.2,
        "description": "🧠 Self - Training Evolution Test"
        },
        "knowledge_creation": {
        "module": "test_1000_knowledge_creation",
        "function": "run_knowledge_creation_test",
        "priority": 0.9,
        "cpu_weight": 0.2,
        "memory_weight": 0.2,
        "description": "🌌 Knowledge Creation Test"
        }
        }

# System resource limits
        self.total_cpus = mp.cpu_count()
        self.total_memory_gb = psutil.virtual_memory().total / (1024 * * 3)
        self.reserved_memory_gb = 2.0  # Reserve for system
        self.available_memory_gb = self.total_memory_gb - self.reserved_memory_gb

# Process tracking
        self.processes = {}
        self.start_time = None
        self.shutdown_requested = False

        def calculate_resource_allocation(self) - > Dict[str, Dict[str, float]]:
"""Calculate optimal resource allocation with O(1) complexity."""
            allocations = {}

# Calculate total weights
            total_cpu_weight = sum(test["cpu_weight"] for test in self.tests.values())
            total_memory_weight = sum(test["memory_weight"]
            for test in self.tests.values())

# Allocate resources proportionally
            for name, config in self.tests.items():
                allocations[name] = {
                "cpu_cores": max(1, int(self.total_cpus * config["cpu_weight"] / total_cpu_weight)),
                "memory_gb": self.available_memory_gb * config["memory_weight"] / total_memory_weight,
                "priority": config["priority"]
                }

                return allocations

            async def run_test_subprocess(self, test_name: str, config: Dict[str, Any],
            allocation: Dict[str, float]) - > Dict[str, Any]:
"""Run a test in a subprocess with resource limits."""
                print(f"\n🚀 Starting {config["description"]}")
                print(
                f" 📊 Allocated: {
                allocation["cpu_cores"]} CPUs, {
                allocation["memory_gb"]:.1f}GB RAM")

# Create subprocess command
                cmd = [
                sys.executable,
                "-c",
                f"""
                sys.path.insert(0, "{Path(__file__).parent}")

# Set memory limit
                resource.setrlimit(resource.RLIMIT_AS, ({int(allocation["memory_gb"] * 1024 * 1024 * 1024)}, - 1))

# Run test
                asyncio.run({config["function"]}(keep_data = True))
"""
                ]

# Start subprocess
                start_time = time.time()
                try:
                    process = await asyncio.create_subprocess_exec(
                    * cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
# Set CPU affinity if supported
                    preexec_fn=lambda: os.sched_setaffinity(
                    0, range(allocation["cpu_cores"]))
                    if hasattr(os, "sched_setaffinity") else None
                    )

                    self.processes[test_name] = process

# Wait for completion or interruption
                    stdout, stderr = await process.communicate()

                    runtime = time.time() - start_time

                    return {
                "test": test_name,
                "status": "completed" if process.returncode = = 0 else "failed",
                "runtime": runtime,
                "return_code": process.returncode,
                "stdout_lines": len(stdout.decode().split("\n")) if stdout else 0,
                "stderr": stderr.decode() if stderr and process.returncode ! = 0 else None
                }

                except Exception as e:
                    return {
                "test": test_name,
                "status": "error",
                "runtime": time.time() - start_time,
                "error": str(e)
                }

                async def monitor_system_resources(self):
"""Monitor system resources with O(1) sampling."""
                    monitor_interval = 10  # seconds

                    while not self.shutdown_requested:
                        try:
                            cpu_percent = psutil.cpu_percent(interval=1)
                            memory = psutil.virtual_memory()

# Show system status
                            status = (
                            f"\r📊 System Status | "
                            f"CPU: {cpu_percent:.1f}% | "
                            f"RAM: {memory.percent:.1f}% ({memory.used / (1024**3):.1f}GB used) | "
                            f"Active Tests: {len([p for p in self.processes.values() if p and p.returncode is None])} | "
                            f"Runtime: {time.time() - self.start_time:.0f}s"
                            )
                            print(status + " " * 20, end="", flush=True)

                            await asyncio.sleep(monitor_interval)

                            except Exception as e:
                                logger.error(f"Monitor error: {e}")
                                await asyncio.sleep(monitor_interval)

                                async def run_all_tests_parallel(self, keep_data: bool = True):
"""Run all tests in parallel with optimal resource allocation."""
                                    print("\n" + "=" * 80)
                                    print("🚀 THINK AI PARALLEL TEST ORCHESTRATOR")
                                    print("=" * 80 + "\n")

                                    self.start_time = time.time()

# Calculate resource allocations
                                    allocations = self.calculate_resource_allocation()

                                    print(
                                    f"💻 System Resources: {
                                    self.total_cpus} CPUs, {
                                    self.total_memory_gb:.1f}GB RAM")
                                    print(f"📊 Running {len(self.tests)} tests in parallel\n")

# Start resource monitor
                                    monitor_task = asyncio.create_task(self.monitor_system_resources())

# Launch all tests concurrently
                                    test_tasks = []
                                    for test_name, config in self.tests.items():
                                        allocation = allocations[test_name]
                                        task = asyncio.create_task(
                                        self.run_test_subprocess(test_name, config, allocation)
                                        )
                                        test_tasks.append(task)

# Small delay to avoid resource contention at startup
                                        await asyncio.sleep(0.5)

                                        print(f"\n✅ All {len(test_tasks)} tests launched!\n")
                                        print("🔧 Press Ctrl + C to gracefully shutdown all tests\n")

# Wait for all tests to complete
                                        try:
                                            results = await asyncio.gather(* test_tasks, return_exceptions=True)
                                            except KeyboardInterrupt:
                                                print("\n\n🛑 Shutdown requested - terminating all tests...")
                                                self.shutdown_requested = True

# Terminate all processes
                                                for test_name, process in self.processes.items():
                                                    if process and process.returncode is None:
                                                        process.terminate()
                                                        print(f" ⏹️ Terminating {test_name}")

# Wait for graceful shutdown
                                                        await asyncio.sleep(2)

# Force kill if needed
                                                        for test_name, process in self.processes.items():
                                                            if process and process.returncode is None:
                                                                process.kill()
                                                                print(f" ❌ Force killing {test_name}")

                                                                results = []

# Cancel monitor
                                                                monitor_task.cancel()
                                                                try:
                                                                    await monitor_task
                                                                    except asyncio.CancelledError:
                                                                        pass

# Display final results
                                                                    total_runtime = time.time() - self.start_time

                                                                    print("\n\n" + "=" * 80)
                                                                    print("📊 PARALLEL TEST RESULTS")
                                                                    print("=" * 80 + "\n")

                                                                    print(f"⏱️ Total Runtime: {total_runtime / 3600:.2f} hours\n")

                                                                    if results:
                                                                        success_count = sum(
                                                                        1 for r in results if isinstance(
                                                                        r, dict) and r.get("status") == "completed")

                                                                        print(f"✅ Successful: {success_count}/{len(results)}")
                                                                        print(f"❌ Failed: {len(results) - success_count}\n")

                                                                        print("📋 Individual Test Results:")
                                                                        for result in results:
                                                                            if isinstance(result, dict):
                                                                                status_icon = "✅" if result["status"] = = "completed" else "❌"
                                                                                print(f" {status_icon} {result["test"]}: {result["status"]} "
                                                                                f"(runtime: {result["runtime"]/3600:.2f}h)")
                                                                                if result.get("error"):
                                                                                    print(f" Error: {result["error"]}")

# Save summary
                                                                                    if keep_data:
                                                                                        summary = {
                                                                                        "test_date": datetime.now().isoformat(),
                                                                                        "total_runtime_hours": total_runtime / 3600,
                                                                                        "system_info": {
                                                                                        "cpus": self.total_cpus,
                                                                                        "memory_gb": self.total_memory_gb
                                                                                        },
                                                                                        "resource_allocations": allocations,
                                                                                        "results": results if results else []
                                                                                        }

                                                                                        filename = f"parallel_test_summary_{
                                                                                        datetime.now().strftime("%Y%m%d_%H%M%S")}.json"
                                                                                        with open(filename, "w") as f:
                                                                                            json.dump(summary, f, indent=2)

                                                                                            print(f"\n💾 Summary saved to: {filename}")

                                                                                            print("\n✅ Parallel test execution complete!")

                                                                                            def signal_handler(signum, frame):
"""Handle shutdown signals gracefully."""
                                                                                                print("\n🛑 Shutdown signal received...")
                                                                                                sys.exit(0)

                                                                                                async def main():
"""Main entry point."""
# Setup signal handlers
                                                                                                    signal.signal(signal.SIGINT, signal_handler)
                                                                                                    signal.signal(signal.SIGTERM, signal_handler)

# Parse arguments
                                                                                                    keep_data = "--keep - data" in sys.argv

# Run parallel tests
                                                                                                    orchestrator = ParallelTestOrchestrator()
                                                                                                    await orchestrator.run_all_tests_parallel(keep_data)

                                                                                                    if __name__ = = "__main__":
# Set multiprocessing start method
                                                                                                        mp.set_start_method("spawn", force=True)

# Run async main
                                                                                                        asyncio.run(main())
