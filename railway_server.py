#!/usr/bin/env python3
"""Ultra-minimal server for Railway deployment."""

import os
import sys

print("Starting Railway server...")
print(f"Python version: {sys.version}")
print(f"PORT env var: {os.environ.get('PORT', 'NOT SET')}")

try:
    import uvicorn
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    print("Successfully imported FastAPI and uvicorn")
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

app = FastAPI(title="Think AI Railway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Think AI is running on Railway!"}


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "think-ai-railway"}


@app.post("/chat")
async def chat(message: str = "Hello"):
    return {"response": f"Echo: {message}"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting server on 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
