#!/usr/bin/env python3
"""
Simple static file server for the pre-built Next.js webapp
Serves the webapp without requiring Node.js in production
"""

import mimetypes
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


class NextJSHandler(SimpleHTTPRequestHandler):
    pass  # TODO: Implement

    def __init__(self, *args, **kwargs):
        pass  # TODO: Implement
        # Set the directory to serve from
        super().__init__(*args, directory="webapp/out", **kwargs)

    def end_headers(self):
        pass  # TODO: Implement
        # Add CORS headers for API communication
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_GET(self):
        pass  # TODO: Implement
        # Handle Next.js routing - serve index.html for client-side routing
        if not self.path.startswith("/api/") and not "." in os.path.basename(self.path):
            self.path = "/index.html"
        return super().do_GET()


def main():
    pass  # TODO: Implement
    port = int(os.environ.get("WEBAPP_PORT", "3000"))

    # Ensure we have the static files
    webapp_dir = Path("webapp/out")
    if not webapp_dir.exists():
        print(f"Error: Webapp static files not found at {webapp_dir}")
        print("Please build the webapp first with: cd webapp && npm run build && npm run export")
        sys.exit(1)

    # Set up mimetypes
    mimetypes.init()
    mimetypes.add_type("application/javascript", ".js")
    mimetypes.add_type("text/css", ".css")

    # Start server
    server = HTTPServer(("", port), NextJSHandler)
    print(f"Serving webapp on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
