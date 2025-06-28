#!/usr/bin/env python3

import requests
import json
import time

def test_conversation_continuity():
    print("🧪 Testing Conversation Continuity")
    print("=" * 40)
    
    base_url = "http://localhost:8080"
    
    # Test the exact conversation flow that was broken
    conversation_steps = [
        {
            "query": "hello",
            "expected_type": "greeting"
        },
        {
            "query": "what is love",
            "expected_type": "love_concept"
        },
        {
            "query": "what is care",
            "expected_type": "care_concept_with_continuity"
        }
    ]
    
    print("🔄 Running the exact conversation that was failing...")
    print()
    
    for i, step in enumerate(conversation_steps, 1):
        print(f"{i}. Query: '{step['query']}'")
        
        try:
            response = requests.post(
                f"{base_url}/chat",
                headers={"Content-Type": "application/json"},
                json={"query": step["query"]},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                
                print(f"   Response: {ai_response[:100]}{'...' if len(ai_response) > 100 else ''}")
                
                # Check the response quality
                if step["expected_type"] == "greeting":
                    if "Think AI" in ai_response and "meet you" in ai_response:
                        print("   ✅ PASS - Proper greeting")
                    else:
                        print("   ❌ FAIL - Poor greeting")
                        
                elif step["expected_type"] == "love_concept":
                    if "love" in ai_response.lower() and "emotion" in ai_response.lower():
                        print("   ✅ PASS - Good love concept response")
                    else:
                        print("   ❌ FAIL - Poor love response")
                        
                elif step["expected_type"] == "care_concept_with_continuity":
                    if ("care" in ai_response.lower() and 
                        "That's a really thoughtful question" not in ai_response and
                        len(ai_response) > 100):  # Should be substantive, not generic
                        print("   ✅ PASS - Proper care concept response")
                        
                        # Check for conversation continuity
                        if "love" in ai_response.lower() or "talking about" in ai_response.lower():
                            print("   🎯 BONUS - Shows conversation continuity!")
                        else:
                            print("   📝 NOTE - Care response good, but no explicit continuity reference")
                    else:
                        print("   ❌ FAIL - Still giving generic fallback for 'what is care'")
                        
            else:
                print(f"   ❌ FAIL - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ ERROR - {e}")
        
        print()
        time.sleep(0.3)  # Brief pause between requests
    
    print("=" * 40)
    print("📊 This test validates that 'what is care' now gets a proper")
    print("   conversational response instead of a generic fallback.")

if __name__ == "__main__":
    test_conversation_continuity()