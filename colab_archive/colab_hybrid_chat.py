#!/usr/bin/env python3

"""Hybrid chat that uses available services (Redis + Neo4j) in Colab
Falls back to local storage for Cassandra and Milvus.
"""

import asyncio
import sys
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

from full_architecture_chat import FullArchitectureChat
from implement_proper_architecture import ProperThinkAI

sys.path.insert(0, str(Path(__file__).parent))

# Patch imports before loading the main module


# Mock Cassandra
class MockCassandraCluster:
    def connect(self, keyspace=None):
        return MockCassandraSession()


class MockCassandraSession:
    def __init__(self) -> None:
        self.data = {}

    def execute(self, query, params=None):
        # Simple in-memory storage
        if "CREATE" in query:
            return []
        if "INSERT" in query:
            if params:
                self.data[params[0]] = params
            return []
        if "SELECT" in query:
            return list(self.data.values())
        return []

    def prepare(self, query):
        return query


# Mock Milvus
class MockMilvusConnection:
    def __init__(self, *args, **kwargs) -> None:
        self.collections = {}

    def create_collection(self, name, fields, **kwargs) -> None:
        self.collections[name] = {"fields": fields, "data": []}

    def has_collection(self, name):
        return name in self.collections

    def get_collection(self, name):
        return MockCollection(name, self.collections.get(name, {}))


class MockCollection:
    def __init__(self, name, data) -> None:
        self.name = name
        self.data = data

    def insert(self, data):
        self.data.get("data", []).append(data)
        return {"insert_count": len(data)}

    def search(self, *args, **kwargs):
        # Return empty results
        return [[]]


# Apply patches

mock_cassandra = type(sys)("cassandra")
mock_cassandra.cluster = type(sys)("cluster")
mock_cassandra.cluster.Cluster = MockCassandraCluster
mock_cassandra.cluster.Session = MockCassandraSession
sys.modules["cassandra"] = mock_cassandra
sys.modules["cassandra.cluster"] = mock_cassandra.cluster

mock_pymilvus = type(sys)("pymilvus")
mock_pymilvus.connections = type(sys)("connections")
mock_pymilvus.connections.connect = lambda *args, **kwargs: None
mock_pymilvus.Collection = MockCollection
mock_pymilvus.utility = type(sys)("utility")
mock_pymilvus.utility.has_collection = lambda name: False
sys.modules["pymilvus"] = mock_pymilvus

# Now import the actual architecture

console = Console()


class HybridChat(FullArchitectureChat):
    """Chat that uses available services and mocks missing ones."""

    def __init__(self) -> None:
        # Skip parent init to control service initialization
        self.think_ai = None
        self.intelligence_level = 0
        self.neural_pathways = 0
        self.current_thought = "Initializing hybrid mode..."
        self.thought_count = 0
        self.name = None
        self.initialized = False
        self.conversation_context = []

    async def initialize_hybrid(self) -> None:
        """Initialize with available services."""
        console.print("\n🔧 Initializing Hybrid Mode...", style="yellow")
        console.print(
            "✅ Using: Redis (cache) + Neo4j (knowledge graph)", style="green"
        )
        console.print("🔄 Mocking: ScyllaDB + Milvus", style="yellow")

        # Initialize with custom config
        self.think_ai = ProperThinkAI(enable_cache=True)

        # Override service initialization
        self.think_ai.services = {
            "redis": self.think_ai.services.get("redis"),  # Keep Redis
            "neo4j": self.think_ai.services.get("neo4j"),  # Keep Neo4j
            "scylla": MockCassandraSession(),  # Mock Cassandra
            "milvus": MockMilvusConnection(),  # Mock Milvus
        }

        self.initialized = True
        console.print("✅ Hybrid mode ready!", style="green")


async def main() -> None:
    """Run hybrid chat."""
    chat = HybridChat()
    await chat.initialize_hybrid()

    console.print("\n🧠 [bold cyan]THINK AI - HYBRID MODE[/bold cyan]")
    console.print("Using Redis + Neo4j with local fallbacks")
    console.print("Type 'exit' to quit, 'help' for commands\n")

    while True:
        try:
            user_input = Prompt.ask("\n[bold green]You[/bold green]")

            if user_input.lower() == "exit":
                break
            if user_input.lower() == "help":
                console.print("\nCommands:", style="yellow")
                console.print("- exit: Quit the chat")
                console.print("- help: Show this help")
                continue

            # Process with hybrid system
            response = await chat.think_ai.process_with_consciousness(user_input)

            console.print(f"\n[bold blue]Think AI[/bold blue]: {response}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            console.print("Continuing with fallback mode...")

    console.print("\n👋 Goodbye!", style="yellow")


if __name__ == "__main__":
    asyncio.run(main())
