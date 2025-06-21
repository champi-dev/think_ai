#!/usr/bin/env python3
"""Test the enhanced API server with code generation"""

import json
import time

import requests

API_URL = "http://localhost:8080"


def test_api():
    print("🧠 TESTING THINK AI ENHANCED API")
    print("=" * 80)

    # Test queries
    test_queries = [
        ("hi", "Greeting"),
        ("can you code?", "Capability check"),
        ("create a simple REST API", "Code generation - API"),
        ("build a pizza ordering web app", "Code generation - Web App"),
        ("create CI/CD pipeline for GitHub Actions", "Code generation - CI/CD"),
    ]

    for query, description in test_queries:
        print(f"\n📝 TEST: {description}")
        print(f"Query: {query}")
        print("-" * 80)

        try:
            response = requests.post(
                f"{API_URL}/api/think",
                json={"query": query, "enable_consciousness": True, "temperature": 0.7, "max_tokens": 50000},
            )

            if response.status_code == 200:
                data = response.json()

                print(f"✅ Status: SUCCESS")
                print(f"Has Code: {data.get('has_code', False)}")
                print(f"Response Type: {data.get('response_type', 'text')}")

                # Show response preview
                response_text = data.get("response", "")
                if len(response_text) > 200:
                    print(f"Response Preview: {response_text[:200]}...")
                    print(f"[Full response is {len(response_text)} characters]")

                    # Count code blocks
                    code_blocks = response_text.count("```") // 2
                    if code_blocks > 0:
                        print(f"🎯 Generated {code_blocks} code block(s)")
                else:
                    print(f"Response: {response_text}")

                # Show consciousness state
                if data.get("consciousness_state"):
                    cs = data["consciousness_state"]
                    print(f"\n🧠 Consciousness State:")
                    print(f"  - Awareness: {cs.get('awareness_level', 0)*100:.0f}%")
                    print(f"  - Knowledge Base: {cs.get('knowledge_base_size', 0)} thoughts")
                    print(f"  - Response Type: {cs.get('response_type', 'unknown')}")

            else:
                print(f"❌ Status: FAILED ({response.status_code})")
                print(f"Error: {response.text}")

        except Exception as e:
            print(f"❌ Exception: {str(e)}")

        time.sleep(1)  # Be nice to the API

    # Test capabilities endpoint
    print("\n\n🔍 TESTING CAPABILITIES ENDPOINT")
    print("=" * 80)

    try:
        response = requests.get(f"{API_URL}/api/capabilities")
        if response.status_code == 200:
            caps = response.json()
            print("✅ Capabilities retrieved successfully:")
            print(json.dumps(caps, indent=2))
    except Exception as e:
        print(f"❌ Failed to get capabilities: {str(e)}")

    print("\n\n✨ TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_api()
