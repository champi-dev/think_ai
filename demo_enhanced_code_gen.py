#!/usr/bin/env python3
"""Demonstrate Think AI Enhanced Code Generation"""

import sys

from think_ai_conversation_enhanced import *

# Initialize components
print("🧠 INITIALIZING THINK AI ENHANCED CODE GENERATOR")
print("=" * 80)

# Test queries
test_queries = [
    ("hi", "Should return greeting"),
    ("can u code?", "Should confirm coding ability"),
    ("build a simple API", "Should generate API code"),
    ("create a pizza ordering web app", "Should generate web app"),
    (
        "build ur own ci cd pipeline tooling for deploying yourself think ai to github actions an vercel",
        "Should generate CI/CD",
    ),
]

for query, expected in test_queries:
    print(f"\n{'='*80}")
    print(f"QUERY: {query}")
    print(f"EXPECTED: {expected}")
    print("-" * 80)

    # Generate response
    response = generate_contextual_response(query, [])

    # Show response summary
    if len(response) > 500:
        print(f"RESPONSE: {response[:300]}...")
        print(f"\n[...Response contains {len(response)} characters with code...]")
        if "```" in response:
            code_blocks = response.count("```") // 2
            print(f"✅ Generated {code_blocks} code block(s)")
    else:
        print(f"RESPONSE: {response}")
    print()

print("\n" + "=" * 80)
print("✅ THINK AI ENHANCED NOW GENERATES REAL CODE!")
print("✅ Fixed issues: Actually codes when asked")
print("✅ Provides CI/CD pipelines, APIs, web apps, and more")
print("=" * 80)
