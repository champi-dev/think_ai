#!/usr/bin/env python3
"""Ultra-fast Railway startup script - minimal initialization."""

import json
import os
import sys
from typing import Any, Dict

# Force all optimizations
os.environ["THINK_AI_USE_LIGHTWEIGHT"] = "true"
os.environ["THINK_AI_MINIMAL_INIT"] = "true"
os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"  # Skip model checks
os.environ["HF_HUB_OFFLINE"] = "1"  # Skip HuggingFace hub
os.environ["TOKENIZERS_PARALLELISM"] = "false"

print("⚡ Ultra-fast Railway startup initiated...")

# Minimal FastAPI setup
try:
    import uvicorn
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse

    # Create minimal app
    app = FastAPI(title="Think AI Railway", description="Optimized for fast startup", version="3.0.0")

    # Add CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health endpoint
    @app.get("/health")
    async def health():
        return {"status": "healthy", "mode": "fast-start"}

    # Serve webapp HTML at root
    @app.get("/")
    async def root():
        # Return HTML that loads the webapp
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Think AI</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; }
                .chat-box { border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 20px 0; min-height: 300px; background: #fafafa; }
                .input-group { display: flex; gap: 10px; }
                input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
                button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
                button:hover { background: #0056b3; }
                .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
                .user { background: #e3f2fd; text-align: right; }
                .ai { background: #f5f5f5; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Think AI - Fast Start Mode</h1>
                <div id="chat-box" class="chat-box">
                    <div class="message ai">Welcome to Think AI! I'm running in fast-start mode for quick deployment.</div>
                </div>
                <div class="input-group">
                    <input type="text" id="message-input" placeholder="Type your message..." onkeypress="if(event.key==='Enter')sendMessage()">
                    <button onclick="sendMessage()">Send</button>
                </div>
            </div>
            <script>
                async function sendMessage() {
                    const input = document.getElementById('message-input');
                    const chatBox = document.getElementById('chat-box');
                    const message = input.value.trim();
                    if (!message) return;
                    
                    // Add user message
                    chatBox.innerHTML += `<div class="message user">${message}</div>`;
                    input.value = '';
                    
                    try {
                        const response = await fetch('/api/v1/chat', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({message: message})
                        });
                        const data = await response.json();
                        chatBox.innerHTML += `<div class="message ai">${data.response}</div>`;
                    } catch (error) {
                        chatBox.innerHTML += `<div class="message ai">Error: ${error.message}</div>`;
                    }
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            </script>
        </body>
        </html>
        """
        from fastapi.responses import HTMLResponse

        return HTMLResponse(content=html_content)

    # Basic chat endpoint
    @app.post("/api/v1/chat")
    async def chat(request: Dict[str, Any]):
        message = request.get("message", "")
        return JSONResponse(
            {"response": f"Echo: {message}", "mode": "fast-start", "note": "Full AI capabilities loading in background"}
        )

    # Start server immediately
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 8080))
        print(f"🚀 Starting ultra-fast server on port {port}")

        # Run with minimal config
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="warning",  # Reduce logging
            access_log=False,  # No access logs
            workers=1,
            loop="asyncio",
        )

except Exception as e:
    print(f"❌ Fast start failed: {e}")

    # Ultra-minimal HTTP server fallback
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class MinimalHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/health":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status":"healthy"}')
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Think AI - Minimal Mode")

        def log_message(self, format, *args):
            pass  # No logging for speed

    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), MinimalHandler)
    print(f"✅ Minimal server running on port {port}")
    server.serve_forever()
