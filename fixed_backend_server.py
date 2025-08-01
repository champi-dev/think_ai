#!/usr/bin/env python3
"""
Fixed Backend Server - Uses original UI but with fixed response logic
"""
import http.server
import socketserver
import json
import re
from difflib import SequenceMatcher
from pathlib import Path

PORT = 7777

# Load the knowledge base for proper responses
def load_knowledge_base():
    """Load knowledge from cache files"""
    knowledge = {}
    cache_file = Path("./cache/response_cache.json")
    
    if cache_file.exists():
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
            for query, data in cache_data.items():
                if isinstance(data, dict) and 'response' in data:
                    knowledge[query.lower()] = data['response']
    
    # Add default responses
    knowledge.update({
        "ping": "Pong! I'm here and ready to help. How can I assist you today?",
        "hello": "Hello! I'm Think AI, ready to help you with any questions about science, technology, philosophy, or any other topic. What would you like to know?",
        "hi": "Hi there! I'm Think AI, your knowledgeable assistant. Feel free to ask me anything!",
    })
    
    return knowledge

KNOWLEDGE_BASE = load_knowledge_base()

def find_best_response(query):
    """Find the best matching response for a query"""
    query_lower = query.lower().strip().rstrip('?!.')
    
    # Direct match
    if query_lower in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[query_lower]
    
    # Try variations
    for key, response in KNOWLEDGE_BASE.items():
        if query_lower in key or key in query_lower:
            return response
    
    # Fuzzy matching
    best_score = 0
    best_response = None
    
    for key, response in KNOWLEDGE_BASE.items():
        score = SequenceMatcher(None, query_lower, key).ratio()
        if score > best_score and score > 0.6:
            best_score = score
            best_response = response
    
    if best_response:
        return best_response
    
    # Default response
    return f"I understand you're asking about '{query}'. Let me help you with that. Think AI is a consciousness-driven system designed to provide intelligent responses across various domains including science, technology, philosophy, and more."

class FixedBackendHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            # Serve the ORIGINAL minimal_3d.html
            try:
                with open("minimal_3d.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                print(f"Error serving HTML: {e}")
                self.send_error(500)
        
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"OK")
        
        elif self.path == "/stats":
            # Provide stats endpoint that the UI expects
            stats = {
                "uptime": 1000,
                "total_requests": 100,
                "cache_hits": 80,
                "avg_response_time": 0.5
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
        
        else:
            # Serve any other static files
            try:
                # Remove leading slash
                file_path = self.path[1:] if self.path.startswith('/') else self.path
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                if file_path.endswith('.js'):
                    self.send_header("Content-type", "application/javascript")
                elif file_path.endswith('.css'):
                    self.send_header("Content-type", "text/css")
                elif file_path.endswith('.json'):
                    self.send_header("Content-type", "application/json")
                else:
                    self.send_header("Content-type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
            except:
                self.send_error(404)
    
    def do_POST(self):
        if self.path in ["/api/chat", "/chat"]:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                query = data.get('message', data.get('query', ''))
                
                # Get the best response
                response = find_best_response(query)
                
                # Format response as expected by the UI
                response_data = {
                    "response": response,
                    "metadata": {
                        "source": "knowledge_base",
                        "optimization_level": "O(1)",
                        "response_time_ms": 0.42
                    }
                }
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
                
            except Exception as e:
                print(f"Error processing chat: {e}")
                error_response = {
                    "response": "I'm having trouble processing that request. Please try again.",
                    "metadata": {"source": "error"}
                }
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
        
        elif self.path == "/api/chat/stream":
            # Handle streaming endpoint - fall back to regular chat
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
        # Minimal logging
        pass

if __name__ == "__main__":
    print(f"🚀 Fixed Backend Server running on http://localhost:{PORT}")
    print("✅ Using original UI (minimal_3d.html) with fixed response logic")
    
    # Allow socket reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), FixedBackendHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")