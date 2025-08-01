#!/usr/bin/env python3
"""
Improved AI Server with better response matching
"""
import http.server
import socketserver
import json
import os
from pathlib import Path
from difflib import SequenceMatcher
import re

PORT = 7777
HOST = "0.0.0.0"

class ImprovedKnowledgeMatcher:
    def __init__(self):
        self.knowledge = self.load_knowledge()
        self.response_cache = self.load_response_cache()
        
    def load_knowledge(self):
        """Load knowledge from evaluated_knowledge.json"""
        knowledge_file = Path("./cache/evaluated_knowledge.json")
        if knowledge_file.exists():
            with open(knowledge_file, 'r') as f:
                data = json.load(f)
                return data.get("knowledge_base", {})
        return {}
    
    def load_response_cache(self):
        """Load response cache"""
        cache_file = Path("./cache/response_cache.json")
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def normalize_query(self, query):
        """Normalize query for better matching"""
        # Remove punctuation and lowercase
        query = query.lower().strip()
        query = re.sub(r'[?!.,;:]', '', query)
        return query
    
    def extract_keywords(self, query):
        """Extract meaningful keywords from query"""
        # Remove common words
        stop_words = {'what', 'is', 'are', 'the', 'a', 'an', 'tell', 'me', 'about', 
                     'explain', 'how', 'does', 'can', 'you', 'please', 'help', 'with'}
        words = query.lower().split()
        keywords = [w for w in words if w not in stop_words]
        return keywords
    
    def find_best_match(self, query):
        """Find the best matching response for a query"""
        normalized_query = self.normalize_query(query)
        
        # First check response cache for exact or close matches
        if normalized_query in self.response_cache:
            response_data = self.response_cache[normalized_query]
            if isinstance(response_data, dict) and 'response' in response_data:
                return response_data['response']
            elif isinstance(response_data, str):
                return response_data
        
        # Check for partial matches in cache
        for cached_query, response_data in self.response_cache.items():
            cached_normalized = self.normalize_query(cached_query)
            if cached_normalized in normalized_query or normalized_query in cached_normalized:
                if isinstance(response_data, dict) and 'response' in response_data:
                    return response_data['response']
                elif isinstance(response_data, str):
                    return response_data
        
        # Extract keywords and search knowledge base
        keywords = self.extract_keywords(query)
        
        best_score = 0
        best_topic = None
        best_response = None
        
        for topic, data in self.knowledge.items():
            score = 0
            
            # Check if any keyword matches the topic
            topic_lower = topic.lower()
            for keyword in keywords:
                if keyword in topic_lower:
                    score += 3
                
            # Check related concepts
            related = data.get("related_concepts", [])
            for concept in related:
                for keyword in keywords:
                    if keyword in concept.lower():
                        score += 2
            
            # Fuzzy matching for the whole query
            similarity = SequenceMatcher(None, normalized_query, topic_lower).ratio()
            if similarity > 0.6:  # Higher threshold to avoid false matches
                score += similarity * 5
            
            # Check if topic words appear in query
            topic_words = topic_lower.split()
            for word in topic_words:
                if word in normalized_query and len(word) > 3:  # Skip short words
                    score += 2
            
            if score > best_score and score > 2:  # Minimum threshold
                best_score = score
                best_topic = topic
                best_response = data.get("content", "")
        
        if best_response:
            return best_response
        
        # Default response when no good match is found
        return "I understand you're asking about '" + query + "'. While I don't have specific information about that exact topic, I can help with a wide range of subjects including science, technology, philosophy, psychology, and more. Could you please rephrase your question or ask about a related topic?"

class ImprovedAIHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.matcher = ImprovedKnowledgeMatcher()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            # Simple test interface
            html = """
<!DOCTYPE html>
<html>
<head>
    <title>Think AI - Improved Version</title>
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
        h1 { color: #333; }
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
            min-height: 50px;
        }
        .status { color: #4CAF50; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Think AI - <span class="status">Improved Version</span></h1>
        <p>Now with better contextual understanding and relevant responses!</p>
        
        <input type="text" id="query" placeholder="Ask me anything..." onkeypress="if(event.key==='Enter') sendQuery()">
        <button onclick="sendQuery()">Ask</button>
        
        <div id="response"></div>
    </div>
    
    <script>
        async function sendQuery() {
            const query = document.getElementById('query').value;
            if (!query.trim()) return;
            
            document.getElementById('response').innerHTML = '<em>Thinking...</em>';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: query})
                });
                const data = await response.json();
                
                document.getElementById('response').innerHTML = data.response;
            } catch (e) {
                document.getElementById('response').innerHTML = 'Error: Could not get response';
            }
        }
        
        // Focus on input
        document.getElementById('query').focus();
    </script>
</body>
</html>
"""
            self.wfile.write(html.encode())
            
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"OK - Improved AI Server Running")
            
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path in ["/api/chat", "/chat"]:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                query = data.get('message', data.get('query', ''))
                
                # Get best matching response
                response_text = self.matcher.find_best_match(query)
                
                response_data = {
                    "response": response_text,
                    "query": query,
                    "status": "success"
                }
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
                
            except Exception as e:
                print(f"Error processing request: {e}")
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "response": "I encountered an error processing your request. Please try again.",
                    "error": str(e)
                }).encode())
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def log_message(self, format, *args):
        # Only log errors
        if args[1] != '200':
            print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == "__main__":
    # Change to project directory
    os.chdir("/home/administrator/think_ai")
    
    print(f"🚀 Improved Think AI Server starting on http://{HOST}:{PORT}")
    print("✅ Enhanced response matching algorithm")
    print("✅ Better handling of unknown queries")
    print("✅ Love and emotion knowledge added")
    
    handler = lambda *args, **kwargs: ImprovedAIHandler(*args, **kwargs)
    
    with socketserver.TCPServer((HOST, PORT), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")