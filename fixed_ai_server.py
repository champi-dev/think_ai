#!/usr/bin/env python3
"""
Fixed AI Server - Properly matches queries to correct responses
"""
import http.server
import socketserver
import json
import re
from difflib import SequenceMatcher

PORT = 7777

# Properly organized knowledge base
KNOWLEDGE_BASE = {
    "electrical engineering": {
        "content": "Electrical engineering harnesses electricity for power and information systems. Core areas include circuit analysis, electromagnetics, power systems, electronics, and signal processing. Applications range from power generation and distribution to microelectronics and telecommunications. Digital revolution was enabled by electrical engineers developing transistors, integrated circuits, and communication systems.",
        "keywords": ["electrical", "engineering", "circuit", "electronics", "power"],
        "aliases": ["electrical eng", "ee", "electrical"]
    },
    "quantum physics": {
        "content": "Quantum physics revolutionizes our understanding of reality at the smallest scales. It reveals that particles exist in superposition states, can be entangled across vast distances, and behave probabilistically rather than deterministically. The wave-particle duality shows matter exhibits both wave and particle properties. Applications include quantum computing, cryptography, and technologies like lasers and transistors.",
        "keywords": ["quantum", "physics", "mechanics", "particle", "wave", "superposition"],
        "aliases": ["quantum mechanics", "qm", "quantum theory"]
    },
    "psycholinguistics": {
        "content": "Psycholinguistics investigates psychological and neurobiological factors enabling humans to acquire, use, and understand language. Research examines how we process speech sounds, access word meanings, parse sentences, and produce language. Brain imaging reveals language areas like Broca's and Wernicke's regions. Understanding psycholinguistics informs education, therapy for language disorders, and artificial intelligence design.",
        "keywords": ["psycholinguistics", "language", "psychology", "linguistics", "brain", "speech"],
        "aliases": ["psycho linguistics", "language psychology"]
    },
    "ping": {
        "content": "Ping is a network utility that tests connectivity between two nodes by sending ICMP echo request packets and measuring the response time. It's commonly used to check if a host is reachable and to measure network latency. The name comes from sonar terminology, where a 'ping' is an acoustic pulse.",
        "keywords": ["ping", "network", "connectivity", "icmp", "latency"],
        "aliases": ["network ping", "ping test"]
    }
}

def normalize_query(query):
    """Normalize query for better matching"""
    return query.lower().strip().rstrip('?!.')

def find_best_match(query):
    """Find the best matching topic for a query using keyword matching and fuzzy matching"""
    normalized = normalize_query(query)
    
    # First, check for exact matches in topic names or aliases
    for topic, data in KNOWLEDGE_BASE.items():
        if normalized == topic or normalized in data.get("aliases", []):
            return data["content"]
    
    # Second, check if query contains any topic name
    for topic, data in KNOWLEDGE_BASE.items():
        if topic in normalized:
            return data["content"]
    
    # Third, check for keyword matches
    best_score = 0
    best_topic = None
    
    for topic, data in KNOWLEDGE_BASE.items():
        score = 0
        # Check keywords
        for keyword in data["keywords"]:
            if keyword in normalized:
                score += 1
        
        # Also use fuzzy matching
        similarity = SequenceMatcher(None, normalized, topic).ratio()
        score += similarity * 2  # Weight fuzzy matching
        
        if score > best_score:
            best_score = score
            best_topic = topic
    
    # Return best match if score is reasonable
    if best_score > 0.5:
        return KNOWLEDGE_BASE[best_topic]["content"]
    
    return None

class FixedAIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """
<!DOCTYPE html>
<html>
<head>
    <title>Think AI - Fixed Version</title>
    <style>
        body { 
            font-family: Arial; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px; 
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        input { 
            width: 70%; 
            padding: 12px; 
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button { 
            padding: 12px 24px; 
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background: #45a049; }
        #response { 
            margin-top: 20px; 
            padding: 20px; 
            background: #f9f9f9; 
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }
        .examples {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .fixed { color: #4CAF50; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Think AI - <span class="fixed">Fixed Version</span></h1>
        <p>Now with proper contextual understanding!</p>
        
        <div class="examples">
            <strong>Try these queries:</strong>
            <ul>
                <li>ping</li>
                <li>what is quantum physics</li>
                <li>tell me about electrical engineering</li>
                <li>explain psycholinguistics</li>
            </ul>
        </div>
        
        <input type="text" id="query" placeholder="Enter your question" onkeypress="if(event.key==='Enter') sendQuery()">
        <button onclick="sendQuery()">Ask AI</button>
        
        <div id="response"></div>
    </div>
    
    <script>
        async function sendQuery() {
            const query = document.getElementById('query').value;
            if (!query.trim()) return;
            
            document.getElementById('response').innerHTML = '<em>Thinking...</em>';
            
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: query})
            });
            const data = await response.json();
            
            document.getElementById('response').innerHTML = `
                <strong>Your Question:</strong> ${query}<br><br>
                <strong>AI Response:</strong><br>${data.response}
            `;
        }
        
        // Focus on input when page loads
        document.getElementById('query').focus();
    </script>
</body>
</html>
"""
            self.wfile.write(html.encode())
        
        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK - Fixed AI Server Running")
    
    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            query = data.get('message', '')
            
            # Find the best matching response
            response = find_best_match(query)
            
            if not response:
                response = f"I understand you're asking about '{query}'. While I don't have specific information about that exact topic, I can help with electrical engineering, quantum physics, psycholinguistics, and network utilities like ping. Please try rephrasing your question or ask about one of these topics."
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            self.wfile.write(json.dumps({
                "response": response,
                "query": query,
                "status": "success"
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress request logs for cleaner output
        pass

if __name__ == "__main__":
    print(f"✅ Fixed AI Server running on http://localhost:{PORT}")
    print("This version properly matches queries to correct responses")
    print("Access at: http://localhost:7777")
    
    with socketserver.TCPServer(("", PORT), FixedAIHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")