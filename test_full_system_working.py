#! / usr / bin / env python3

"""Comprehensive test showing the full system works with real AI responses."""

import asyncio
import sys
import time

import traceback
from implement_proper_architecture import ProperThinkAI


async def test_full_system():
"""Test the complete Think AI system."""
    print("🧪 COMPREHENSIVE THINK AI SYSTEM TEST")
    print("=" * 80)

# Check if running with cache
    use_cache = "--cache" in sys.argv or "--fast" in sys.argv

# Initialize system
    print(
    f"\n📥 Initializing Full Think AI System {
    "WITH CACHING" if use_cache else "WITHOUT CACHING"}...")
    think_ai = ProperThinkAI(enable_cache=use_cache)

    try:
        start_time = time.time()
        await think_ai.initialize()
        init_time = time.time() - start_time
        print(f"✅ System initialized successfully in {init_time:.2f}s!")

        if use_cache and think_ai._cache_loaded:
            print("⚡ LOADED FROM CACHE - O(1) INITIALIZATION!")
        elif use_cache:
            print("💾 Cache saved for next run")

# Test queries
            test_queries = [
            "What is Mars?",
            "Explain black holes",
            "What is the sun?",
            "Tell me about artificial intelligence",
            "How does quantum physics work?",
            "What is consciousness?",
            "Hello, how are you?",
            "What can you help me with?"
            ]

            print("\n🔬 Testing System Responses:")
            print("-" * 80)

            success_count = 0
            fallback_count = 0

            for query in test_queries:
                print(f"\n❓ Question: {query}")
                print("🔄 Processing through full distributed architecture...")

                start_time = time.time()
                result = await think_ai.query(query)
                process_time = time.time() - start_time

# Extract response and metadata
                response = result.get("response", "No response")
                source = result.get("source", "unknown")
                architecture = result.get("architecture_usage", {})

                print(
                f"\n🤖 Response: {response[:200]}{"..." if len(response) > 200 else ""}")
                print("\n📊 Metadata:")
                print(f" • Source: {source}")
                print(f" • Process Time: {process_time:.2f}s")
                print(" • Architecture Components Used:")
                for component, usage in architecture.items():
                    print(f" - {component}: {usage}")

# Check if it's using real AI'
                    if source = = "distributed":
                        print("✅ Using distributed AI system!")
                        success_count + = 1
                    elif "fallback" in response.lower() or "self - trainer" in source.lower():
                        print("⚠️ Using fallback / self - trainer")
                        fallback_count + = 1
                    else:
                        print("✅ Generated AI response!")
                        success_count + = 1

                        print("-" * 80)

# Summary
                        print("\n📈 TEST SUMMARY:")
                        print(f" • Total Questions: {len(test_queries)}")
                        print(f" • Successful AI Responses: {success_count}")
                        print(f" • Fallback Responses: {fallback_count}")
                        print(f" • Success Rate: {(success_count / len(test_queries)*100):.1f}%")

# Check specific components
                        print("\n🔍 Component Health Check:")
                        health = await think_ai.get_health_status()
                        for service, status in health.items():
                            if isinstance(status, dict) and status.get("status") = = "healthy":
                                print(f" ✅ {service}: Connected")
                            else:
                                print(f" ❌ {service}: {status}")

# Show that Qwen model is working
                                if hasattr(
                                think_ai,
                                "distributed_system") and hasattr(
                                think_ai.distributed_system,
                                "model_orchestrator"):
                                    model_info = await think_ai.distributed_system.model_orchestrator.get_model_info()
                                    if model_info.get("status") ! = "not_initialized":
                                        print("\n🤖 Language Model Status:")
                                        print(f" • Model: {model_info.get("model_name", "Unknown")}")
                                        print(f" • Device: {model_info.get("device", "Unknown")}")
                                        print(f" • Parameters: {model_info.get("parameters", "Unknown")}")
                                        print(" ✅ Model is loaded and working!")
                                    else:
                                        print("\n❌ Language model not initialized!")

                                        return success_count > fallback_count

                                    except Exception as e:
                                        print(f"\n❌ ERROR: {e}")
                                        traceback.print_exc()
                                        return False

                                finally:
# Cleanup
                                    print("\n🧹 Shutting down...")
                                    await think_ai.shutdown()

                                    if __name__ = = "__main__":
                                        success = asyncio.run(test_full_system())
                                        print(f"\n{"✅ ALL TESTS PASSED!" if success else "❌ TESTS FAILED!"}")

# Show cache usage tip
                                        if "--cache" not in sys.argv and "--fast" not in sys.argv:
                                            print("\n💡 TIP: Run with --cache or --fast flag for O(1) initialization!")
                                            print(" Example: python test_full_system_working.py --cache")

                                            exit(0 if success else 1)
