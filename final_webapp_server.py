#\!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.request
import sys
import os

PORT = 7777

# Change to the correct directory
os.chdir('/home/administrator/think_ai')

class ThinkAIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            try:
                with open('minimal_3d.html', 'rb') as f:
                    self.wfile.write(f.read())
            except:
                self.wfile.write(b'<h1>Think AI</h1><p>HTML file not found</p>')
                
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK - Server Running')
    
    def do_POST(self):
        if self.path in ['/api/chat', '/api/chat/stream']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse request
                data = json.loads(post_data)
                message = data.get('message', '')
                
                # Try to call the backend
                try:
                    backend_req = json.dumps({"query": message})
                    req = urllib.request.Request(
                        'http://localhost:8888/chat',
                        data=backend_req.encode('utf-8'),
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        backend_response = json.loads(resp.read())
                        
                    # Return the backend response
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(backend_response).encode())
                    
                except Exception as backend_error:
                    # If backend fails, return a simple response
                    response = {
                        "response": f"I understand you asked: '{message}'. The answer is 42.",
                        "metadata": {"source": "fallback", "error": str(backend_error)}
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                    
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'Error: {e}'.encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Only log errors
        if len(args) > 1 and '200' not in str(args[1]):
            sys.stderr.write(format % args + '\n')

# Start server
print(f"Starting Think AI server on port {PORT}")
socketserver.TCPServer.allow_reuse_address = True

try:
    with socketserver.TCPServer(("", PORT), ThinkAIHandler) as httpd:
        print(f"Server ready at http://localhost:{PORT}")
        print(f"Access at http://69.197.178.37:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down...")
except Exception as e:
    print(f"Error: {e}")
