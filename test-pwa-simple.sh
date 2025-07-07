#!/bin/bash
set -e

echo "🌐 Testing Think AI PWA with Simple Server"
echo "========================================="

# Kill any existing processes on port 8080
echo "🔧 Cleaning up port 8080..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
sleep 1

# Copy PWA files to static directory
echo "📦 Setting up PWA files..."
mkdir -p static/icons
cp -f think-ai-webapp/static/manifest.json static/
cp -f think-ai-webapp/static/sw.js static/
cp -f think-ai-webapp/static/offline.html static/
cp -f think-ai-webapp/static/pwa.html static/index.html
cp -f think-ai-webapp/static/icons/* static/icons/ 2>/dev/null || true

# Create a simple PWA server script
cat > serve-pwa.py << 'EOF'
#!/usr/bin/env python3
import http.server
import socketserver
import json
from urllib.parse import urlparse

class PWAHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        
        # Serve PWA files with correct headers
        if path == '/':
            self.path = '/index.html'
        elif path == '/sw.js':
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.send_header('Service-Worker-Allowed', '/')
            self.end_headers()
            with open('static/sw.js', 'rb') as f:
                self.wfile.write(f.read())
            return
        elif path == '/manifest.json':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            with open('static/manifest.json', 'rb') as f:
                self.wfile.write(f.read())
            return
            
        # Default file serving
        super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # Simple response for testing
            response = {
                "response": f"O(1) Response: I received your message '{data['message']}'. This is a PWA test response with O(1) performance!",
                "processing_time": 0.001,
                "confidence": 0.95
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

PORT = 8080
with socketserver.TCPServer(("", PORT), PWAHandler) as httpd:
    print(f"🚀 PWA Server running at http://localhost:{PORT}")
    print("📱 Features: Install prompt, offline support, service worker")
    print("🔧 DevTools: Check Application tab for PWA features")
    print("\nPress Ctrl+C to stop...")
    httpd.serve_forever()
EOF

# Run the PWA server
echo -e "\n🚀 Starting Think AI PWA server..."
python3 serve-pwa.py