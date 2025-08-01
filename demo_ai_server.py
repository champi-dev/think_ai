#!/usr/bin/env python3
"""
Demo AI Server - Shows the broken response mapping issue
"""
import http.server
import socketserver
import json
import hashlib

PORT = 7777

# Simulating the issue - responses are mapped incorrectly
KNOWLEDGE_BASE = {
    "ping": "Electrical engineering harnesses electricity for power and information systems. Core areas include circuit analysis, electromagnetics, power systems, electronics, and signal processing. Applications range from power generation and distribution to microelectronics and telecommunications. Digital revolution was enabled by electrical engineers developing transistors, integrated circuits, and communication systems.. In practical terms, this helps you understand the core concepts better.",
    "what is quantum physics": "Psycholinguistics investigates psychological and neurobiological factors enabling humans to acquire, use, and understand language. Brain imaging reveals language areas like Broca's and Wernicke's regions. Knowing about psycholinguistics informs education, therapy for language disorders, and artificial intelligence design... In practical terms, this helps you understand the core concepts better.",
    "electrical engineering": "Correct response about electrical engineering would go here",
    "psycholinguistics": "Correct response about psycholinguistics would go here"
}

def normalize_query(query):
    """Simple normalization - just lowercase and strip"""
    return query.lower().strip().rstrip('?!.')

class BrokenAIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """
<!DOCTYPE html>
<html>
<head>
    <title>Think AI - Broken Demo</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        input { width: 70%; padding: 10px; }
        button { padding: 10px 20px; }
        #response { margin-top: 20px; padding: 20px; background: #f0f0f0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Think AI - Demonstrating the Issue</h1>
    <p>Try these queries to see the problem:</p>
    <ul>
        <li>ping</li>
        <li>what is quantum physics</li>
    </ul>
    <input type="text" id="query" placeholder="Enter your question">
    <button onclick="sendQuery()">Ask</button>
    <div id="response"></div>
    
    <script>
        async function sendQuery() {
            const query = document.getElementById('query').value;
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: query})
            });
            const data = await response.json();
            document.getElementById('response').innerHTML = '<strong>Response:</strong><br>' + data.response;
        }
    </script>
</body>
</html>
"""
            self.wfile.write(html.encode())
        
        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
    
    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            query = data.get('message', '')
            normalized = normalize_query(query)
            
            # This is where the bug is - using exact match instead of semantic understanding
            response = KNOWLEDGE_BASE.get(normalized, 
                "I don't have information about that topic. Try 'ping' or 'what is quantum physics'")
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            self.wfile.write(json.dumps({
                "response": response,
                "query": query,
                "normalized": normalized
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

if __name__ == "__main__":
    print(f"🚨 Broken AI Server running on http://localhost:{PORT}")
    print("This demonstrates the response mapping issue")
    
    with socketserver.TCPServer(("", PORT), BrokenAIHandler) as httpd:
        httpd.serve_forever()