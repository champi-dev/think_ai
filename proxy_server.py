#!/usr/bin/env python3
import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import os

PORT = 9090
BACKEND = "http://localhost:8080"


class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/minimal_3d.html"
        elif self.path == "/health":
            # Proxy health check to backend
            try:
                with urllib.request.urlopen(f"{BACKEND}/health") as response:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()
                    self.wfile.write(response.read())
                return
            except:
                self.send_error(503, "Backend unavailable")
                return

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path in ["/api/chat", "/api/chat/stream"]:
            # Read request body
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            # Forward to backend
            try:
                req = urllib.request.Request(
                    f"{BACKEND}{self.path}",
                    data=post_data,
                    headers={
                        "Content-Type": "application/json",
                        "Content-Length": str(content_length),
                    },
                    method="POST",
                )

                with urllib.request.urlopen(req) as response:
                    # Forward response
                    self.send_response(response.getcode())
                    for header, value in response.headers.items():
                        if header.lower() not in ["connection", "transfer-encoding"]:
                            self.send_header(header, value)
                    self.end_headers()

                    # For streaming, forward chunks as they arrive
                    if self.path == "/api/chat/stream":
                        while True:
                            chunk = response.read(1024)
                            if not chunk:
                                break
                            self.wfile.write(chunk)
                            self.wfile.flush()
                    else:
                        self.wfile.write(response.read())
            except urllib.error.HTTPError as e:
                self.send_error(e.code, e.reason)
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, "Not found")


os.chdir("/home/administrator/think_ai")


class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


print(f"Starting proxy server on port {PORT}")
print(f"Serving static files from current directory")
print(f"Proxying API requests to {BACKEND}")

with ReuseAddrTCPServer(("", PORT), ProxyHTTPRequestHandler) as httpd:
    httpd.serve_forever()
