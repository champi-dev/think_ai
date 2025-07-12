#\!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import subprocess
import time
import urllib.request
import sys

PORT = 7777
HOST = "0.0.0.0"

# Start backend if not running
try:
    urllib.request.urlopen('http://localhost:8888/health', timeout=2)
    print("Backend already running on 8888")
except:
    print("Starting backend on port 8888...")
    os.system("pkill -f stable-server 2>/dev/null || true")
    time.sleep(1)
    
    backend_env = os.environ.copy()
    backend_env["PORT"] = "8888"
    subprocess.Popen(
        ["./target/release/stable-server"],
        env=backend_env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3)

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            try:
                with open('minimal_3d.html', 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            except:
                self.send_error(500)
                
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'OK')
    
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Try backend first
                data = json.loads(post_data)
                message = data.get('message', data.get('query', ''))
                backend_data = json.dumps({"query": message})
                
                req = urllib.request.Request(
                    'http://localhost:8888/chat',
                    data=backend_data.encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req, timeout=10) as resp:
                    response_data = resp.read()
                    
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response_data)
            except:
                # Fallback response
                fallback = json.dumps({
                    "response": "Hello\! I'm Think AI. How can I help you today?",
                    "metadata": {"source": "fallback"}
                })
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(fallback.encode())
                
        elif self.path == '/api/chat/stream':
            # Simple non-streaming fallback
            self.path = '/api/chat'
            self.do_POST()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        pass

print(f"Starting server on {HOST}:{PORT}")
os.chdir('/home/administrator/think_ai')

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    print(f"Server ready at http://69.197.178.37:{PORT}")
    httpd.serve_forever()
