import http.server
import socketserver
import json
import urllib.request

PORT = 5555


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            # Serve a fixed version of the webapp
            html = """<\!DOCTYPE html>
<html>
<head>
    <title>Think AI - Fixed</title>
    <style>
        body { background: #0a0a0a; color: #fff; font-family: monospace; padding: 20px; }
        #messages { height: 400px; overflow-y: auto; border: 1px solid #333; padding: 10px; margin: 20px 0; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #1a3a52; color: #3b82f6; }
        .ai { background: #0a3a2a; color: #10b981; }
        .error { background: #3a0a0a; color: #ef4444; }
        input { width: 70%; padding: 10px; background: #1a1a1a; border: 1px solid #333; color: #fff; }
        button { padding: 10px 20px; background: #3b82f6; border: none; color: #fff; cursor: pointer; margin-left: 10px; }
    </style>
</head>
<body>
    <h1>🚀 Think AI - Working Interface</h1>
    <div id="messages"></div>
    <div>
        <input type="text" id="input" placeholder="Ask me anything..." autofocus>
        <button onclick="sendMessage()">Send</button>
    </div>
    
    <script>
        const messages = document.getElementById("messages");
        const input = document.getElementById("input");
        
        function addMessage(text, className) {
            const div = document.createElement("div");
            div.className = "message " + className;
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
        
        async function sendMessage() {
            const text = input.value.trim();
            if (\!text) return;
            
            addMessage("You: " + text, "user");
            input.value = "";
            
            addMessage("AI: Thinking...", "ai thinking");
            
            try {
                const response = await fetch("http://69.197.178.37:7777/api/chat", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({message: text})
                });
                
                const data = await response.json();
                
                // Remove thinking message
                const thinking = document.querySelector(".thinking");
                if (thinking) thinking.remove();
                
                // Add actual response
                addMessage("AI: " + (data.response || "No response"), "ai");
                
            } catch (error) {
                const thinking = document.querySelector(".thinking");
                if (thinking) thinking.remove();
                addMessage("Error: " + error.message, "error");
            }
        }
        
        input.addEventListener("keypress", (e) => {
            if (e.key === "Enter") sendMessage();
        });
        
        // Test message
        addMessage("System: Connected\! Type a message and press Enter.", "ai");
    </script>
</body>
</html>"""

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

    def log_message(self, format, *args):
        pass


print(f"🌐 Starting local test server on http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    httpd.serve_forever()
