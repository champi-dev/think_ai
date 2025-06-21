#!/usr/bin/env python3
"""Dead simple HTTP server for Railway testing."""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "healthy", "service": "think-ai-railway"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Think AI Railway Server is running!")

    def log_message(self, format, *args):
        # Override to see logs
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting simple HTTP server on port {port}")

    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"Server listening on 0.0.0.0:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
