#!/usr/bin/env python3
"""Test markdown handling through the API"""

import requests
import json

# Test cases
test_messages = [
    "# Simple Header",
    "This is **bold** and *italic*",
    "- List item 1\n- List item 2",
    "```python\nprint('hello')\n```",
    """# Complete Test

This has **formatting**.

## Lists
- Item 1
- Item 2

1. First
2. Second

`inline code` here"""
]

print("Testing Think AI Markdown Handling")
print("="*50)

for i, msg in enumerate(test_messages):
    print(f"\nTest {i+1}: {msg[:30]}...")
    
    try:
        # Send to API
        response = requests.post(
            "http://localhost:7777/api/chat",
            headers={"Content-Type": "application/json"},
            json={"query": msg}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Response received")
            print(f"  Source: {data['metadata']['source']}")
            print(f"  Response preview: {data['response'][:100]}...")
        else:
            print(f"✗ Error {response.status_code}")
            
    except Exception as e:
        print(f"✗ Failed: {e}")

print("\n" + "="*50)
print("Open http://localhost:8889/debug_markdown_parser.html to see parser tests")
print("Open http://localhost:7777 to test in the actual webapp")