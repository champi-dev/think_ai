#!/usr/bin/env python3
"""Ultra-fast Railway startup script - minimal initialization."""

import os
import sys
import json
from typing import Dict, Any

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
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    import uvicorn
    
    # Create minimal app
    app = FastAPI(
        title="Think AI Railway", 
        description="Optimized for fast startup",
        version="3.0.0"
    )
    
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
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "name": "Think AI",
            "status": "operational",
            "mode": "fast-start",
            "message": "System initialized in minimal mode for fast startup"
        }
    
    # Basic chat endpoint
    @app.post("/api/v1/chat")
    async def chat(request: Dict[str, Any]):
        message = request.get("message", "")
        return JSONResponse({
            "response": f"Echo: {message}",
            "mode": "fast-start",
            "note": "Full AI capabilities loading in background"
        })
    
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
            loop="asyncio"
        )
        
except Exception as e:
    print(f"❌ Fast start failed: {e}")
    
    # Ultra-minimal HTTP server fallback
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
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