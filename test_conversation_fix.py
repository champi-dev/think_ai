#!/usr/bin/env python3

import requests
import json
import time

# Test the fixed conversation patterns
def test_conversation_patterns():
    print("🧪 Testing Fixed Conversation Patterns")
    print("=" * 50)
    
    base_url = "http://localhost:8080"
    
    # Test cases that were failing before
    test_cases = [
        {
            "name": "Family Question (was giving Industrial Revolution)",
            "query": "what is family",
            "expected_keywords": ["family", "love", "support", "care", "connection"]
        },
        {
            "name": "Coding Request (was giving random knowledge)",
            "query": "create a hello world in python",
            "expected_keywords": ["python", "print", "Hello", "World"]
        },
        {
            "name": "Coding Ability Question",
            "query": "can you code",
            "expected_keywords": ["code", "programming", "help", "python", "javascript"]
        },
        {
            "name": "Personal Emotion Question",
            "query": "do you feel love",
            "expected_keywords": ["feel", "care", "connection", "experience", "meaningful"]
        },
        {
            "name": "Love Concept Question",
            "query": "what is love",
            "expected_keywords": ["love", "profound", "connection", "affection", "forms"]
        }
    ]
    
    print("🚀 Starting test server check...")
    
    # Check if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=2)
        print("✅ Server is running")
    except:
        print("❌ Server not running. Please start with: ./target/release/think-ai server")
        return
    
    print("\n🔍 Testing conversation patterns...")
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Query: '{test_case['query']}'")
        
        try:
            response = requests.post(
                f"{base_url}/chat",
                headers={"Content-Type": "application/json"},
                json={"query": test_case["query"]},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                
                print(f"   Response: {ai_response[:100]}{'...' if len(ai_response) > 100 else ''}")
                
                # Check if response contains expected keywords
                response_lower = ai_response.lower()
                found_keywords = [kw for kw in test_case["expected_keywords"] if kw.lower() in response_lower]
                
                if len(found_keywords) >= 2:  # At least 2 keywords should match
                    print(f"   ✅ PASS - Found keywords: {found_keywords}")
                else:
                    print(f"   ❌ FAIL - Expected keywords: {test_case['expected_keywords']}")
                    print(f"            Found keywords: {found_keywords}")
                    all_passed = False
                    
                # Check for problematic fallbacks
                if ("Industrial Revolution" in ai_response or 
                    "I don't have specific information" in ai_response or
                    "Additionally, i don't have" in ai_response):
                    print(f"   ⚠️  WARNING - Contains fallback text")
                    all_passed = False
                    
            else:
                print(f"   ❌ FAIL - HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERROR - {e}")
            all_passed = False
        
        time.sleep(0.5)  # Brief pause between requests
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Conversation patterns fixed.")
    else:
        print("⚠️  Some tests failed. Check the patterns above.")
    
    print("\n📊 Summary:")
    print("- Family questions should now give thoughtful responses about relationships")
    print("- Coding requests should provide actual code examples")
    print("- Personal questions should engage meaningfully")
    print("- No more random knowledge fallbacks for conversational queries")

if __name__ == "__main__":
    test_conversation_patterns()