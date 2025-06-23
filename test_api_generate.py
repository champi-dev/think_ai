#!/usr/bin/env python3
"""Test the generate API endpoint."""

import requests
import json


def test_generate():
    """Test the generate endpoint."""
    url = "http://localhost:8080/api/v1/generate"

    payload = {"prompt": "Hello Think AI!", "max_length": 200, "temperature": 0.7, "colombian_mode": True}

    print("Testing generate endpoint...")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    response = requests.post(url, json=payload)

    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success!")
        print(f"Generated text: {data.get('generated_text', 'N/A')}")
        print(f"Colombian mode: {data.get('colombian_mode', False)}")
    else:
        print(f"\n❌ Failed with status {response.status_code}")


if __name__ == "__main__":
    test_generate()
