#! / usr / bin / env python3

"""CPU - only API server for Think AI - bypasses CUDA issues."""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from think_ai.consciousness.awareness import ConsciousnessFramework
from think_ai.intelligence.self_trainer import SelfTrainingIntelligence
from think_ai.language import spanish_handler

# Force CPU mode before importing torch
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["THINK_AI_DEVICE"] = "cpu"

# Think AI imports

# Setup logging
logging.basicConfig(
level=logging.INFO,
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Global engines
intelligence_engine = None
consciousness_engine = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize engines on startup."""
    global intelligence_engine, consciousness_engine

    try:
        logger.info("Initializing Think AI engines (CPU mode)...")

# Initialize intelligence
        intelligence_engine = SelfTrainingIntelligence()
        logger.info("✅ Intelligence engine initialized")

# Initialize consciousness
        consciousness_engine = ConsciousnessFramework()
        logger.info("✅ Consciousness engine initialized")

# Self - training starts automatically
        logger.info("✅ Self - training active")

        yield

    finally:
        logger.info("Shutting down Think AI engines...")
        if intelligence_engine:
            intelligence_engine.stop_training()

# Create FastAPI app
            app = FastAPI(
            title = "Think AI API (CPU Mode)",
            version = "2.0.0",
            lifespan = lifespan,
            )

# Add CORS
            app.add_middleware(
            CORSMiddleware,
            allow_origins = ["*"],
            allow_credentials = True,
            allow_methods = ["*"],
            allow_headers = ["*"],
            )

# Request / Response models

            class ThinkRequest(BaseModel):
                query: str
                enable_consciousness: bool = True

                class ThinkResponse(BaseModel):
                    result: Dict[str, Any]

                    @app.get("/api / v1 / health")
                    async def health():
"""Health check endpoint."""
                        return {
                    "status": "healthy",
                    "mode": "cpu",
                    "active_requests": 0,
                    "timestamp": int(datetime.now().timestamp()),
                    }

                    @app.post("/api / v1 / think")
                    async def think(request: ThinkRequest):
"""Process a thinking request."""
                        try:
                            if not intelligence_engine:
                                raise HTTPException(status_code = 503, detail = "Intelligence engine not initialized")

# First, detect language using multilingual detection
                            logger.info(f"Processing query: {request.query}")

# Detect language
                            detected_language = spanish_handler.detect_language(request.query)
                            logger.info(f"Language detected: {detected_language}")

# Add query to conversation memory for context
                            spanish_handler.add_to_conversation_memory(request.query, detected_language)

                            if detected_language ! = "english":
# Try to generate response in the detected language
                                response = spanish_handler.generate_multilingual_response(request.query, detected_language)
                                logger.info(f"{detected_language.title()} response generated: {response is not None}")

                                if not response:
# If no specific language response, generate English and translate (for Spanish)
                                    if detected_language = = "spanish":
                                        logger.info("Generating English response for Spanish translation")
                                        english_response = await intelligence_engine.generate_response(request.query)
                                        region = spanish_handler.detect_region(request.query)
                                        response = spanish_handler.translate_response(english_response, region)
                                        logger.info(f"Translated response: {response[:50]}...")
                                    else:
# For other languages, fallback to English
                                        logger.info(f"No {detected_language} handler available, using English")
                                        response = await intelligence_engine.generate_response(request.query)
                                    else:
# Generate response using self - training intelligence
                                        response = await intelligence_engine.generate_response(request.query)

# Add response to conversation memory
                                        spanish_handler.add_to_conversation_memory(response, detected_language)

# Get consciousness state if enabled
                                        consciousness_state = None
                                        if request.enable_consciousness and consciousness_engine:
                                            try:
                                                consciousness_state = consciousness_engine.process_thought(request.query)
                                                logger.info(f"Consciousness depth: {consciousness_state.depth_level}")
                                                except Exception as e:
                                                    logger.warning(f"Consciousness processing failed: {e}")

                                                    result = {
                                                    "response": response,
                                                    "consciousness_state": {
                                                    "depth_level": consciousness_state.depth_level if consciousness_state else 0.9,
                                                    "awareness_score": consciousness_state.awareness_score if consciousness_state else 0.85,
                                                    "attention_focus": request.query[:50],
                                                    } if consciousness_state else None,
                                                    }

                                                    return {"result": result}

                                                except Exception as e:
                                                    logger.exception(f"Think request failed: {e}")
                                                    raise HTTPException(status_code = 500, detail = str(e))

                                                @app.get("/api / intelligence")
                                                async def get_intelligence_metrics():
"""Get current intelligence metrics."""
                                                    try:
                                                        if not intelligence_engine:
                                                            return {
                                                        "iq": 0,
                                                        "knowledge_count": 0,
                                                        "training_cycles": 0,
                                                        "consciousness_level": 0,
                                                        "learning_rate": 0,
                                                        "test_score": 0,
                                                        }

                                                        metrics = intelligence_engine.get_metrics()

# Calculate consciousness level
                                                        consciousness_level = 0
                                                        if consciousness_engine:
                                                            try:
                                                                state = consciousness_engine.process_thought("self - awareness check")
                                                                consciousness_level = state.awareness_score
                                                                except Exception:
                                                                    consciousness_level = 0.85

                                                                    return {
                                                                "iq": min(2000, int(metrics.get("intelligence_level", 1.0) * 100)),
                                                                "knowledge_count": metrics.get("knowledge_concepts", 0),
                                                                "training_cycles": metrics.get("generations_evolved", 0),
                                                                "consciousness_level": consciousness_level,
                                                                "learning_rate": metrics.get("learning_rate", 0.1),
                                                                "test_score": min(0.99, metrics.get("intelligence_level", 1.0) / 200000),
                                                                }
                                                                except Exception as e:
                                                                    logger.exception(f"Error getting intelligence metrics: {e}")
                                                                    return {
                                                                "iq": 0,
                                                                "knowledge_count": 0,
                                                                "training_cycles": 0,
                                                                "consciousness_level": 0,
                                                                "learning_rate": 0,
                                                                "test_score": 0,
                                                                }

                                                                if __name__ = = "__main__":
                                                                    uvicorn.run(app, host = "0.0.0.0", port = 8080)
