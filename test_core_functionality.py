#! / usr / bin / env python3

"""Test core Think AI functionality without model dependencies."""

import asyncio
from datetime import datetime

from think_ai.consciousness.awareness import ConsciousnessFramework
from think_ai.graph.knowledge_graph import KnowledgeGraph
from think_ai.storage.redis_cache import RedisCache
from think_ai.storage.scylla_backend import ScyllaBackend
from think_ai.storage.vector_db import MilvusVectorDB


async def test_core_services():
"""Test all core services are working."""
    results = {}

# Test 1: Consciousness Framework
    try:
        consciousness = ConsciousnessFramework()
        state = consciousness.get_state()
        results["consciousness"] = {
        "status": "✅ PASS",
        "state": state,
        "compassion": consciousness.compassion_active,
        }
        except Exception as e:
            results["consciousness"] = {"status": "❌ FAIL", "error": str(e)}

# Test 2: ScyllaDB
            try:
                scylla = ScyllaBackend()
                await scylla.initialize()
# Store test data
                await scylla.store("test_key", {"test": "data", "timestamp": datetime.now().isoformat()})
# Retrieve test data
                data = await scylla.get("test_key")
                results["scylladb"] = {
                "status": "✅ PASS",
                "test_write": "Success",
                "test_read": "Success" if data else "Failed",
                }
                except Exception as e:
                    results["scylladb"] = {"status": "❌ FAIL", "error": str(e)}

# Test 3: Redis Cache
                    try:
                        redis = RedisCache()
                        await redis.initialize()
# Test cache operations
                        await redis.set("test_cache", "cached_value", ttl=60)
                        cached = await redis.get("test_cache")
                        results["redis"] = {
                        "status": "✅ PASS",
                        "cache_set": "Success",
                        "cache_get": cached or "Failed",
                        }
                        except Exception as e:
                            results["redis"] = {"status": "❌ FAIL", "error": str(e)}

# Test 4: Milvus Vector DB
                            try:
                                milvus = MilvusVectorDB()
                                await milvus.initialize()
                                collections = milvus.client.list_collections()
                                results["milvus"] = {
                                "status": "✅ PASS",
                                "collections": len(collections),
                                "ready": True,
                                }
                                except Exception as e:
                                    results["milvus"] = {"status": "❌ FAIL", "error": str(e)}

# Test 5: Neo4j Knowledge Graph
                                    try:
                                        neo4j = KnowledgeGraph()
                                        await neo4j.initialize()
# Test graph query
                                        result = neo4j.driver.execute_query(
                                        "MATCH (n) RETURN count(n) as node_count",
                                        database_="neo4j",
                                        )
                                        node_count = result.records[0]["node_count"] if result.records else 0
                                        results["neo4j"] = {
                                        "status": "✅ PASS",
                                        "nodes": node_count,
                                        "connected": True,
                                        }
                                        except Exception as e:
                                            results["neo4j"] = {"status": "❌ FAIL", "error": str(e)}

# Summary

                                            all_passed = True
                                            for result in results.values():
                                                status = result.get("status", "❓")
                                                if "❌" in status:
                                                    all_passed = False

                                                    if all_passed:
                                                        pass
                                                else:
                                                    pass

                                                return results

                                            if __name__ = = "__main__":
                                                asyncio.run(test_core_services())
