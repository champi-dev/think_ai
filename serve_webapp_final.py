# \!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import sys
import os
import signal


def signal_handler(sig, frame):
    print("\nShutting down server...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


class WebAppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()

            # Serve the fixed HTML with explicit non-streaming behavior
            with open("minimal_3d.html", "r") as f:
                content = f.read()

            # Force non-streaming by modifying the sendQuery function
            fix = """
        async function sendQuery(useStreaming = false) {  // FORCE FALSE
            const query = queryInput.value.trim();
            if (\!query) return;
            
            addMessage(query, true);
            queryInput.value = '';
            
            const loadingMsg = addLoadingMessage();
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: query })
                });
                
                const data = await response.json();
                removeLoadingMessage();
                
                if (data && data.response) {
                    addMessage(data.response);
                } else {
                    addMessage('Error: No response from server');
                }
            } catch (error) {
                removeLoadingMessage();
                addMessage('Error: ' + error.message);
            }
        }"""

            # Replace the complex sendQuery with simple version
            content = content.replace(
                "async function sendQuery(useStreaming = true) {",
                fix + "\n\n        async function OLD_sendQuery(useStreaming = true) {",
            )

            self.wfile.write(content.encode())

        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            # Forward to the actual backend
            req = urllib.request.Request(
                "http://localhost:7777/api/chat",
                data=post_data,
                headers={"Content-Type": "application/json"},
            )

            try:
                with urllib.request.urlopen(req) as response:
                    response_data = response.read()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(response_data)
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


PORT = 3456
server = HTTPServer(("", PORT), WebAppHandler)
print(f"🚀 Fixed webapp server running at http://localhost:{PORT}")
print("This version forces non-streaming mode to ensure responses are displayed")
server.serve_forever()
