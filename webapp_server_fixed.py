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

# Don't start any backend - we'll handle responses directly
# Load the fixed response cache
RESPONSE_CACHE = {}
try:
    with open("cache/response_cache.json", "r") as f:
        cache_data = json.load(f)
        for query, data in cache_data.items():
            if isinstance(data, dict) and 'response' in data:
                RESPONSE_CACHE[query.lower()] = data['response']
except:
    pass

# Add defaults
RESPONSE_CACHE.update({
    "ping": "Pong! I'm here and ready to help. How can I assist you today?",
    "hello": "Hello! I'm Think AI, ready to help you with any questions about science, technology, philosophy, or any other topic. What would you like to know?",
})

def find_response(query):
    """Find best matching response"""
    query_lower = query.lower().strip().rstrip('?!.')
    
    # Direct match
    if query_lower in RESPONSE_CACHE:
        return RESPONSE_CACHE[query_lower]
    
    # Partial match
    for key, response in RESPONSE_CACHE.items():
        if query_lower in key or key in query_lower:
            return response
    
    # Default
    return "I'm here to help! Think AI provides intelligent responses across science, technology, philosophy and more. What would you like to know?"

class WebAppHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open("minimal_3d.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                print(f"Error: {e}")
                self.send_error(500)

        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"OK")

        else:
            self.send_error(404)

    def do_POST(self):
        if self.path in ["/api/chat", "/chat"]:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            try:
                # Parse incoming data
                data = json.loads(post_data)
                message = data.get("message", data.get("query", ""))

                # Get response
                response_text = find_response(message)

                response_data = json.dumps({
                    "response": response_text,
                    "metadata": {"source": "cache", "optimization_level": "O(1)"}
                })

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(response_data.encode("utf-8"))

            except Exception as e:
                print(f"Chat error: {e}")
                error_response = json.dumps({
                    "response": "I'm having trouble connecting. Please try again.",
                    "metadata": {"source": "error"}
                })
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(error_response.encode("utf-8"))

        elif self.path == "/api/chat/stream":
            # Fallback to regular chat
            self.path = "/api/chat"
            self.do_POST()
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        return  # Suppress logs


print(f"🚀 Think AI webapp running on http://{HOST}:{PORT}")
print(f"🌐 Access at: http://69.197.178.37:{PORT}")
print(f"✅ Using fixed response cache")

os.chdir("/home/administrator/think_ai")

with socketserver.TCPServer((HOST, PORT), WebAppHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")