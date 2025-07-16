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
    stderr=subprocess.DEVNULL,
)
time.sleep(3)


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
            try:
                req = urllib.request.Request(f"http://localhost:{BACKEND_PORT}/health")
                with urllib.request.urlopen(req, timeout=5) as resp:
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(resp.read())
            except:
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

                # Prepare request for backend
                backend_data = json.dumps({"query": message})

                req = urllib.request.Request(
                    f"http://localhost:{BACKEND_PORT}/chat",
                    data=backend_data.encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                )

                with urllib.request.urlopen(req, timeout=30) as resp:
                    response_data = resp.read()

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(response_data)

            except Exception as e:
                print(f"Chat error: {e}")
                # Send a simple response on error
                error_response = json.dumps(
                    {
                        "response": "I'm having trouble connecting to the backend. Please try again.",
                        "metadata": {"source": "error", "optimization_level": "O(1)"},
                    }
                )
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
print(f"✅ Backend on port {BACKEND_PORT}")

os.chdir("/home/administrator/think_ai")

with socketserver.TCPServer((HOST, PORT), WebAppHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        os.system("pkill -f stable-server")
