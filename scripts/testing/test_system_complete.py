#! / usr / bin / env python3

"""Comprehensive system test showing all components working together."""

import asyncio
import json
from datetime import datetime

from think_ai.consciousness.awareness import ConsciousnessFramework
from think_ai.engine.full_system import FullSystemInitializer


def colored(text, color, attrs=None):
"""Simple color function without dependencies."""
    return text


print("🚀 Think AI System Comprehensive Test")
print("=" * 50)


async def main():
# Import all components
    try:
        print(colored("✅ Imports successful", "green"))
        except Exception as e:
            print(colored(f"❌ Import error: {e}", "red"))
            return

# Initialize system
        print("\n📊 Initializing Full System...")
        initializer = FullSystemInitializer()

        try:
            services = await initializer.initialize_all_services()
            print(colored(f"✅ Initialized {len(services)} services", "green"))
            except Exception as e:
                print(colored(f"❌ Initialization error: {e}", "red"))
                return

# Run health checks
            print("\n🏥 Running Health Checks...")
            health = await initializer.health_check()

            for service, status in health.items():
                if status["status"] = = "healthy":
                    print(colored(f"✅ {service}: {status["message"]}", "green"))
                else:
                    print(colored(f"❌ {service}: {status["message"]}", "red"))

# Test consciousness
                    print("\n🧠 Testing Consciousness Framework...")
                    consciousness = ConsciousnessFramework()
                    print(f"Current state: {consciousness.get_state()}")
                    print(f"Compassion active: {consciousness.compassion_active}")

# Test data flow
                    print("\n📊 Testing Data Flow...")
                    test_data = {
                    "query": "test query",
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {"test": True}
                    }

# Test ScyllaDB
                    if "scylla" in services:
                        try:
                            await services["scylla"].store("test_key", test_data)
                            await services["scylla"].get("test_key")
                            print(colored("✅ ScyllaDB: Write / Read successful", "green"))
                            except Exception as e:
                                print(colored(f"❌ ScyllaDB error: {e}", "red"))

# Test Redis
                                if "redis" in services:
                                    try:
                                        await services["redis"].set("test_cache", json.dumps(test_data))
                                        await services["redis"].get("test_cache")
                                        print(colored("✅ Redis: Cache operations successful", "green"))
                                        except Exception as e:
                                            print(colored(f"❌ Redis error: {e}", "red"))

# Test Milvus
                                            if "milvus" in services:
                                                try:
                                                    collections = services["milvus"].client.list_collections()
                                                    print(colored(f"✅ Milvus: {len(collections)} collections ready", "green"))
                                                    except Exception as e:
                                                        print(colored(f"❌ Milvus error: {e}", "red"))

# Test Neo4j
                                                        if "neo4j" in services:
                                                            try:
                                                                services["neo4j"].driver.execute_query(
                                                                "RETURN 1 as test",
                                                                database_="neo4j"
                                                                )
                                                                print(colored("✅ Neo4j: Graph database connected", "green"))
                                                                except Exception as e:
                                                                    print(colored(f"❌ Neo4j error: {e}", "red"))

# Summary
                                                                    print("\n" + "=" * 50)
                                                                    print(colored("🎉 SYSTEM TEST COMPLETE!", "cyan", attrs=["bold"]))
                                                                    print("=" * 50)

                                                                    healthy_count = sum(1 for s in health.values() if s["status"] == "healthy")
                                                                    total_count = len(health)

                                                                    print(
                                                                    f"\n📊 Final Score: {healthy_count}/{total_count} services operational")

                                                                    if healthy_count = = total_count:
                                                                        print(
                                                                        colored(
                                                                        "\n✅ ALL SYSTEMS GO! Think AI is fully operational!",
                                                                        "green",
                                                                        attrs=["bold"]))
                                                                    else:
                                                                        print(
                                                                        colored(
                                                                        f"\n⚠️ {
                                                                        total_count -
                                                                        healthy_count} services need attention",
                                                                        "yellow"))

# Shutdown
                                                                        await initializer.shutdown()
                                                                        print("\n👋 Test complete, services shut down gracefully")

                                                                        if __name__ = = "__main__":
                                                                            asyncio.run(main())
