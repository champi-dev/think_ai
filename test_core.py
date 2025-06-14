#!/usr/bin/env python3
"""Simple test script to verify Think AI core functionality."""

import os
import asyncio
from think_ai.integrations.claude_api import ClaudeAPI

async def test_claude_api():
    """Test Claude API integration."""
    try:
        # Check if API key is available
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            print("❌ No Claude API key found in environment")
            return False
        
        print("🔑 Claude API key found")
        print(f"🤖 Model: {os.getenv('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022')}")
        print(f"💰 Budget: ${os.getenv('CLAUDE_BUDGET_LIMIT', '20.0')}")
        
        # Initialize Claude API
        claude = ClaudeAPI()
        print("✅ Claude API initialized successfully")
        
        # Get cost summary
        cost_summary = claude.get_cost_summary()
        print(f"💵 Budget remaining: ${cost_summary['budget_remaining']:.2f}")
        
        await claude.close()
        return True
        
    except Exception as e:
        print(f"❌ Error testing Claude API: {e}")
        return False

async def main():
    """Main test function."""
    print("🧠 Testing Think AI Core Components...")
    
    # Test Claude API
    claude_ok = await test_claude_api()
    
    if claude_ok:
        print("\n✅ Think AI setup completed successfully!")
        print("\nYou can now:")
        print("  • Run: python3 -m think_ai.cli.main")
        print("  • Test Claude integration with your API key")
        print("  • Explore the rich CLI interface")
    else:
        print("\n⚠️  Setup completed with warnings")
        print("Claude API may need configuration")

if __name__ == "__main__":
    asyncio.run(main())