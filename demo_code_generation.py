#!/usr/bin/env python3
"""Quick demo showing Think AI enhanced code generation"""

from think_ai_conversation_enhanced import generate_contextual_response

# Test queries
queries = [
    "hi",
    "can you code?",
    "build a simple REST API",
    "create a pizza ordering web app",
    "write a CI/CD pipeline for GitHub Actions",
]

print("🧠 THINK AI ENHANCED CODE GENERATION DEMO")
print("=" * 80)

for query in queries:
    print(f"\n📝 Query: {query}")
    print("-" * 80)

    response = generate_contextual_response(query, [])

    # Show response (truncated if too long)
    if len(response) > 500:
        print(f"{response[:400]}...")
        print(f"\n[Response contains {len(response)} characters]")
        if "```" in response:
            code_blocks = response.count("```") // 2
            print(f"✅ Generated {code_blocks} code block(s)!")
    else:
        print(response)

    print()

print("\n" + "=" * 80)
print("✨ Demo complete! Think AI now generates real code!")
print("🚀 Try it yourself with: python simple_api_server.py")
print("=" * 80)
