#\!/usr/bin/env python3
import http.server
import socketserver
import json

PORT = 5555

class FixedHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            html = '''<\!DOCTYPE html>
<html>
<head>
    <title>Think AI - Fixed Version</title>
    <style>
        body { background: #0a0a0a; color: #fff; font-family: monospace; padding: 20px; }
        #messages { height: 400px; overflow-y: auto; border: 1px solid #333; padding: 10px; margin: 20px 0; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #1a3a52; color: #3b82f6; }
        .ai { background: #0a3a2a; color: #10b981; }
        input { width: 70%; padding: 10px; background: #1a1a1a; border: 1px solid #333; color: #fff; }
        button { padding: 10px 20px; background: #3b82f6; border: none; color: #fff; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Think AI - Working Version</h1>
    <div id="messages"></div>
    <div>
        <input type="text" id="input" placeholder="Ask me anything...">
        <button onclick="send()">Send</button>
    </div>
    
    <script>
        const messages = document.getElementById('messages');
        const input = document.getElementById('input');
        
        function addMsg(text, type) {
            const div = document.createElement('div');
            div.className = 'message ' + type;
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
        
        async function send() {
            const msg = input.value.trim();
            if (\!msg) return;
            
            addMsg('You: ' + msg, 'user');
            input.value = '';
            
            try {
                const res = await fetch('http://69.197.178.37:7777/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                const data = await res.json();
                addMsg('AI: ' + (data.response || 'No response'), 'ai');
            } catch (e) {
                addMsg('Error: ' + e.message, 'ai');
            }
        }
        
        input.addEventListener('keypress', e => {
            if (e.key === 'Enter') send();
        });
        
        input.focus();
    </script>
</body>
</html>'''
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass

print(f"Starting fixed webapp on http://localhost:{PORT}")
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), FixedHandler) as httpd:
    print(f"Server ready\! Open http://localhost:{PORT} in your browser")
    httpd.serve_forever()
