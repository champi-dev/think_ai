# \!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 7778
HOST = "0.0.0.0"


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/minimal_3d.html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        http.server.SimpleHTTPRequestHandler.end_headers(self)


print(f"🚀 Starting Think AI 3D webapp on http://{HOST}:{PORT}")
print(f"🌐 Access remotely at: http://69.197.178.37:{PORT}")
print(f"📁 Serving minimal_3d.html as default page")

with socketserver.TCPServer((HOST, PORT), CustomHandler) as httpd:
    httpd.serve_forever()
