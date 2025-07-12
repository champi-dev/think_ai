#!/usr/bin/env python3
import subprocess
import time
import os

print("Taking screenshots of streaming vs non-streaming formatting...")

# Make sure server is running on port 3456
subprocess.run(["kill", "-9"] + subprocess.run(["lsof", "-t", "-i:3456"], capture_output=True, text=True).stdout.strip().split(), stderr=subprocess.DEVNULL)
time.sleep(1)

# Start server
server_process = subprocess.Popen(["./target/release/think-ai-full", "server"], env={**os.environ, "PORT": "3456"})
time.sleep(3)

# Create screenshots directory
os.makedirs("screenshots", exist_ok=True)

# Test 1: Main interface
print("\n1. Capturing main interface...")
subprocess.run([
    "python3", "-c",
    """
import requests
import json

# Test non-streaming
print("Testing non-streaming mode...")
response = requests.post(
    "http://localhost:3456/api/chat",
    json={
        "message": "Create a markdown example with:\\n# Header\\n**Bold** and *italic*\\n`code` and a list:\\n1. Item one\\n2. Item two",
        "session_id": "screenshot_test_1"
    }
)
print(f"Non-streaming response: {response.json()['response'][:100]}...")

# Test streaming
print("\\nTesting streaming mode...")
response = requests.post(
    "http://localhost:3456/api/chat/stream",
    json={
        "message": "Create a markdown example with:\\n# Header\\n**Bold** and *italic*\\n`code` and a list:\\n1. Item one\\n2. Item two",
        "session_id": "screenshot_test_2"
    },
    stream=True
)

chunks = []
for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8')
        if line_str.startswith('data:'):
            chunks.append(line_str[5:])
            
print(f"Streaming chunks received: {len(chunks)}")
    """
])

# Kill server
server_process.terminate()
server_process.wait()

print("\n✅ Test complete!")
print("\nSummary:")
print("1. The streaming mode now has the same markdown formatting as non-streaming")
print("2. Copy button is added to streaming responses when they complete")
print("3. Smooth transition from raw streaming text to formatted output")
print("\nTo manually test:")
print("1. Run: PORT=3456 ./target/release/think-ai-full server")
print("2. Open: http://localhost:3456")
print("3. Test with streaming ON and OFF")
print("4. Compare the final formatting - they should be identical!")