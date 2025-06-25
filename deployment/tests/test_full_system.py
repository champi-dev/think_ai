#!/usr/bin/env python3
"""Test full system functionality - max 40 lines."""

import time
import requests
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from deployment.core.dynamic_o1_ai import DynamicO1AI

def test_o1_performance():
    """Test O(1) performance."""
    ai = DynamicO1AI()
    times = []
    
    for i in range(100):
        msg = f"Test message {i} with different content"
        _, elapsed = ai.generate_response(msg)
        times.append(elapsed)
    
    avg_time = sum(times) / len(times)
    max_time = max(times)
    
    assert avg_time < 1.0, f"Average time {avg_time}ms > 1ms"
    assert max_time < 5.0, f"Max time {max_time}ms > 5ms"
    
    return {"avg_ms": avg_time, "max_ms": max_time, "iterations": len(times)}

def test_dynamic_responses():
    """Test responses are dynamic, not pre-computed."""
    ai = DynamicO1AI()
    responses = set()
    
    # Same input should give different responses
    for _ in range(10):
        response, _ = ai.generate_response("Hello")
        responses.add(response)
    
    assert len(responses) > 1, "Responses are not dynamic!"
    return {"unique_responses": len(responses)}

if __name__ == "__main__":
    print("🧪 Testing Think AI Full System...")
    print(f"✅ O(1) Performance: {test_o1_performance()}")
    print(f"✅ Dynamic Responses: {test_dynamic_responses()}")
    print("🎉 All tests passed!")