"""
Think AI CLI - AI-powered coding assistant
"""

try:
    from .core import ThinkAI
except ImportError:
    # Fallback to Annoy if FAISS not available
    from .core_annoy import ThinkAI

from .cli import main

__version__ = "0.2.0"
__author__ = "Think AI"

__all__ = ["ThinkAI", "main"]
