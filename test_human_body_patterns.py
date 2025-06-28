#!/usr/bin/env python3

import requests
import json
import time

def test_human_body_patterns():
    print("🧪 Testing Human & Body Pattern Fixes")
    print("=" * 45)
    
    base_url = "http://localhost:8080"
    
    # Test the exact patterns that were broken
    test_cases = [
        {
            "name": "Human Concept Question (was giving random anatomy)",
            "query": "what means human",
            "expected_keywords": ["human", "conscious", "empathy", "creativity", "meaning", "remarkable"]
        },
        {
            "name": "Body Concept Question (was giving generic fallback)",
            "query": "what is body?",
            "expected_keywords": ["body", "experience", "sensation", "home", "connection", "fascinating"]
        },
        {
            "name": "Alternative Human Question",
            "query": "what is human",
            "expected_keywords": ["human", "beings", "love", "creativity", "empathy"]
        },
        {
            "name": "Alternative Body Question",
            "query": "what means body",
            "expected_keywords": ["body", "intimate", "biological", "experience", "touch"]
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
    
    print("\n🔍 Testing human & body conversation patterns...")
    
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
                
                print(f"   Response: {ai_response[:120]}{'...' if len(ai_response) > 120 else ''}")
                
                # Check if response contains expected keywords
                response_lower = ai_response.lower()
                found_keywords = [kw for kw in test_case["expected_keywords"] if kw.lower() in response_lower]
                
                if len(found_keywords) >= 3:  # At least 3 keywords should match
                    print(f"   ✅ PASS - Found keywords: {found_keywords}")
                else:
                    print(f"   ❌ FAIL - Expected keywords: {test_case['expected_keywords']}")
                    print(f"            Found keywords: {found_keywords}")
                    all_passed = False
                    
                # Check for problematic fallbacks that were happening before
                if ("Human anatomy studies body structure" in ai_response or 
                    "That's a really thoughtful question" in ai_response or
                    "I don't have specific information" in ai_response):
                    print(f"   ⚠️  WARNING - Contains old fallback/random knowledge text")
                    all_passed = False
                else:
                    print(f"   🎯 GOOD - No fallback/random knowledge detected")
                    
            else:
                print(f"   ❌ FAIL - HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERROR - {e}")
            all_passed = False
        
        time.sleep(0.5)  # Brief pause between requests
    
    print("\n" + "=" * 45)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Human & body patterns fixed.")
    else:
        print("⚠️  Some tests failed. Check the patterns above.")
    
    print("\n📊 Summary:")
    print("- 'what means human' should now give thoughtful response about humanity")
    print("- 'what is body?' should now give philosophical response about the human body")
    print("- No more random anatomy responses or generic fallbacks")
    print("- Both patterns should engage with questions about personal meaning")

if __name__ == "__main__":
    test_human_body_patterns()