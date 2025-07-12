#\!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.request
from http import HTTPStatus

class DebugHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = '''<\!DOCTYPE html>
<html>
<head>
    <title>Debug Think AI</title>
    <style>
        body { font-family: monospace; padding: 20px; background: #1a1a1a; color: #fff; }
        button { padding: 10px; margin: 10px; }
        #messages { border: 1px solid #333; padding: 10px; margin: 10px 0; min-height: 200px; }
        .message { margin: 5px 0; padding: 5px; }
        .user { color: #3b82f6; }
        .ai { color: #10b981; }
        .error { color: #ef4444; }
        .debug { color: #facc15; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>Think AI Debug Interface</h1>
    <input type="text" id="input" placeholder="Type a message..." style="width: 300px; padding: 10px;">
    <button onclick="sendMessage()">Send</button>
    <button onclick="clearMessages()">Clear</button>
    <div id="messages"></div>
    
    <script>
        const messages = document.getElementById('messages');
        const input = document.getElementById('input');
        
        function addMessage(content, className = '') {
            const msg = document.createElement('div');
            msg.className = 'message ' + className;
            msg.textContent = content;
            messages.appendChild(msg);
            messages.scrollTop = messages.scrollHeight;
        }
        
        function addDebug(content) {
            addMessage('[DEBUG] ' + content, 'debug');
        }
        
        async function sendMessage() {
            const query = input.value.trim();
            if (\!query) return;
            
            addMessage('User: ' + query, 'user');
            input.value = '';
            
            addDebug('Sending request to /api/chat...');
            
            try {
                const response = await fetch('http://69.197.178.37:7777/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: query})
                });
                
                addDebug('Response status: ' + response.status);
                
                const data = await response.json();
                addDebug('Response data: ' + JSON.stringify(data));
                
                if (data.response) {
                    addMessage('AI: ' + data.response, 'ai');
                } else {
                    addMessage('ERROR: No response field in data', 'error');
                    addDebug('Full data object: ' + JSON.stringify(data, null, 2));
                }
            } catch (error) {
                addMessage('ERROR: ' + error.message, 'error');
                addDebug('Error details: ' + error.stack);
            }
        }
        
        function clearMessages() {
            messages.innerHTML = '';
            addDebug('Messages cleared');
        }
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        addDebug('Debug interface ready');
        addDebug('API endpoint: http://69.197.178.37:7777/api/chat');
    </script>
</body>
</html>'''
            self.wfile.write(html.encode())
        else:
            super().do_GET()

# Start debug server
PORT = 3456
with socketserver.TCPServer(("", PORT), DebugHandler) as httpd:
    print(f"Debug server running at http://localhost:{PORT}")
    print("Open this in your browser to test the API connection")
    httpd.serve_forever()
