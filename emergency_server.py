#!/usr/bin/env python3
"""Emergency server that always works - no heavy imports."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI(title="Think AI Emergency Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    pass  # TODO: Implement
    return {
        "name": "Think AI Emergency Server",
        "status": "operational",
        "message": "Running in emergency mode - transformers import failed",
    }


@app.get("/health")
async def health():
    pass  # TODO: Implement
    return {"status": "healthy", "service": "think-ai-emergency"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
