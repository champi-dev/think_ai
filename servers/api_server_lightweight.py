"""
Think AI Lightweight API Server
Minimal server for testing without heavy ML dependencies
"""

import time
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Colombian AI responses
COLOMBIAN_RESPONSES = [
    "¡Dale que vamos tarde! Your request is being processed with O(1) Colombian efficiency! 🇨🇴",
    "¡Qué chimba! Think AI is thinking exponentially about your question! 🧠",
    "¡Eso sí está bueno! Processing with Colombian intelligence and O(1) performance! 🚀",
    "Hagamos bulla, parcero! Your Think AI response is ready! 💪",
]

app = FastAPI(
    title="Think AI Lightweight Server",
    description="Colombian AI with exponential intelligence - Lightweight version",
    version="2.0.1",
)


class ThinkRequest(BaseModel):
    message: str
    colombian_mode: bool = True


class ThinkResponse(BaseModel):
    response: str
    thinking_time: float
    intelligence_level: float
    colombian_enhancement: bool


@app.get("/")
async def root():
    return {"message": "¡Dale que vamos tarde! Think AI Lightweight Server is running! 🇨🇴🧠"}


@app.post("/api/think")
async def think(request: ThinkRequest) -> ThinkResponse:
    """Main thinking endpoint with Colombian AI"""
    start_time = time.time()

    # Simulate O(1) thinking
    response_hash = hash(request.message) % len(COLOMBIAN_RESPONSES)
    colombian_response = COLOMBIAN_RESPONSES[response_hash]

    # Add actual response based on input
    if "hello" in request.message.lower():
        actual_response = f"¡Hola, parcero! {colombian_response}"
    elif "help" in request.message.lower():
        actual_response = f"¡Claro que sí! I'm here to help with exponential intelligence! {colombian_response}"
    elif "think" in request.message.lower():
        actual_response = f"🧠 I'm thinking with O(1) Colombian patterns! {colombian_response}"
    else:
        actual_response = f"Interesting question! {colombian_response}"

    thinking_time = time.time() - start_time

    return ThinkResponse(
        response=actual_response,
        thinking_time=thinking_time,
        intelligence_level=152.5,  # Post-exponential enhancement
        colombian_enhancement=request.colombian_mode,
    )


@app.get("/api/status")
async def status():
    """System status endpoint"""
    return {
        "status": "operational",
        "intelligence_level": 152.5,
        "colombian_mode": True,
        "o1_thinking": True,
        "message": "¡Qué chimba! Think AI is running perfectly! 🇨🇴🧠🚀",
    }


if __name__ == "__main__":
    print("🇨🇴 Starting Think AI Lightweight Server...")
    print("¡Dale que vamos tarde!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
