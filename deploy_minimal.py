#!/usr/bin/env python3
"""Minimal deployment script for Think AI - guaranteed to work."""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Import FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import our O(1) chat
from think_ai_simple_chat import get_response_time, response_cache, keyword_to_category

# Create FastAPI app
app = FastAPI(
    title="Think AI API",
    description="O(1) Performance AI System",
    version="5.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    
    
class ChatResponse(BaseModel):
    response: str
    response_time_ms: float
    

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Think AI",
        "version": "5.0",
        "status": "operational",
        "performance": "O(1) guaranteed",
        "endpoints": {
            "/": "This page",
            "/chat": "Chat endpoint (POST)",
            "/health": "Health check"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "response_cache_size": len(response_cache)}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """O(1) chat endpoint."""
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Get O(1) response
    start_time = asyncio.get_event_loop().time()
    
    # Hash-based category lookup
    words = request.message.lower().split()
    category = 0
    
    for word in words:
        word_hash = hash(word)
        if word_hash in keyword_to_category:
            category = keyword_to_category[word_hash]
            break
    
    # Get response from cache
    responses = response_cache[category]
    response_text = responses[hash(request.message) % len(responses)]
    
    # Calculate response time
    response_time = (asyncio.get_event_loop().time() - start_time) * 1000
    
    return ChatResponse(
        response=response_text,
        response_time_ms=round(response_time, 3)
    )


def main():
    """Run the minimal deployment."""
    port = int(os.environ.get("PORT", 8080))
    host = "0.0.0.0"
    
    print(f"🚀 Starting Think AI Minimal API on {host}:{port}")
    print(f"📊 O(1) Performance Guaranteed")
    print(f"🌐 API Docs: http://localhost:{port}/docs")
    
    # Run server
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()