#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import subprocess
import time
import urllib.request
import urllib.error

PORT = 7777
HOST = "0.0.0.0"
BACKEND_PORT = 7778

# Start the stable server on backend port
print(f"Starting backend server on port {BACKEND_PORT}...")
backend_env = os.environ.copy()
backend_env["PORT"] = str(BACKEND_PORT)
backend_process = subprocess.Popen(
    ["./target/release/stable-server"],
    env=backend_env
)
time.sleep(3)  # Give backend time to start

class SimpleWebappHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve minimal_3d.html for root path
            try:
                with open('minimal_3d.html', 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                print(f"Error serving webapp: {e}")
                self.send_error(404)
                return
        
        # Let the webapp communicate directly with backend on BACKEND_PORT
        # Just serve static files
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

os.chdir('/home/administrator/think_ai')
print(f"🚀 Starting Think AI Webapp Server on http://{HOST}:{PORT}")
print(f"🌐 Access remotely at: http://69.197.178.37:{PORT}")
print(f"📡 Backend API server running on port {BACKEND_PORT}")
print(f"📁 Webapp will communicate directly with backend")

# Update the webapp to use the backend port
webapp_content = open('minimal_3d.html', 'r').read()
# Replace API calls to use backend port
webapp_content = webapp_content.replace("fetch('/health')", f"fetch('http://localhost:{BACKEND_PORT}/health')")
webapp_content = webapp_content.replace("fetch('/chat'", f"fetch('http://localhost:{BACKEND_PORT}/chat'")
webapp_content = webapp_content.replace("fetch('/chat/stream'", f"fetch('http://localhost:{BACKEND_PORT}/chat/stream'")
webapp_content = webapp_content.replace("fetch('/stats'", f"fetch('http://localhost:{BACKEND_PORT}/stats'")

# Save modified webapp
with open('minimal_3d_temp.html', 'w') as f:
    f.write(webapp_content)

# Serve the modified version
os.rename('minimal_3d_temp.html', 'minimal_3d.html')

try:
    with socketserver.TCPServer((HOST, PORT), SimpleWebappHandler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n👋 Stopping servers...")
    backend_process.terminate()
except Exception as e:
    print(f"Error: {e}")
    backend_process.terminate()