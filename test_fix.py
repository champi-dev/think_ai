#!/usr/bin/env python3
"""
Test script to verify the fix works correctly
"""

import json
from pathlib import Path

def test_response_mappings():
    """Test that responses are correctly mapped"""
    
    cache_dir = Path("./cache")
    response_cache_file = cache_dir / "response_cache.json"
    
    if not response_cache_file.exists():
        print("❌ response_cache.json not found")
        return
    
    with open(response_cache_file, 'r') as f:
        cache = json.load(f)
    
    # Test cases
    test_cases = [
        {
            "query": "ping",
            "expected_contains": "Pong",
            "should_not_contain": "electrical engineering"
        },
        {
            "query": "what is quantum physics",
            "expected_contains": "Quantum mechanics",
            "should_not_contain": "Psycholinguistics"
        },
        {
            "query": "electrical engineering",
            "expected_contains": "circuit analysis",
            "should_not_contain": "quantum"
        }
    ]
    
    print("🧪 Testing response mappings...\n")
    
    all_passed = True
    
    for test in test_cases:
        query = test["query"]
        if query in cache:
            response = cache[query]["response"]
            
            # Check expected content
            if test["expected_contains"].lower() in response.lower():
                print(f"✅ '{query}' -> Correct (contains '{test['expected_contains']}')")
            else:
                print(f"❌ '{query}' -> Missing expected content '{test['expected_contains']}'")
                all_passed = False
            
            # Check unwanted content
            if test["should_not_contain"].lower() in response.lower():
                print(f"❌ '{query}' -> Contains incorrect content '{test['should_not_contain']}'")
                all_passed = False
        else:
            print(f"❌ '{query}' -> Not found in cache")
            all_passed = False
    
    print("\n" + "="*50)
    
    if all_passed:
        print("✅ All tests passed! The fix is working correctly.")
    else:
        print("❌ Some tests failed. Check the implementation.")
    
    # Show sample responses
    print("\n📝 Sample Responses:")
    for query in ["ping", "what is quantum physics"]:
        if query in cache:
            response = cache[query]["response"]
            print(f"\nQ: {query}")
            print(f"A: {response[:150]}...")

if __name__ == "__main__":
    test_response_mappings()