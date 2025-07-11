#!/usr/bin/env python3
import http.server
import socketserver
import os
import socket

PORT = 9090

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/minimal_3d.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

os.chdir('/home/administrator/think_ai')

class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

try:
    with ReuseAddrTCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        httpd.serve_forever()
except Exception as e:
    print(f"Error: {e}")
    # Try to force close and restart
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", PORT))
    sock.close()
    with ReuseAddrTCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        httpd.serve_forever()