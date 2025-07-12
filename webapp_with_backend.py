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
backend_process = subprocess.Popen(
    ["./target/release/stable-server"],
    env={**os.environ, "PORT": str(BACKEND_PORT)},
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
time.sleep(3)  # Give backend time to start

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve minimal_3d.html for root path
            try:
                with open('minimal_3d.html', 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-length', len(content))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                print(f"Error serving webapp: {e}")
        
        elif self.path in ['/health', '/stats']:
            # Proxy GET requests to backend
            try:
                req = urllib.request.Request(f'http://localhost:{BACKEND_PORT}{self.path}')
                with urllib.request.urlopen(req) as resp:
                    content = resp.read()
                    self.send_response(200)
                    self.send_header('Content-type', resp.headers.get('Content-Type', 'text/plain'))
                    self.send_header('Content-length', len(content))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(content)
                    return
            except Exception as e:
                print(f"Error proxying GET: {e}")
                self.send_error(502, "Bad Gateway")
                return
        
        # For other paths, use default handler
        return super().do_GET(self)
    
    def do_POST(self):
        if self.path == '/chat':
            # Proxy chat requests to backend
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Forward to backend
                req = urllib.request.Request(
                    f'http://localhost:{BACKEND_PORT}/chat',
                    data=post_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req) as resp:
                    content = resp.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Content-length', len(content))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(content)
                
            except urllib.error.HTTPError as e:
                print(f"HTTP Error proxying chat: {e}")
                self.send_error(e.code, e.reason)
            except Exception as e:
                print(f"Error proxying chat: {e}")
                self.send_error(502, "Bad Gateway")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

os.chdir('/home/administrator/think_ai')
print(f"🚀 Starting Think AI Webapp with Backend on http://{HOST}:{PORT}")
print(f"🌐 Access remotely at: http://69.197.178.37:{PORT}")
print(f"📡 Backend server on port {BACKEND_PORT}")
print(f"📁 Serving minimal_3d.html with real AI responses")

try:
    with socketserver.TCPServer((HOST, PORT), ProxyHandler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n👋 Stopping servers...")
    backend_process.terminate()
except Exception as e:
    print(f"Error: {e}")
    backend_process.terminate()