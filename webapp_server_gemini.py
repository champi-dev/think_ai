#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import time
import requests

PORT = 7777
HOST = "0.0.0.0"

# Gemini configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAFq-hpsSt4k_McDdWqIFt5ebPltLKNSRo")
GEMINI_MODEL = os.environ.get("MODEL_ID", "gemini-2.0-flash-exp")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Cache for responses
RESPONSE_CACHE = {}
try:
    with open("cache/response_cache.json", "r") as f:
        cache_data = json.load(f)
        for query, data in cache_data.items():
            if isinstance(data, dict) and 'response' in data:
                RESPONSE_CACHE[query.lower()] = data['response']
except:
    pass

def call_gemini(prompt):
    """Call Gemini API for AI response"""
    url = f"{GEMINI_BASE_URL}/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.9,
            "maxOutputTokens": 500
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                return data["candidates"][0]["content"]["parts"][0]["text"]
        elif response.status_code == 429:
            return "I'm experiencing high demand. Please try again in a moment."
        else:
            print(f"Gemini API error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Gemini API exception: {e}")
    
    return None

def find_response(query):
    """Find response using Gemini or cache"""
    query_lower = query.lower().strip().rstrip('?!.')
    
    # Check cache first
    if query_lower in RESPONSE_CACHE:
        return RESPONSE_CACHE[query_lower], "cache"
    
    # Try Gemini
    gemini_response = call_gemini(query)
    if gemini_response:
        # Cache the response for future use
        RESPONSE_CACHE[query_lower] = gemini_response
        return gemini_response, "gemini-2.0-flash-exp"
    
    # Fallback
    return "I'm here to help! Think AI provides intelligent responses across science, technology, philosophy and more. What would you like to know?", "fallback"

class WebAppHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open("webapp_temp_marked.html", "rb") as f:
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
            self.wfile.write(b"OK - Using Gemini 2.0 Flash")

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
                start_time = time.time()
                response_text, source = find_response(message)
                response_time = int((time.time() - start_time) * 1000)

                response_data = json.dumps({
                    "response": response_text,
                    "metadata": {
                        "source": source,
                        "model": GEMINI_MODEL if source == GEMINI_MODEL else source,
                        "response_time_ms": response_time
                    }
                })

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(response_data.encode("utf-8"))

            except Exception as e:
                print(f"Chat error: {e}")
                error_response = json.dumps({
                    "response": "I'm having trouble processing your request. Please try again.",
                    "metadata": {"source": "error", "error": str(e)}
                })
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(error_response.encode("utf-8"))

        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """Override to reduce logging noise"""
        if len(args) > 0 and isinstance(args[0], str):
            if "chat" in args[0] or "health" in args[0]:
                return
        print(f"{self.address_string()} - {format % args}")

# Main server
if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), WebAppHandler) as httpd:
        print(f"Think AI server (Gemini-powered) running at http://{HOST}:{PORT}")
        print(f"Using Gemini model: {GEMINI_MODEL}")
        print(f"API Key configured: {'Yes' if GEMINI_API_KEY else 'No'}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")