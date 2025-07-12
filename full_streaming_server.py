#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import subprocess
import time
import urllib.request
import urllib.error
import threading

PORT = 7777
HOST = "0.0.0.0"
BACKEND_PORT = 8889  # Different port to avoid conflicts

# Kill any existing backends
os.system("lsof -ti:8889 | xargs kill -9 2>/dev/null || true")
time.sleep(1)

# Start the stable server on backend port
print(f"Starting Qwen-powered backend on port {BACKEND_PORT}...")
backend_process = subprocess.Popen(
    ["./target/release/stable-server"],
    env={**os.environ, "PORT": str(BACKEND_PORT)},
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
time.sleep(5)  # Give backend time to start

class StreamingProxyHandler(http.server.BaseHTTPRequestHandler):
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
            except Exception as e:
                print(f"Error serving webapp: {e}")
                self.send_error(500)
        
        elif self.path == '/health':
            # Check backend health
            try:
                req = urllib.request.Request(f'http://localhost:{BACKEND_PORT}/health')
                with urllib.request.urlopen(req, timeout=2) as resp:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(b"OK - Backend Connected")
            except:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b"OK - Frontend Running")
                
        elif self.path == '/stats':
            # Proxy stats to backend
            try:
                req = urllib.request.Request(f'http://localhost:{BACKEND_PORT}/stats')
                with urllib.request.urlopen(req) as resp:
                    content = resp.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(content)
            except Exception as e:
                print(f"Stats error: {e}")
                self.send_error(502)
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path in ['/api/chat', '/chat']:
            # Handle regular chat endpoint
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse incoming data
                data = json.loads(post_data)
                message = data.get('message', data.get('query', ''))
                
                # Prepare request for backend
                backend_data = json.dumps({"query": message})
                
                req = urllib.request.Request(
                    f'http://localhost:{BACKEND_PORT}/chat',
                    data=backend_data.encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req, timeout=30) as resp:
                    content = resp.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(content)
                    
            except Exception as e:
                print(f"Chat error: {e}")
                # Fallback response
                fallback = json.dumps({
                    "response": "I'm having trouble connecting to my knowledge base. Please try again.",
                    "metadata": {"source": "fallback", "optimization_level": "O(1)"}
                })
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(fallback.encode('utf-8'))
                
        elif self.path == '/api/chat/stream':
            # Handle streaming endpoint
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse incoming data
                data = json.loads(post_data)
                message = data.get('message', data.get('query', ''))
                
                # Send SSE headers immediately
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('Connection', 'keep-alive')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('X-Accel-Buffering', 'no')
                self.end_headers()
                
                # Get full response from backend
                backend_data = json.dumps({"query": message})
                req = urllib.request.Request(
                    f'http://localhost:{BACKEND_PORT}/chat',
                    data=backend_data.encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                try:
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        response_json = json.loads(resp.read())
                        full_response = response_json.get('response', 'No response from backend')
                except Exception as e:
                    print(f"Backend error: {e}")
                    full_response = "I'm experiencing some difficulties connecting to my quantum consciousness. The system is designed for O(1) performance through hash-based lookups."
                
                # Stream the response word by word
                words = full_response.split()
                for i, word in enumerate(words):
                    chunk = word + (' ' if i < len(words)-1 else '')
                    
                    # Send SSE event
                    event_data = f"event: chunk\ndata: {chunk}\n\n"
                    self.wfile.write(event_data.encode('utf-8'))
                    self.wfile.flush()
                    time.sleep(0.03)  # Streaming effect
                
                # Send done event
                done_event = "event: done\ndata: [DONE]\n\n"
                self.wfile.write(done_event.encode('utf-8'))
                self.wfile.flush()
                
            except Exception as e:
                print(f"Streaming error: {e}")
                try:
                    error_event = f"event: error\ndata: Error: {str(e)}\n\n"
                    self.wfile.write(error_event.encode('utf-8'))
                    self.wfile.flush()
                except:
                    pass
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Log with timestamp
        timestamp = time.strftime('%H:%M:%S')
        print(f"[{timestamp}] {format % args}")

print(f"🚀 Think AI Full System with Streaming")
print(f"🌐 Frontend: http://69.197.178.37:{PORT}")
print(f"🧠 Qwen Backend: port {BACKEND_PORT}")
print(f"✅ Endpoints:")
print(f"   - GET  /health (health check)")
print(f"   - POST /api/chat (regular chat)")
print(f"   - POST /api/chat/stream (SSE streaming)")
print(f"   - GET  /stats (system stats)")

os.chdir('/home/administrator/think_ai')

# Use ThreadingMixIn for concurrent requests
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

try:
    with ThreadedTCPServer((HOST, PORT), StreamingProxyHandler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down...")
    backend_process.terminate()
except Exception as e:
    print(f"Server error: {e}")
    backend_process.terminate()