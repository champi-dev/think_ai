#!/usr/bin/env python3
"""
Lightweight startup script for Think AI on Railway.
Uses minimal dependencies and built-in lightweight alternatives.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add think_ai to path
sys.path.insert(0, str(Path(__file__).parent))

# Set lightweight mode environment variables
os.environ["THINK_AI_MODE"] = "lightweight"
os.environ["THINK_AI_NO_ML"] = "true"
os.environ["THINK_AI_USE_FALLBACKS"] = "true"


async def main():
    """Start Think AI in lightweight mode."""
    try:
        # Import only minimal dependencies, avoid ML modules
        import hashlib

        import numpy as np
        import uvicorn
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware

        # Use inline lightweight config to avoid importing think_ai modules
        class LightweightConfig:
            max_memory_mb = 256
            host = "0.0.0.0"
            port = int(os.environ.get("PORT", 8080))
            workers = 1
            embedding_dimension = 384
            features = {"use_transformers": False, "use_torch": False, "use_ml_models": False, "mode": "lightweight"}

            @classmethod
            def for_railway(cls):
                return cls()

        # Create lightweight config
        config = LightweightConfig.for_railway()

        # Create FastAPI app
        app = FastAPI(title="Think AI Lightweight", description="Memory-efficient Think AI deployment", version="1.0.0")

        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Health check endpoint
        @app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "mode": "lightweight",
                "memory_limit_mb": config.max_memory_mb,
                "features": config.features,
            }

        # Root endpoint
        @app.get("/")
        async def root():
            return {"message": "Think AI Lightweight is running", "docs": "/docs", "health": "/health"}

        # Chat endpoint using lightweight components
        from pydantic import BaseModel

        class ChatRequest(BaseModel):
            message: str

        @app.post("/chat")
        async def chat(request: ChatRequest):
            """Simple chat endpoint using pattern matching."""
            # Use simple pattern-based responses
            responses = {
                "hello": "Hello! I'm Think AI running in lightweight mode.",
                "help": "I'm a lightweight version optimized for minimal memory usage.",
                "status": f"Running with {config.max_memory_mb}MB memory limit.",
            }

            # Simple keyword matching
            message_lower = request.message.lower()
            for keyword, response in responses.items():
                if keyword in message_lower:
                    return {"response": response}

            return {
                "response": "I'm running in lightweight mode. My responses are limited but I'm using minimal resources!"
            }

        # API endpoints for vector operations
        @app.post("/embed")
        async def embed_text(text: str):
            """Generate embeddings using hash-based approach."""

            # Hash-based embedding
            hash_obj = hashlib.sha256(text.encode())
            hash_bytes = hash_obj.digest()

            # Convert to normalized embedding
            embedding = np.array([(byte / 255.0 - 0.5) * 2 for byte in hash_bytes[: config.embedding_dimension // 8]])

            # Pad or truncate to exact dimension
            if len(embedding) < config.embedding_dimension:
                embedding = np.pad(embedding, (0, config.embedding_dimension - len(embedding)))
            else:
                embedding = embedding[: config.embedding_dimension]

            return {"embedding": embedding.tolist(), "dimension": config.embedding_dimension, "method": "hash-based"}

        @app.post("/search")
        async def search_similar(query: str, top_k: int = 5):
            """Simple similarity search using in-memory store."""
            return {"results": [], "message": "Search is running in lightweight mode", "top_k": top_k}

        # Start the server
        print(f"Starting Think AI Lightweight on port {config.port}")
        print(f"Memory limit: {config.max_memory_mb}MB")
        print("Mode: Lightweight (no ML dependencies)")

        # Run with minimal uvicorn config
        uvicorn_config = uvicorn.Config(
            app,
            host=config.host,
            port=config.port,
            log_level="info",
            access_log=False,  # Disable access logs to save memory
            workers=config.workers,
            loop="asyncio",
            limit_max_requests=1000,  # Restart workers periodically to prevent memory leaks
        )

        server = uvicorn.Server(uvicorn_config)
        await server.serve()

    except Exception as e:
        print(f"Error starting lightweight server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
