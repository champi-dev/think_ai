#\!/usr/bin/env python3
import http.server
import socketserver
import json
import time
import urllib.request

PORT = 7777

class StreamingHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            with open('minimal_3d.html', 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(content)
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK - Streaming Server Running')
    
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                req = urllib.request.Request(
                    'http://69.197.178.37:7777/api/chat',
                    data=post_data,
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    response_data = resp.read()
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response_data)
            except Exception as e:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'response': str(e)}).encode())
                
        elif self.path == '/api/chat/stream':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                req = urllib.request.Request(
                    'http://69.197.178.37:7777/api/chat',
                    data=post_data,
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    response_json = json.loads(resp.read())
                    full_response = response_json.get('response', 'No response')
                
                words = full_response.split()
                for i, word in enumerate(words):
                    chunk = word + (' ' if i < len(words)-1 else '')
                    self.wfile.write(f'event: chunk\ndata: {chunk}\n\n'.encode())
                    self.wfile.flush()
                    time.sleep(0.03)
                
                self.wfile.write(b'event: done\ndata: [DONE]\n\n')
                self.wfile.flush()
                
            except Exception as e:
                self.wfile.write(f'event: error\ndata: {str(e)}\n\n'.encode())
                self.wfile.flush()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        pass

print(f'Starting streaming server on port {PORT}...')
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(('', PORT), StreamingHandler) as httpd:
    print(f'✅ Server ready at http://localhost:{PORT}')
    print('🌊 Streaming endpoint: POST /api/chat/stream')
    httpd.serve_forever()
