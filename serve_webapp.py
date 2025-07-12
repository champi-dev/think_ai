#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 7777
HOST = "0.0.0.0"

class WebAppHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve minimal_3d.html for root path
            try:
                with open('minimal_3d.html', 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-length', len(content))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
                return
            except:
                pass
        # For all other paths, use default handler
        return super().do_GET(self)

os.chdir('/home/administrator/think_ai')
print(f"🚀 Starting Think AI 3D webapp on http://{HOST}:{PORT}")
print(f"🌐 Access remotely at: http://69.197.178.37:{PORT}")
print(f"📁 Serving minimal_3d.html at root /")

with socketserver.TCPServer((HOST, PORT), WebAppHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")