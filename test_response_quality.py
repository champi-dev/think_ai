#!/usr/bin/env python3
"""Test script to verify improved response quality after removing template responses"""

import subprocess
import json
import time

def test_response(query):
    """Send a query to Think AI and get the response"""
    process = subprocess.Popen(
        ['./target/release/think-ai', 'chat'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=query + '\nexit\n')
    
    # Extract the response (skip the welcome message and prompts)
    lines = stdout.strip().split('\n')
    response_lines = []
    capture = False
    
    for line in lines:
        if query in line:
            capture = True
            continue
        elif capture and ('>' in line or 'exit' in line):
            break
        elif capture:
            response_lines.append(line)
    
    return '\n'.join(response_lines).strip()

def analyze_response(query, response):
    """Analyze if the response has template patterns"""
    template_patterns = [
        "Your question about",
        "Regarding your inquiry about",
        "Throughout history",
        "continues to evolve with new discoveries",
        "Additionally, throughout history",
        "Furthermore,",
        "the understanding of",
    ]
    
    problems = []
    for pattern in template_patterns:
        if pattern in response:
            problems.append(f"Found template pattern: '{pattern}'")
    
    return problems

def main():
    print("Testing Think AI Response Quality\n" + "="*50)
    
    test_queries = [
        "what is the sun",
        "what is the universe",
        "what is love",
        "hello",
        "what is programming",
    ]
    
    results = []
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 30)
        
        response = test_response(query)
        print(f"Response: {response}")
        
        problems = analyze_response(query, response)
        
        if problems:
            print(f"\n❌ Issues found:")
            for problem in problems:
                print(f"   - {problem}")
        else:
            print(f"\n✅ No template patterns detected!")
        
        results.append({
            "query": query,
            "response": response,
            "problems": problems,
            "passed": len(problems) == 0
        })
        
        time.sleep(0.5)  # Small delay between tests
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print(f"Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed < total:
        print("\nFailed queries:")
        for r in results:
            if not r["passed"]:
                print(f"  - {r['query']}: {len(r['problems'])} issues")

if __name__ == "__main__":
    main()