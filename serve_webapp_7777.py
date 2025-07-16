#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.request
import urllib.error
import subprocess
import time
import sys
import os

PORT = 7777
BACKEND_PORT = 7778

# Start backend server
print(f"Starting backend server on port {BACKEND_PORT}...")
backend_env = os.environ.copy()
backend_env["PORT"] = str(BACKEND_PORT)
backend_proc = subprocess.Popen(
    ["./target/release/stable-server-streaming"],
    env=backend_env,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(3)  # Wait for backend to start


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open("webapp_temp.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                print(f"Error serving webapp: {e}")
                self.send_error(500, f"Error: {e}")
        elif self.path == "/health":
            # Check backend health
            try:
                urllib.request.urlopen(
                    f"http://localhost:{BACKEND_PORT}/health", timeout=2
                )
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b"OK")
            except:
                self.send_error(503, "Backend not available")
        elif self.path == "/stats":
            # Proxy to backend
            self.proxy_request(f"http://localhost:{BACKEND_PORT}/stats")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path in ["/chat", "/api/chat"]:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            # Proxy to backend /chat endpoint
            self.proxy_request(f"http://localhost:{BACKEND_PORT}/chat", post_data)
        elif self.path == "/api/chat/stream":
            # Proxy to streaming endpoint
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            self.proxy_streaming_request(
                f"http://localhost:{BACKEND_PORT}/chat/stream", post_data
            )
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def proxy_request(self, url, data=None):
        try:
            req = urllib.request.Request(url)
            if data:
                req.add_header("Content-Type", "application/json")
                req.data = data

            response = urllib.request.urlopen(req, timeout=30)

            self.send_response(response.getcode())
            for header, value in response.headers.items():
                if header.lower() not in ["connection", "transfer-encoding"]:
                    self.send_header(header, value)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response.read())
        except urllib.error.HTTPError as e:
            self.send_error(e.code, e.reason)
        except Exception as e:
            print(f"Proxy error: {e}")
            self.send_error(502, str(e))

    def proxy_streaming_request(self, url, data):
        try:
            req = urllib.request.Request(url)
            req.add_header("Content-Type", "application/json")
            req.add_header("Accept", "text/event-stream")
            req.data = data

            # Open streaming response
            response = urllib.request.urlopen(req)

            # Send SSE headers
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            # Stream the response
            while True:
                chunk = response.read(1024)
                if not chunk:
                    break
                self.wfile.write(chunk)
                self.wfile.flush()

        except Exception as e:
            print(f"Streaming proxy error: {e}")
            self.send_error(502, str(e))

    def log_message(self, format, *args):
        # Only log non-health check requests
        if "/health" not in self.path:
            super().log_message(format, *args)


try:
    print(f"Starting webapp server on http://0.0.0.0:{PORT}")
    print(f"Backend running on http://localhost:{BACKEND_PORT}")

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"\n✅ Think AI webapp is ready at http://0.0.0.0:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down...")
    backend_proc.terminate()
    sys.exit(0)
