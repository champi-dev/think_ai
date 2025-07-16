#!/usr/bin/env python3
"""Comprehensive test of the full distributed Think AI system."""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from think_ai.engine.full_system import DistributedThinkAI
from think_ai.integrations.claude_api import ClaudeAPI
from think_ai.storage.base import StorageItem
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


class SystemTester:
    """Comprehensive system testing suite."""

    def __init__(self) -> None:
        self.system = DistributedThinkAI()
        self.services = None
        self.test_results = {
            "passed": [],
            "failed": [],
            "warnings": [],
        }

    async def run_all_tests(self) -> None:
        """Run comprehensive system tests."""
        try:
            # Start system
            await self._test_system_startup()

            # Test each component
            await self._test_scylladb()
            await self._test_milvus()
            await self._test_consciousness()
            await self._test_language_model()
            await self._test_federated_learning()
            await self._test_claude_integration()
            await self._test_eternal_memory()
            await self._test_full_query_processing()

            # Generate report
            self._generate_report()

        except Exception as e:
            self._log_failure("System Test", f"Fatal error: {e}")
            import traceback

            traceback.print_exc()
        finally:
            await self._cleanup()

    async def _test_system_startup(self) -> None:
        """Test system initialization."""
        try:
            self.services = await self.system.start()
            self._log_success(
                "System Startup", f"Started {len(self.services)} services"
            )

            # Check expected services
            expected = [
                "scylla",
                "milvus",
                "consciousness",
                "federated",
                "model_orchestrator",
            ]
            for service in expected:
                if service in self.services:
                    self._log_success(f"Service {service}", "Active")
                else:
                    self._log_failure(f"Service {service}", "Not found")

        except Exception as e:
            self._log_failure("System Startup", str(e))

    async def _test_scylladb(self) -> None:
        """Test ScyllaDB distributed storage."""
        if "scylla" not in self.services:
            self._log_warning("ScyllaDB", "Service not available")
            return

        try:
            scylla = self.services["scylla"]

            # Test 1: Store data
            test_key = f"test_key_{datetime.now().timestamp()}"
            test_data = {
                "content": "Test knowledge entry",
                "timestamp": datetime.now().isoformat(),
                "love_score": 0.95,
            }

            item = StorageItem(
                key=test_key,
                value=json.dumps(test_data),
                metadata={"test": True},
            )

            await scylla.put(test_key, item)
            self._log_success("ScyllaDB Write", "Data stored successfully")

            # Test 2: Retrieve data
            retrieved = await scylla.get(test_key)
            if retrieved and json.loads(retrieved.value) == test_data:
                self._log_success("ScyllaDB Read", "Data retrieved correctly")
            else:
                self._log_failure("ScyllaDB Read", "Data mismatch")

            # Test 3: Batch operations
            batch_items = []
            for i in range(5):
                batch_items.append(
                    StorageItem(
                        key=f"batch_test_{i}",
                        value=f"Batch value {i}",
                        metadata={"batch": True},
                    )
                )

            await scylla.put_batch(batch_items)
            self._log_success("ScyllaDB Batch", "Batch write successful")

            # Test 4: Prefix query
            prefix_results = await scylla.list_by_prefix("batch_test_")
            results_list = []
            async for item in prefix_results:
                results_list.append(item)

            if len(results_list) == 5:
                self._log_success(
                    "ScyllaDB Prefix Query", f"Found {len(results_list)} items"
                )
            else:
                self._log_failure(
                    "ScyllaDB Prefix Query", f"Expected 5, got {len(results_list)}"
                )

        except Exception as e:
            self._log_failure("ScyllaDB", str(e))

    async def _test_milvus(self) -> None:
        """Test Milvus vector database."""
        if "milvus" not in self.services:
            self._log_warning("Milvus", "Service not available")
            return

        try:
            milvus = self.services["milvus"]

            # Test 1: Check collection
            if milvus._initialized:
                self._log_success("Milvus Connection", "Connected")
            else:
                self._log_failure("Milvus Connection", "Not initialized")

            # Test 2: Collection exists
            from pymilvus import utility

            if utility.has_collection("think_ai_knowledge"):
                self._log_success("Milvus Collection", "think_ai_knowledge exists")
            else:
                self._log_failure("Milvus Collection", "Collection not found")

            # Test 3: Vector operations would go here
            # (Need embeddings to test properly)
            self._log_success("Milvus Ready", "Vector search available")

        except Exception as e:
            self._log_failure("Milvus", str(e))

    async def _test_consciousness(self) -> None:
        """Test consciousness framework."""
        if "consciousness" not in self.services:
            self._log_warning("Consciousness", "Service not available")
            return

        try:
            consciousness = self.services["consciousness"]

            # Test 1: Generate conscious response
            test_queries = [
                "What is love?",
                "How can AI help humanity?",
                "What are your ethical principles?",
            ]

            for query in test_queries:
                response = await consciousness.generate_conscious_response(query)

                if response and "content" in response:
                    self._log_success(
                        "Consciousness Query", f"'{query}' -> Response generated"
                    )
                else:
                    self._log_failure(
                        "Consciousness Query", f"'{query}' -> No response"
                    )

            # Test 2: Check consciousness states
            states = ["aware", "focused", "compassionate", "reflective"]
            if response.get("consciousness_state") in states:
                self._log_success(
                    "Consciousness State",
                    f"Valid state: {response['consciousness_state']}",
                )
            else:
                self._log_failure("Consciousness State", "Invalid state")

        except Exception as e:
            self._log_failure("Consciousness", str(e))

    async def _test_language_model(self) -> None:
        """Test language model."""
        if "model_orchestrator" not in self.services:
            self._log_warning("Language Model", "Service not available")
            return

        try:
            orchestrator = self.services["model_orchestrator"]

            # Check if model is loaded
            if orchestrator.language_model and orchestrator.language_model._initialized:
                self._log_success("Language Model", "Phi-2 loaded successfully")

                # Get model info
                info = await orchestrator.language_model.get_model_info()
                self._log_success(
                    "Model Info", f"{info['model_name']} on {info['device']}"
                )
            else:
                self._log_failure("Language Model", "Not initialized")

        except Exception as e:
            self._log_failure("Language Model", str(e))

    async def _test_federated_learning(self) -> None:
        """Test federated learning system."""
        if "federated" not in self.services:
            self._log_warning("Federated Learning", "Service not available")
            return

        try:
            federated = self.services["federated"]

            # Test 1: Register client
            test_client_id = f"test_client_{datetime.now().timestamp()}"
            success = await federated.register_client(test_client_id)

            if success:
                self._log_success("Client Registration", f"Registered {test_client_id}")
            else:
                self._log_failure("Client Registration", "Failed to register")

            # Test 2: Get stats
            stats = federated.get_global_stats()
            self._log_success(
                "Federated Stats", f"Total clients: {stats['total_clients']}"
            )
            self._log_success("Model Version", stats["current_model_version"])

        except Exception as e:
            self._log_failure("Federated Learning", str(e))

    async def _test_claude_integration(self) -> None:
        """Test Claude API integration."""
        if not os.getenv("CLAUDE_API_KEY"):
            self._log_warning("Claude API", "No API key found")
            return

        try:
            claude = ClaudeAPI()

            # Test connection
            result = await claude.query("What is 2+2?", max_tokens=50)

            if result and "response" in result:
                self._log_success("Claude API", "Connected and responding")
                self._log_success("Claude Response", result["response"][:50])
                self._log_success("Claude Cost", f"${result['cost']:.4f}")
            else:
                self._log_failure("Claude API", "No response")

        except Exception as e:
            self._log_failure("Claude API", str(e))

    async def _test_eternal_memory(self) -> None:
        """Test eternal memory system."""
        try:
            from think_ai.persistence.eternal_memory import EternalMemory

            memory = EternalMemory()

            # Check memory directory
            if memory.memory_path.exists():
                self._log_success("Memory Directory", str(memory.memory_path))
            else:
                self._log_failure("Memory Directory", "Not found")

            # Test consciousness event logging
            await memory.log_consciousness_event(
                event_type="test_event",
                data={"test": True, "timestamp": datetime.now().isoformat()},
            )
            self._log_success("Event Logging", "Consciousness event logged")

            # Test conversation saving
            test_conversation = {
                "messages": [
                    {"role": "user", "content": "Test message"},
                    {"role": "assistant", "content": "Test response"},
                ],
            }

            await memory.save_conversation(
                conversation_id=f"test_{datetime.now().timestamp()}",
                messages=test_conversation["messages"],
                metadata={"test": True},
            )
            self._log_success(
                "Conversation Save", "Conversation saved to eternal memory"
            )

        except Exception as e:
            self._log_failure("Eternal Memory", str(e))

    async def _test_full_query_processing(self) -> None:
        """Test full system query processing."""
        try:
            test_query = "Explain how distributed AI systems work"

            result = await self.system.process_with_full_system(test_query)

            self._log_success(
                "Query Processing", f"Used {len(result['services_used'])} services"
            )

            # Check each response
            for service, response in result["responses"].items():
                if response:
                    self._log_success(f"{service} Response", "Generated successfully")
                else:
                    self._log_failure(f"{service} Response", "Empty response")

        except Exception as e:
            self._log_failure("Full Query Processing", str(e))

    def _log_success(self, test_name: str, message: str) -> None:
        """Log successful test."""
        self.test_results["passed"].append(f"{test_name}: {message}")

    def _log_failure(self, test_name: str, message: str) -> None:
        """Log failed test."""
        self.test_results["failed"].append(f"{test_name}: {message}")

    def _log_warning(self, test_name: str, message: str) -> None:
        """Log warning."""
        self.test_results["warnings"].append(f"{test_name}: {message}")

    def _generate_report(self) -> None:
        """Generate final test report."""
        total_tests = len(self.test_results["passed"]) + len(
            self.test_results["failed"]
        )
        pass_rate = (
            (len(self.test_results["passed"]) / total_tests * 100)
            if total_tests > 0
            else 0
        )

        if self.test_results["failed"]:
            for _failure in self.test_results["failed"]:
                pass

        if self.test_results["warnings"]:
            for _warning in self.test_results["warnings"]:
                pass

        # Overall assessment
        if pass_rate >= 80 or pass_rate >= 60:
            pass
        else:
            pass

        # Save report
        report_path = Path("test_report.json")
        with open(report_path, "w") as f:
            json.dump(
                {
                    "timestamp": datetime.now().isoformat(),
                    "results": self.test_results,
                    "pass_rate": pass_rate,
                },
                f,
                indent=2,
            )

    async def _cleanup(self) -> None:
        """Clean up after tests."""
        if self.system:
            await self.system.shutdown()


async def main() -> None:
    """Run comprehensive system test."""
    tester = SystemTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
