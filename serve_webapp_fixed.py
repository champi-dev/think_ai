# \!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import urllib.request

PORT = 7777
HOST = "0.0.0.0"


class FixedWebAppHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            with open("minimal_3d.html", "r") as f:
                content = f.read()

            # Fix: Force sendQuery to skip streaming
            content = content.replace(
                "async function sendQuery(useStreaming = true) {",
                "async function sendQuery(useStreaming = false) { // FIXED: Force non-streaming",
            )

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content.encode())

        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"OK - Fixed Server Running")

    def do_POST(self):
        if self.path in ["/api/chat", "/api/chat/stream"]:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            # Forward to the actual Think AI backend
            req = urllib.request.Request(
                "http://69.197.178.37:7777/api/chat",
                data=post_data,
                headers={"Content-Type": "application/json"},
            )

            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    response_data = resp.read()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(response_data)
            except Exception as e:
                error_response = json.dumps(
                    {"response": f"Error: {str(e)}", "metadata": {"source": "error"}}
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(error_response.encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        if args[1] != "200":
            print(f"{format % args}")


print(f"🚀 Fixed webapp server starting on port {PORT}")
print("✅ This version forces non-streaming mode")
print(f"📡 Proxying to http://69.197.178.37:7777/api/chat")

os.chdir("/home/administrator/think_ai")
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer((HOST, PORT), FixedWebAppHandler) as httpd:
    print(f"\n🌐 Fixed server ready at http://localhost:{PORT}")
    httpd.serve_forever()
