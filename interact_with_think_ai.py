#! / usr / bin / env python3
"""Interact with Think AI to get deployment instructions"""

# Let's use the direct modules
try:
    from think_ai_cli.core import ThinkAICLI

    # Initialize CLI
    cli = ThinkAICLI()

    # Ask about deployment
    response = cli.chat(
        "How do I redeploy this Think AI application to production? Please provide step-by-step instructions.")
    print("Think AI Response:")
    print("=" * 50)
    print(response)
    print("=" * 50)

except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative approach...")

    # Alternative: use the web API
    import requests

    try:
        response = requests.post(
            "http://localhost:8000/api/v1/chat",
            json={"message": "How do I redeploy this Think AI application?"}
        )
        if response.status_code == 200:
            print("API Response:", response.json())
        else:
            print("API not available")
    except Exception:
        print("Cannot connect to API")
