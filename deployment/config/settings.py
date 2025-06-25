"""Deployment settings - max 40 lines."""

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
WEBAPP_DIR = PROJECT_ROOT / "webapp"

# Server settings
API_HOST = "0.0.0.0"
API_PORT = int(os.environ.get("PORT", 8080))
WEBAPP_PORT = int(os.environ.get("WEBAPP_PORT", 3000))

# Features
FEATURES = {
    "o1_performance": True,
    "consciousness": True,
    "intelligence": True,
    "coding": True,
    "vector_search": True,
}

# API info
API_INFO = {
    "title": "Think AI Full System",
    "version": "5.0",
    "description": "O(1) AI with consciousness"
}