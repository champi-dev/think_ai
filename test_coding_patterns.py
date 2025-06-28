#!/usr/bin/env python3

import requests
import json

def test_coding_patterns():
    print("🧪 Testing Specific Coding Pattern Fixes")
    print("=" * 50)
    
    base_url = "http://localhost:8080"
    
    # Test the exact patterns the user reported as broken
    test_cases = [
        {
            "name": "Informal Coding Question",
            "query": "can u code?",
            "expected": "coding"
        },
        {
            "name": "Single Word Coding",
            "query": "coding?",
            "expected": "coding"
        },
        {
            "name": "What is Code Question",
            "query": "what is code?",
            "expected": "code"
        },
        {
            "name": "Standard Coding Question",
            "query": "can you code",
            "expected": "coding"
        }
    ]
    
    print("🔍 Testing each pattern...")
    
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
                
                print(f"   Response: {ai_response[:80]}{'...' if len(ai_response) > 80 else ''}")
                
                # Check if it's about coding (not generic fallback)
                if (test_case["expected"] in ai_response.lower() and 
                    "programming" in ai_response.lower() and
                    not "That's a really thoughtful question" in ai_response):
                    print(f"   ✅ PASS - Proper coding response")
                else:
                    print(f"   ❌ FAIL - Still giving generic fallback")
                    
            else:
                print(f"   ❌ FAIL - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ ERROR - {e}")

if __name__ == "__main__":
    test_coding_patterns()