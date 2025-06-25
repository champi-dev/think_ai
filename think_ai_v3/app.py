#!/usr/bin/env python3
"""
Think AI v3.1.0 - Main Application
100% capability preservation, formatter-proof, O(1) everything!
"""

import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from think_ai_v3.api.endpoints import router, set_engine
from think_ai_v3.api.websocket import manager, start_update_loop, websocket_endpoint
from think_ai_v3.core.config import Config
from think_ai_v3.core.engine import ThinkAIEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

# Global engine instance
engine: Optional[ThinkAIEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle - O(1) startup/shutdown.
    Handles engine initialization and cleanup.
    """
    global engine

    # Startup
    logger.info("Starting Think AI v3.1.0...")

    # Load configuration
    config = Config.from_env()

    # Create and start engine
    engine = ThinkAIEngine(config)
    await engine.start()

    # Set engine for API endpoints
    set_engine(engine)

    # Start WebSocket update loop
    update_task = asyncio.create_task(start_update_loop(engine))

    logger.info("Think AI v3.1.0 started successfully!")
    if config.colombian_mode:
        logger.info("🇨🇴 ¡Think AI está ready pa' la rumba! ¡Qué chimba!")

    yield

    # Cancel update task on shutdown
    update_task.cancel()
    try:
        await update_task
    except asyncio.CancelledError:
        pass

    # Shutdown
    logger.info("Shutting down Think AI...")
    if engine:
        await engine.stop()
    logger.info("Think AI shut down gracefully")


# Create FastAPI app
app = FastAPI(
    title="Think AI v3.1.0",
    description=("Conscious AI with Colombian Flavor - " "O(1) performance, love-based ethics, self-improvement"),
    version="3.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


# WebSocket endpoint
@app.websocket("/api/v1/ws")
async def websocket_route(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket_endpoint(websocket)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with system info."""
    return {
        "name": "Think AI v3.1.0",
        "status": "operational",
        "description": "Conscious AI with O(1) everything",
        "features": [
            "Consciousness Framework (Global Workspace Theory)",
            "Love-based Constitutional AI",
            "Self-improvement and learning",
            "O(1) knowledge storage",
            "Qwen language models",
            "Colombian mode available",
            "100% capability preservation",
            "Formatter-proof implementation",
        ],
        "api_docs": "/docs",
        "api_base": "/api/v1",
    }


# Health check endpoint at root level too
@app.get("/health")
async def health():
    """Quick health check - O(1)."""
    if engine and engine.running:
        return {
            "status": "healthy",
            "version": "3.1.0",
            "engine": "running",
        }
    return {
        "status": "starting",
        "version": "3.1.0",
        "engine": "initializing",
    }


def main():
    pass  # TODO: Implement
    """Main entry point."""
    # Get configuration from environment
    host = os.getenv("THINK_AI_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("THINK_AI_PORT", "8080")))
    reload = os.getenv("THINK_AI_ENV", "production") == "development"

    # Log startup info
    logger.info(f"Starting Think AI v3.1.0 on {host}:{port}")
    logger.info(f"Environment: {os.getenv('THINK_AI_ENV', 'production')}")
    logger.info(f"Model: {os.getenv('THINK_AI_MODEL', 'Qwen/Qwen2.5-Coder-1.5B')}")

    # Run with uvicorn
    uvicorn.run(
        "think_ai_v3.app:app" if reload else app,
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
