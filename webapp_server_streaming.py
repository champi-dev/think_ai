#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import subprocess
import time
import urllib.request

PORT = 7777
HOST = "0.0.0.0"

# Kill any existing backend
os.system("pkill -f stable-server 2>/dev/null || true")
time.sleep(1)

# Start the stable server on a different internal port
BACKEND_PORT = 8888
print(f"Starting backend on port {BACKEND_PORT}...")
backend_env = os.environ.copy()
backend_env["PORT"] = str(BACKEND_PORT)
subprocess.Popen(
    ["./target/release/stable-server"],
    env=backend_env,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(3)

class StreamingWebAppHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            try:
                with open('minimal_3d.html', 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                print(f"Error: {e}")
                self.send_error(500)
                
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b"OK - Streaming Server Running")
                
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path in ['/api/chat', '/chat']:
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
                    response_data = resp.read()
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(response_data)
                    
            except Exception as e:
                print(f"Chat error: {e}")
                error_response = json.dumps({
                    "response": "I'm having trouble connecting. Please try again.",
                    "metadata": {"source": "error", "optimization_level": "O(1)"}
                })
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(error_response.encode('utf-8'))
                
        elif self.path == '/api/chat/stream':
            # Proper SSE streaming endpoint
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse incoming data
                data = json.loads(post_data)
                message = data.get('message', data.get('query', ''))
                
                # Send SSE headers
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('Connection', 'keep-alive')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('X-Accel-Buffering', 'no')  # Disable Nginx buffering
                self.end_headers()
                
                # Get full response from backend
                backend_data = json.dumps({"query": message})
                req = urllib.request.Request(
                    f'http://localhost:{BACKEND_PORT}/chat',
                    data=backend_data.encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req, timeout=30) as resp:
                    response_json = json.loads(resp.read())
                    full_response = response_json.get('response', 'No response')
                
                # Stream the response word by word
                words = full_response.split()
                for i, word in enumerate(words):
                    chunk = word + (' ' if i < len(words)-1 else '')
                    
                    # Send SSE event
                    event_data = f"event: chunk\ndata: {chunk}\n\n"
                    self.wfile.write(event_data.encode('utf-8'))
                    self.wfile.flush()
                    time.sleep(0.03)  # Small delay for streaming effect
                
                # Send done event
                done_event = "event: done\ndata: [DONE]\n\n"
                self.wfile.write(done_event.encode('utf-8'))
                self.wfile.flush()
                
            except Exception as e:
                print(f"Streaming error: {e}")
                error_event = f"event: error\ndata: Error: {str(e)}\n\n"
                try:
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
        # Only log errors
        if args and len(args) > 1 and args[1] != '200':
            print(format % args)

print(f"🚀 Think AI Streaming Server starting on http://{HOST}:{PORT}")
print(f"🌐 Access at: http://69.197.178.37:{PORT}")
print(f"✅ Backend on port {BACKEND_PORT}")
print(f"🌊 Streaming endpoint: POST /api/chat/stream (SSE)")
print(f"💬 Regular endpoint: POST /api/chat")

os.chdir('/home/administrator/think_ai')

with socketserver.TCPServer((HOST, PORT), StreamingWebAppHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        os.system("pkill -f stable-server")