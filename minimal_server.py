import http.server
import socketserver
import json

PORT = 7777


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("minimal_3d.html", "rb") as f:
                self.wfile.write(f.read())

    def do_POST(self):
        if "/chat" in self.path:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"response": "Server is working\!"}).encode())

    def log_message(self, *args):
        pass


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), H) as httpd:
    print(f"Server on {PORT}")
    httpd.serve_forever()
