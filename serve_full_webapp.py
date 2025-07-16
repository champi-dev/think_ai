#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
from urllib.parse import urlparse

PORT = 7777
HOST = "0.0.0.0"


class FullWebAppHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            # Serve minimal_3d.html for root path
            try:
                with open("minimal_3d.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(content))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                print(f"Error serving webapp: {e}")

        elif self.path == "/health":
            # Simple health check
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"OK - Think AI Server Running")
            return

        # For other paths, use default handler
        return super().do_GET(self)

    def do_POST(self):
        if self.path == "/api/chat":
            # Handle chat requests with a simple response
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data)
                query = data.get("message", "")  # webapp sends 'message' field

                # Simple response for now
                response = {
                    "response": f"Hello! You said: '{query}'. The Think AI system is running with O(1) performance!",
                    "metadata": {
                        "response_time_ms": 0.5,
                        "source": "demo",
                        "optimization_level": "O(1)",
                    },
                }

                response_json = json.dumps(response)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Content-length", len(response_json))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(response_json.encode())

            except Exception as e:
                print(f"Error handling chat: {e}")
                self.send_error(500, "Internal Server Error")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


os.chdir("/home/administrator/think_ai")
print(f"🚀 Starting Think AI Full Webapp on http://{HOST}:{PORT}")
print(f"🌐 Access remotely at: http://69.197.178.37:{PORT}")
print(f"📁 Serving minimal_3d.html with API endpoints")

try:
    with socketserver.TCPServer((HOST, PORT), FullWebAppHandler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n👋 Server stopped")
except Exception as e:
    print(f"Error: {e}")
