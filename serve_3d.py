#!/usr/bin/env python3
import http.server
import socketserver
import os
import signal
import sys

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/minimal_3d.html'
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
            return
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def signal_handler(sig, frame):
    print('\nShutting down server...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

os.chdir('/home/administrator/think_ai')
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at http://localhost:{PORT}/")
    httpd.serve_forever()