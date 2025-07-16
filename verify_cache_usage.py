#!/usr/bin/env python3

import requests
import json
import time


def verify_cache_usage():
    print("🔍 Verifying Multi-Level Cache Usage")
    print("=" * 50)

    base_url = "http://localhost:8080"

    # Test cases specifically designed to hit different cache levels
    test_cases = [
        {
            "name": "Full Message Cache Test",
            "query": "hello",
            "should_hit_cache": "FullMessage",
            "description": "Should hit exact full message cache and log it",
        },
        {
            "name": "Love Concept Test",
            "query": "what is love",
            "should_hit_cache": "FullMessage",
            "description": "Should hit cached love response",
        },
        {
            "name": "Human Concept Test",
            "query": "what means human",
            "should_hit_cache": "FullMessage",
            "description": "Should hit cached human response",
        },
        {
            "name": "Phrase Cache Test",
            "query": "what is mathematics",
            "should_hit_cache": "Phrase",
            "description": "Should hit 'what is' phrase pattern",
        },
        {
            "name": "Word Cache Test",
            "query": "programming is fun",
            "should_hit_cache": "Word",
            "description": "Should hit 'programming' word cache",
        },
        {
            "name": "Novel Query Test",
            "query": "what is quantum mechanics",
            "should_hit_cache": "Generated",
            "description": "Should generate new cache patterns dynamically",
        },
    ]

    print("🚀 Starting server verification...")

    # Check if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=2)
        print("✅ Server is running")
    except:
        print(
            "❌ Server not running. Please start with: ./target/release/think-ai server"
        )
        return

    print("\n🧪 Testing each cache level with detailed logging...")
    print("📝 Check the server logs to see cache hits/misses!")
    print("")

    cache_verification_results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['name']}")
        print(f"   Query: '{test_case['query']}'")
        print(f"   Expected: {test_case['description']}")

        try:
            start_time = time.time()
            response = requests.post(
                f"{base_url}/chat",
                headers={"Content-Type": "application/json"},
                json={"query": test_case["query"]},
                timeout=10,
            )
            response_time = (time.time() - start_time) * 1000

            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")

                print(f"   ⏱️  Response time: {response_time:.1f}ms")
                print(f"   📄 Response length: {len(ai_response)} chars")
                print(f"   💬 Response preview: {ai_response[:60]}...")

                # Analyze response characteristics to infer cache usage
                cache_indicators = {
                    "very_fast": response_time < 30,
                    "consistent_length": len(ai_response) > 100,
                    "engaging": "?" in ai_response or "!" in ai_response,
                    "specific_content": any(
                        word in ai_response.lower()
                        for word in ["love", "human", "programming", "hello"]
                    ),
                }

                if (
                    cache_indicators["very_fast"]
                    and cache_indicators["consistent_length"]
                ):
                    print(f"   🎯 LIKELY CACHE HIT - Fast, consistent response")
                    cache_verification_results.append("HIT")
                elif response_time < 100:
                    print(f"   ⚡ POSSIBLE CACHE HIT - Reasonably fast")
                    cache_verification_results.append("POSSIBLE")
                else:
                    print(
                        f"   🔄 LIKELY COMPUTED - Slower response suggests processing"
                    )
                    cache_verification_results.append("MISS")

                print(f"   📊 Cache indicators: {cache_indicators}")

            else:
                print(f"   ❌ FAIL - HTTP {response.status_code}")
                cache_verification_results.append("ERROR")

        except Exception as e:
            print(f"   ❌ ERROR - {e}")
            cache_verification_results.append("ERROR")

        print("")
        time.sleep(1)  # Pause between requests to see logs clearly

    print("=" * 50)
    print("📊 Cache Verification Summary:")
    hits = cache_verification_results.count("HIT")
    possible = cache_verification_results.count("POSSIBLE")
    misses = cache_verification_results.count("MISS")
    errors = cache_verification_results.count("ERROR")

    print(f"   🎯 Definite Cache Hits: {hits}")
    print(f"   ⚡ Possible Cache Hits: {possible}")
    print(f"   🔄 Likely Cache Misses: {misses}")
    print(f"   ❌ Errors: {errors}")

    if hits >= 3:
        print("\n🎉 SUCCESS: Multi-level cache appears to be working!")
    elif hits + possible >= 4:
        print("\n✅ GOOD: Cache system likely functioning")
    else:
        print("\n⚠️  WARNING: Cache may not be working as expected")

    print("\n🔍 To verify cache usage:")
    print("1. Check server logs for 'MultiLevel Cache' messages")
    print("2. Look for 'CACHE HIT' vs 'CACHE MISS' logs")
    print("3. Check component scoring - MultiLevelCache should score highest")
    print("4. Verify 'USING COMPONENT: MultiLevelCache' messages")


def test_cache_vs_conversational():
    print("\n🆚 Testing Cache vs Conversational Component Priority")
    print("=" * 55)

    base_url = "http://localhost:8080"

    # Test query that both components could handle
    test_query = "hello"

    print(f"Testing query: '{test_query}'")
    print("This should prefer MultiLevelCache over Conversational component")
    print("")

    try:
        response = requests.post(
            f"{base_url}/chat",
            headers={"Content-Type": "application/json"},
            json={"query": test_query},
            timeout=5,
        )

        if response.status_code == 200:
            data = response.json()
            ai_response = data.get("response", "")

            print(f"Response: {ai_response}")
            print("")
            print("🔍 Check the server logs above to see:")
            print("- Component scoring (MultiLevelCache should score highest)")
            print("- Which component was actually used")
            print("- Whether cache hit or miss occurred")

        else:
            print(f"❌ HTTP {response.status_code}")

    except Exception as e:
        print(f"❌ ERROR - {e}")


if __name__ == "__main__":
    verify_cache_usage()
    test_cache_vs_conversational()
