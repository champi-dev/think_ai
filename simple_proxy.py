#!/usr/bin/env python3
import os
import subprocess
import time

# First start the backend
print("Starting backend server...")
backend_env = os.environ.copy()
backend_env["PORT"] = "7778"
subprocess.Popen(["./target/release/stable-server"], env=backend_env)
time.sleep(3)

# Then start a simple HTTP server with modified webapp
print("Preparing webapp...")

# Read webapp and modify to use correct backend
with open("minimal_3d.html", "r") as f:
    content = f.read()

# Replace API endpoints to point to backend port
content = content.replace("fetch('/health')", "fetch('http://localhost:7778/health')")
content = content.replace("fetch('/api/chat'", "fetch('http://localhost:7778/chat'")
content = content.replace(
    "fetch('/api/chat/stream'", "fetch('http://localhost:7778/chat/stream'"
)
content = content.replace("fetch('/stats'", "fetch('http://localhost:7778/stats'")

# Also fix the request body format
content = content.replace("{ message: query }", "{ query: query }")

# Save modified webapp
with open("webapp_temp.html", "w") as f:
    f.write(content)

print("Starting webapp server on port 7777...")
print("Access at: http://69.197.178.37:7777/webapp_temp.html")

# Start simple HTTP server
os.system("python3 -m http.server 7777 --bind 0.0.0.0")
