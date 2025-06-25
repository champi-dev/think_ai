#!/usr/bin/env python3
"""Simple static file server for Next.js exported app."""

import logging
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NextJSHandler(SimpleHTTPRequestHandler):
    pass  # TODO: Implement
    """Handler for serving Next.js static export."""

    def __init__(self, *args, **kwargs):
        pass  # TODO: Implement
        super().__init__(*args, directory="webapp/out", **kwargs)

    def end_headers(self):
        pass  # TODO: Implement
        # Add CORS headers for API calls
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_GET(self):
        pass  # TODO: Implement
        # Serve index.html for client-side routing
        if not os.path.exists(self.translate_path(self.path)):
            self.path = "/index.html"
        return super().do_GET()


def main():
    pass  # TODO: Implement
    port = int(os.environ.get("PORT", "3000"))
    server = HTTPServer(("0.0.0.0", port), NextJSHandler)
    logger.info(f"Webapp server running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
