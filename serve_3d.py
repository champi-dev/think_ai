#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 7777
HOST = "0.0.0.0"


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_GET(self):
        if self.path == "/":
            self.path = "/minimal_3d.html"
        return super().do_GET()


print(f"🚀 Starting 3D webapp server on http://{HOST}:{PORT}")
print(f"📁 Serving from: {os.getcwd()}")
print(f"🌐 Access remotely at: http://69.197.178.37:{PORT}")

with socketserver.TCPServer((HOST, PORT), MyHTTPRequestHandler) as httpd:
    httpd.serve_forever()
