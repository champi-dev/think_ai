#!/usr/bin/env python3
"""Simple Think AI API server - Clean implementation for Railway."""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Think AI",
    description="Think AI - Powered by Qwen models",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: str
    model: str = "qwen"

class GenerateRequest(BaseModel):
    prompt: str
    max_length: int = 200
    temperature: float = 0.7

class GenerateResponse(BaseModel):
    text: str
    model: str = "qwen"
    tokens: int

# Simple in-memory state
conversations = {}
model_info = {
    "name": "Qwen/Qwen2.5-Coder-1.5B",
    "type": "language_model",
    "capabilities": ["chat", "code", "reasoning"]
}

@app.get("/")
async def root():
    """Root endpoint with system info."""
    return {
        "name": "Think AI",
        "status": "operational",
        "model": model_info["name"],
        "version": "2.0.0",
        "endpoints": [
            "/health",
            "/api/v1/chat",
            "/api/v1/generate",
            "/api/v1/model/info"
        ]
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "model": model_info["name"],
        "conversations_active": len(conversations)
    }

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    """Chat endpoint - simple response for now."""
    conversation_id = request.conversation_id or f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Store conversation
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    
    conversations[conversation_id].append({
        "role": "user",
        "content": request.message,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    # Simple response
    response_text = f"I understand you said: '{request.message}'. I'm Think AI powered by Qwen models!"
    
    conversations[conversation_id].append({
        "role": "assistant",
        "content": response_text,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return ChatResponse(
        response=response_text,
        conversation_id=conversation_id,
        timestamp=datetime.utcnow().isoformat()
    )

@app.post("/api/v1/generate")
async def generate(request: GenerateRequest):
    """Text generation endpoint."""
    # Simple generation for now
    generated_text = f"{request.prompt}\n\n[Generated content would go here - using {model_info['name']}]"
    
    return GenerateResponse(
        text=generated_text,
        tokens=len(generated_text.split())
    )

@app.get("/api/v1/model/info")
async def model_info_endpoint():
    """Get model information."""
    return {
        "model": model_info,
        "capabilities": {
            "chat": True,
            "code_generation": True,
            "embeddings": True,
            "multi_language": True
        },
        "limits": {
            "max_tokens": 2048,
            "max_conversations": 1000
        }
    }

@app.get("/api/v1/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history."""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id]
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Think AI on port {port}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)