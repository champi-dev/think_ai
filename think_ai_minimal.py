#!/usr/bin/env python3
"""Minimal Think AI API server for Railway deployment."""

import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# FastAPI imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Import our lightweight components
try:
    from think_ai.config.lightweight_config import LightweightConfig
    from think_ai.models.embeddings.embeddings_fixed import FixedEmbeddingModel
    from think_ai.storage.vector.vector_db_fallback import FallbackVectorDB

    logger.info("Successfully imported Think AI lightweight components")
except ImportError as e:
    logger.error(f"Failed to import Think AI components: {e}")

    # Fallback implementations
    class LightweightConfig:
        def __init__(self):
            self.host = "0.0.0.0"
            self.port = int(os.environ.get("PORT", 8080))
            self.storage_path = "/tmp/think_ai"
            self.enable_cache = True
            self.cache_ttl = 3600

    class FixedEmbeddingModel:
        def embed(self, text: str) -> List[float]:
            # Simple hash-based embedding
            import hashlib

            hash_obj = hashlib.md5(text.encode())
            hash_bytes = hash_obj.digest()
            return [float(b) / 255.0 for b in hash_bytes[:8]]

    class FallbackVectorDB:
        def __init__(self, storage_path: str):
            self.storage = {}

        def add(self, text: str, embedding: List[float], metadata: Dict = None):
            doc_id = str(len(self.storage))
            self.storage[doc_id] = {"text": text, "embedding": embedding, "metadata": metadata or {}}
            return doc_id

        def search(self, query_embedding: List[float], k: int = 5) -> List[Dict]:
            # Simple cosine similarity
            results = []
            for doc_id, doc in self.storage.items():
                score = sum(a * b for a, b in zip(query_embedding, doc["embedding"]))
                results.append({"id": doc_id, "score": score, "text": doc["text"], "metadata": doc["metadata"]})
            results.sort(key=lambda x: x["score"], reverse=True)
            return results[:k]


# Initialize components
config = LightweightConfig()
embedder = FixedEmbeddingModel()
vector_db = FallbackVectorDB(getattr(config, "storage_path", "/tmp/think_ai"))

# Create FastAPI app
app = FastAPI(
    title="Think AI Minimal API", description="Lightweight Think AI API for Railway deployment", version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class ChatMessage(BaseModel):
    role: str = "user"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "think-ai-mini"
    temperature: float = 0.7
    max_tokens: int = 150


class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]


class EmbeddingRequest(BaseModel):
    input: str
    model: str = "think-ai-embeddings"


class SearchRequest(BaseModel):
    query: str
    k: int = 5


# Simple response generation
def generate_response(messages: List[ChatMessage], temperature: float = 0.7) -> str:
    """Generate a simple response based on the last message."""
    if not messages:
        return "Hello! How can I help you today?"

    last_message = messages[-1].content.lower()

    # Simple pattern matching for responses
    if "hello" in last_message or "hi" in last_message:
        return "Hello! I'm Think AI, running on Railway. How can I assist you?"
    elif "how are you" in last_message:
        return "I'm running smoothly on Railway! Thanks for asking."
    elif "think ai" in last_message:
        return "Think AI is an intelligent system designed to help with various tasks. I'm a minimal version optimized for Railway deployment."
    elif "help" in last_message:
        return "I can help you with: 1) General questions, 2) Text embeddings, 3) Semantic search. What would you like to know?"
    else:
        # Echo-based response with some intelligence
        words = last_message.split()
        if len(words) > 3:
            return f"I understand you're asking about {' '.join(words[:3])}... Let me think about that. Based on my lightweight processing, I'd say this relates to the concept of {words[-1]}."
        return f"Interesting question! As a minimal Think AI deployment, I'm processing: '{last_message}'. Could you provide more context?"


# API endpoints
@app.get("/")
async def root():
    return {
        "name": "Think AI Minimal API",
        "version": "1.0.0",
        "status": "running",
        "deployment": "railway",
        "endpoints": ["/health", "/v1/chat/completions", "/v1/embeddings", "/v1/search"],
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "think-ai-minimal",
        "timestamp": datetime.now().isoformat(),
        "components": {"embedder": "operational", "vector_db": "operational", "api": "operational"},
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """Handle chat completion requests."""
    try:
        # Generate response
        response_text = generate_response(request.messages, request.temperature)

        # Create response
        response = ChatResponse(
            id=f"chatcmpl-{datetime.now().timestamp():.0f}",
            created=int(datetime.now().timestamp()),
            model=request.model,
            choices=[{"index": 0, "message": {"role": "assistant", "content": response_text}, "finish_reason": "stop"}],
            usage={
                "prompt_tokens": sum(len(msg.content.split()) for msg in request.messages),
                "completion_tokens": len(response_text.split()),
                "total_tokens": sum(len(msg.content.split()) for msg in request.messages) + len(response_text.split()),
            },
        )

        return response
    except Exception as e:
        logger.error(f"Chat completion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/embeddings")
async def create_embeddings(request: EmbeddingRequest):
    """Create embeddings for the input text."""
    try:
        embedding = embedder.embed(request.input)

        return {
            "object": "list",
            "data": [{"object": "embedding", "embedding": embedding, "index": 0}],
            "model": request.model,
            "usage": {"prompt_tokens": len(request.input.split()), "total_tokens": len(request.input.split())},
        }
    except Exception as e:
        logger.error(f"Embedding error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/search")
async def search(request: SearchRequest):
    """Search for similar documents."""
    try:
        # Generate query embedding
        query_embedding = embedder.embed(request.query)

        # Search
        results = vector_db.search(query_embedding, request.k)

        return {"query": request.query, "results": results, "total": len(results)}
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/index")
async def index_document(text: str, metadata: Optional[Dict] = None):
    """Index a document for search."""
    try:
        # Generate embedding
        embedding = embedder.embed(text)

        # Add to vector DB
        doc_id = vector_db.add(text, embedding, metadata)

        return {"id": doc_id, "status": "indexed", "text_length": len(text)}
    except Exception as e:
        logger.error(f"Indexing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Think AI Minimal API on port {port}")

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
