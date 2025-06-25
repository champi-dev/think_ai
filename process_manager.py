#!/usr/bin/env python3
"""Process manager for running multiple services on Railway with a single PORT."""

import os
import sys
import subprocess
import threading
import time
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection
from urllib.parse import urlparse, parse_qs
import json
from think_ai.utils.progress import O1ProgressBar, progress_context

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ReverseProxyHandler(BaseHTTPRequestHandler):
    """Simple reverse proxy to route requests to appropriate services."""

    def do_GET(self):
        self._proxy_request()

    def do_POST(self):
        self._proxy_request()

    def do_PUT(self):
        self._proxy_request()

    def do_DELETE(self):
        self._proxy_request()

    def do_HEAD(self):
        self._proxy_request()

    def do_OPTIONS(self):
        self._proxy_request()

    def _proxy_request(self):
        """Route requests to the appropriate backend service."""
        # Determine target based on path
        if self.path.startswith("/api/") or self.path == "/health":
            # Route to API server
            target_host = "localhost"
            target_port = 8081
        else:
            # Route to webapp
            target_host = "localhost"
            target_port = 3000

        # Create connection to target
        conn = HTTPConnection(target_host, target_port)

        # Get request body if present
        content_length = self.headers.get("Content-Length")
        body = None
        if content_length:
            body = self.rfile.read(int(content_length))

        # Forward the request
        try:
            # Copy headers
            headers = {}
            for key, value in self.headers.items():
                if key.lower() not in ["host", "connection"]:
                    headers[key] = value
            headers["Host"] = f"{target_host}:{target_port}"

            # Make request
            conn.request(self.command, self.path, body=body, headers=headers)

            # Get response
            response = conn.getresponse()

            # Send response status
            self.send_response(response.status)

            # Copy response headers
            for key, value in response.getheaders():
                if key.lower() not in ["connection", "transfer-encoding"]:
                    self.send_header(key, value)
            self.end_headers()

            # Copy response body
            while True:
                chunk = response.read(4096)
                if not chunk:
                    break
                self.wfile.write(chunk)

        except Exception as e:
            logger.error(f"Proxy error: {e}")
            self.send_error(502, f"Bad Gateway: {str(e)}")
        finally:
            conn.close()

    def log_message(self, format, *args):
        """Override to use our logger."""
        logger.info(f"{self.address_string()} - {format % args}")


def start_service(name, command, cwd=None, env=None, progress_bar=None):
    """Start a service in the background."""
    logger.info(f"Starting {name}...")
    
    if progress_bar:
        progress_bar.update(0, f"Starting {name}...")

    process = subprocess.Popen(
        command, cwd=cwd, env=env or os.environ.copy(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Start threads to log output
    def log_output(pipe, prefix):
        for line in iter(pipe.readline, b""):
            logger.info(f"[{prefix}] {line.decode().strip()}")

    threading.Thread(target=log_output, args=(process.stdout, name), daemon=True).start()

    threading.Thread(target=log_output, args=(process.stderr, f"{name}-err"), daemon=True).start()

    return process


def main():
    """Main entry point."""
    # Get the main port from Railway
    main_port = int(os.environ.get("PORT", "8080"))

    logger.info(f"Starting Think AI Full System on Railway port {main_port}")

    # Use progress bar for startup
    with progress_context(total=3, description="Starting Think AI services") as pbar:
        # Start the API server on internal port 8081
        api_env = os.environ.copy()
        api_env["PORT"] = "8081"
        api_process = start_service("API", [sys.executable, "think_ai_full.py"], env=api_env, progress_bar=pbar)
        
        # Wait for API to start
        for i in range(5):
            time.sleep(1)
            if i == 4:
                pbar.update(1, "API server started")
        
        # Start the webapp on internal port 3000
        webapp_env = os.environ.copy()
        webapp_env["PORT"] = "3000"
        webapp_env["NODE_ENV"] = "production"
        webapp_env["NEXT_PUBLIC_API_URL"] = "http://localhost:8081"
        
        webapp_process = start_service("Webapp", ["npm", "start"], cwd="webapp", env=webapp_env, progress_bar=pbar)
        
        # Wait for webapp to start
        for i in range(10):
            time.sleep(1)
            if i == 9:
                pbar.update(1, "Webapp started")
        
        # Start the reverse proxy on the main Railway port
        logger.info(f"Starting reverse proxy on port {main_port}")
        httpd = HTTPServer(("0.0.0.0", main_port), ReverseProxyHandler)
        
        # Start proxy in a thread
        proxy_thread = threading.Thread(target=httpd.serve_forever)
        proxy_thread.daemon = True
        proxy_thread.start()
        
        pbar.update(1, "Reverse proxy started")
    
    logger.info("All services started successfully!")
    logger.info(f"System accessible at: http://0.0.0.0:{main_port}")

    # Monitor processes
    try:
        while True:
            # Check if processes are still running
            if api_process.poll() is not None:
                logger.error("API process died!")
                sys.exit(1)

            if webapp_process.poll() is not None:
                logger.error("Webapp process died!")
                sys.exit(1)

            time.sleep(5)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
        api_process.terminate()
        webapp_process.terminate()
        httpd.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()
