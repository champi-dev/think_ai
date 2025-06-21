#!/usr/bin/env python3
"""Minimal Think AI API server for Railway deployment - no heavy dependencies."""

import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Think AI API", description="Think AI Minimal API - Optimized for Railway", version="1.0.0")

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
    model: str = "minimal"


class EmbeddingRequest(BaseModel):
    text: str
    model: Optional[str] = "minimal"


class EmbeddingResponse(BaseModel):
    embedding: List[float]
    dimension: int
    model: str = "minimal"


# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "Think AI Minimal API",
        "version": "1.0.0",
        "status": "operational",
        "deployment": "railway",
        "message": "Minimal API running without heavy ML dependencies",
        "endpoints": ["/health", "/api/v1/chat", "/api/v1/embeddings", "/api/v1/completions"],
    }


# Health endpoint
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "think-ai-minimal",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "running",
    }


# Chat endpoint
@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    """Simple chat endpoint that returns a mock response."""
    return ChatResponse(
        response=f"This is a minimal response to: {request.message}",
        conversation_id=request.conversation_id or "minimal-001",
        timestamp=datetime.utcnow().isoformat(),
    )


# Embeddings endpoint
@app.post("/api/v1/embeddings")
async def embeddings(request: EmbeddingRequest):
    """Simple embeddings endpoint that returns mock embeddings."""
    # Generate a simple hash-based embedding
    text_hash = hash(request.text)
    embedding = [float((text_hash >> i) & 1) for i in range(384)]

    return EmbeddingResponse(embedding=embedding, dimension=384)


# Completions endpoint
@app.post("/api/v1/completions")
async def completions(request: ChatRequest):
    """Simple completions endpoint."""
    return {
        "completion": f"Completion for: {request.message}",
        "model": "minimal",
        "timestamp": datetime.utcnow().isoformat(),
    }


# Error handler
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return {"error": str(exc), "status": "error", "message": "An error occurred processing your request"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Think AI Minimal API on port {port}")

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
