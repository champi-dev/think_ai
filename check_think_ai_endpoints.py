#!/usr/bin/env python3
"""
Check available endpoints on Think AI server
"""

import requests
import json

BASE_URL = "https://thinkai-production.up.railway.app"

endpoints_to_check = [
    "/",
    "/health",
    "/api/health",
    "/chat",
    "/api/chat",
    "/ask",
    "/api/ask",
    "/v1/chat",
    "/api/v1/chat",
    "/query",
    "/api/query"
]

print(f"Checking Think AI endpoints at: {BASE_URL}\n")

# First, try to get the root endpoint
print("Checking root endpoint...")
try:
    response = requests.get(BASE_URL, timeout=10)
    print(f"GET / - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
        if 'text/html' in response.headers.get('content-type', ''):
            print("Response: HTML page (likely the web interface)")
        else:
            print(f"Response preview: {response.text[:200]}...")
except Exception as e:
    print(f"GET / - Error: {e}")

print("\n" + "-"*60 + "\n")

# Check other endpoints
print("Checking API endpoints...")
for endpoint in endpoints_to_check[1:]:  # Skip root since we already checked it
    url = BASE_URL + endpoint
    
    # Try GET first
    try:
        response = requests.get(url, timeout=5)
        print(f"GET {endpoint} - Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  Response: {json.dumps(data, indent=2)[:100]}...")
            except:
                print(f"  Response: {response.text[:100]}...")
    except Exception as e:
        print(f"GET {endpoint} - Error: {e}")
    
    # Try POST for chat-like endpoints
    if any(word in endpoint for word in ["chat", "ask", "query"]):
        try:
            response = requests.post(
                url,
                json={"query": "Hello"},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            print(f"POST {endpoint} - Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  Response: {json.dumps(data, indent=2)[:100]}...")
                except:
                    print(f"  Response: {response.text[:100]}...")
        except Exception as e:
            print(f"POST {endpoint} - Error: {e}")
    
    print()

# Also check if there's API documentation
print("\nChecking for API documentation...")
doc_endpoints = ["/docs", "/api/docs", "/swagger", "/api", "/help"]
for endpoint in doc_endpoints:
    try:
        response = requests.get(BASE_URL + endpoint, timeout=5)
        if response.status_code == 200:
            print(f"Found documentation at: {endpoint}")
    except:
        pass