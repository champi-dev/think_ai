#!/usr/bin/env python3
"""Dead simple HTTP server for Railway testing."""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

# Immediately print to ensure the script is running
print("simple_server.py starting...", file=sys.stderr, flush=True)
print(f"Python executable: {sys.executable}", file=sys.stderr, flush=True)
print(f"Python version: {sys.version}", file=sys.stderr, flush=True)
print(f"Current directory: {os.getcwd()}", file=sys.stderr, flush=True)
print(f"Environment PORT: {os.environ.get('PORT', 'NOT SET')}", file=sys.stderr, flush=True)


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
        # Override to see logs - use stderr for Railway
        print(f"{self.address_string()} - {format % args}", file=sys.stderr, flush=True)


if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8080))
        print(f"Starting simple HTTP server on port {port}", file=sys.stderr, flush=True)
        print(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}", file=sys.stderr, flush=True)

        server = HTTPServer(("0.0.0.0", port), SimpleHandler)
        print(f"Server successfully bound to 0.0.0.0:{port}", file=sys.stderr, flush=True)

        print("Starting serve_forever()...", file=sys.stderr, flush=True)
        server.serve_forever()
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down server...", file=sys.stderr, flush=True)
        server.shutdown()
