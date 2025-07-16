# \!/usr/bin/env python3
import urllib.request
import json

# First, let's test the API response directly
print("Testing API response format...")
url = "http://69.197.178.37:7777/api/chat"
data = json.dumps({"message": "test"}).encode("utf-8")
req = urllib.request.Request(
    url, data=data, headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as response:
        response_data = json.loads(response.read().decode())
        print(f"API Response: {json.dumps(response_data, indent=2)}")
        print(f"Response has 'response' field: {'response' in response_data}")
        print(f"Response value: {response_data.get('response', 'NO RESPONSE FIELD')}")
except Exception as e:
    print(f"Error: {e}")

# Now let's check what the browser would see
print("\n\nChecking browser console logs...")
browser_test = """
// This would run in browser console
const testApi = async () => {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: 'test'})
    });
    const data = await response.json();
    console.log('Response data:', data);
    console.log('Has response field:', 'response' in data);
    console.log('Response text:', data.response);
};
"""
print(browser_test)
