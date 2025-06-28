#!/usr/bin/env python3

import subprocess
import time
import requests

def test_step4_word_analysis():
    print("🔍 STEP 4: Testing Word-by-Word Analysis")
    print("=" * 50)
    
    server_process = None
    try:
        # Start server
        print("🚀 Starting server...")
        server_process = subprocess.Popen(
            ['./target/release/think-ai', 'server'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        time.sleep(3)
        
        # Test word-by-word analysis specifically
        print("\n🧪 Testing word-by-word analysis...")
        
        test_cases = [
            {
                "name": "Single Word with Cache",
                "query": "programming",
                "expected_words": ["programming"],
                "should_analyze": True
            },
            {
                "name": "Multiple Words", 
                "query": "what is programming",
                "expected_words": ["what", "is", "programming"],
                "should_analyze": True
            },
            {
                "name": "Novel Technical Query",
                "query": "quantum computing algorithms",
                "expected_words": ["quantum", "computing", "algorithms"],
                "should_analyze": True
            },
            {
                "name": "Mixed Domain Query",
                "query": "programming with consciousness",
                "expected_words": ["programming", "with", "consciousness"],
                "should_analyze": True
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. {test_case['name']}")
            print(f"   Query: '{test_case['query']}'")
            print(f"   Expected words: {test_case['expected_words']}")
            
            try:
                response = requests.post(
                    "http://localhost:8080/chat",
                    headers={"Content-Type": "application/json"},
                    json={"query": test_case["query"]},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data.get("response", "")
                    print(f"   📥 Response: {ai_response[:120]}{'...' if len(ai_response) > 120 else ''}")
                    
                    # Analyze if response looks like it used word analysis
                    word_indicators = 0
                    for word in test_case['expected_words']:
                        if word.lower() in ai_response.lower():
                            word_indicators += 1
                    
                    if word_indicators >= len(test_case['expected_words']) // 2:
                        print(f"   ✅ GOOD: Response contains {word_indicators}/{len(test_case['expected_words'])} expected words")
                    else:
                        print(f"   ❓ UNCLEAR: Only {word_indicators}/{len(test_case['expected_words'])} expected words found")
                    
                    # Check for signs of sophisticated analysis
                    if len(ai_response) > 100 and ("aspect" in ai_response or "explore" in ai_response):
                        print("   🎯 SOPHISTICATED: Response shows contextual understanding")
                    else:
                        print("   📝 BASIC: Simple response pattern")
                        
                else:
                    print(f"   ❌ HTTP Error: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Request Error: {e}")
        
        # Check server logs for word analysis evidence
        print("\n📋 Analyzing word analysis logs...")
        try:
            server_process.terminate()
            stdout, stderr = server_process.communicate(timeout=5)
            
            # Look for word analysis activity
            word_analysis_lines = [line for line in stdout.split('\n') if 'Words:' in line or 'word' in line.lower()]
            multilevel_lines = [line for line in stdout.split('\n') if 'Analyzing query components' in line]
            
            print(f"   Found {len(word_analysis_lines)} word analysis related lines")
            print(f"   Found {len(multilevel_lines)} component analysis lines")
            
            if multilevel_lines:
                print("   ✅ FOUND: Component analysis activity")
                for line in multilevel_lines[-3:]:
                    print(f"      {line}")
            else:
                print("   ❌ MISSING: No component analysis detected")
                
            if word_analysis_lines:
                print("   📋 Word analysis lines:")
                for line in word_analysis_lines[-5:]:
                    print(f"      {line}")
            else:
                print("   ❓ No explicit word analysis logs found")
                
        except Exception as e:
            print(f"   ❌ Log analysis error: {e}")
    
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        if server_process and server_process.poll() is None:
            server_process.terminate()
            time.sleep(1)
    
    print("\n📊 STEP 4 RESULTS:")
    print("✅ If you see 'Component analysis activity' - word analysis is working")
    print("❌ If no analysis logs - need to implement proper word-by-word breakdown")
    print("🎯 Look for 'Words: [...]' logs showing actual word parsing")

if __name__ == "__main__":
    test_step4_word_analysis()