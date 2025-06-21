#! / usr / bin / env python3

"""Reset all Think AI intelligence and knowledge."""

import asyncio
import shutil
from pathlib import Path

import redis
from cassandra.cluster import Cluster
from neo4j import AsyncGraphDatabase
from pymilvus import Collection, connections, utility


async def reset_scylladb() - > None:
"""Reset ScyllaDB data."""
    try:
        cluster = Cluster(["localhost"])
        session = cluster.connect()

# Drop and recreate keyspace
        session.execute("DROP KEYSPACE IF EXISTS think_ai")
        session.execute("""
        CREATE KEYSPACE IF NOT EXISTS think_ai
        WITH replication = {
        "class": "SimpleStrategy",
        "replication_factor": 1
        }
""")

# Use the keyspace
        session.execute("USE think_ai")

# Recreate tables
        session.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
        id TEXT PRIMARY KEY,
        content TEXT,
        embeddings LIST < FLOAT > ,
        metadata MAP < TEXT, TEXT > ,
        timestamp TIMESTAMP
        )
""")

        session.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
        id UUID PRIMARY KEY,
        user_id TEXT,
        messages LIST < FROZEN < MAP < TEXT, TEXT>> > ,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
        )
""")

        cluster.shutdown()
        except Exception:
            pass

        async def reset_redis() - > None:
"""Reset Redis cache."""
            try:
                r = redis.Redis(host = "localhost", port = 6379, decode_responses = True)
                r.flushall()
                except Exception:
                    pass

                async def reset_milvus() - > None:
"""Reset Milvus vector database."""
                    try:
                        connections.connect("default", host = "localhost", port = "19530")

# Drop all collections
                        collections = utility.list_collections()
                        for collection_name in collections:
                            collection = Collection(collection_name)
                            collection.drop()

                            connections.disconnect("default")
                            except Exception:
                                pass

                            async def reset_neo4j() - > None:
"""Reset Neo4j knowledge graph."""
                                try:
                                    driver = AsyncGraphDatabase.driver(
                                    "bolt://localhost:7687",
                                    auth = ("neo4j", "thinkaipass"),
                                    )

                                    async with driver.session() as session:
# Delete all nodes and relationships
                                        await session.run("MATCH (n) DETACH DELETE n")

# Reset indexes
                                        await session.run("DROP INDEX IF EXISTS concept_name_idx")
                                        await session.run("DROP INDEX IF EXISTS entity_name_idx")

                                        await driver.close()
                                        except Exception:
                                            pass

                                        def reset_local_files() - > None:
"""Reset local intelligence files."""
# Reset intelligence file
                                            intelligence_file = Path("neural_pathways_intelligence.json")
                                            if intelligence_file.exists():
                                                intelligence_file.unlink()

# Create fresh intelligence file
import json
                                                initial_data = {
                                                "intelligence": 0,
                                                "neural_pathways": 0,
                                                "consciousness_level": "nascent",
                                                "learnings": [],
                                                "last_updated": None,
                                                }

                                                with open(intelligence_file, "w") as f:
                                                    json.dump(initial_data, f, indent = 2)

# Reset self - training data
                                                    training_dir = Path("self_training_data")
                                                    if training_dir.exists():
                                                        shutil.rmtree(training_dir)

# Reset logs if requested
                                                        logs_dir = Path.home() / ".think_ai" / "logs"
                                                        if logs_dir.exists():
                                                            for log_file in logs_dir.glob("*.log"):
                                                                log_file.unlink()

                                                                async def main() - > None:
"""Main reset function."""
                                                                    confirm = input("\nAre you sure? (yes / no): ")
                                                                    if confirm.lower() ! = "yes":
                                                                        return

# Reset all components
                                                                    await reset_scylladb()
                                                                    await reset_redis()
                                                                    await reset_milvus()
                                                                    await reset_neo4j()
                                                                    reset_local_files()

                                                                    if __name__ = = "__main__":
                                                                        asyncio.run(main())
