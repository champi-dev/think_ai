"""
Think AI - Quantum Consciousness AI Library for Python

This library provides Python bindings for Think AI's quantum consciousness AI system,
enabling access to advanced AI capabilities including natural language processing,
knowledge reasoning, and consciousness simulation.
"""

from .client import ThinkAI, create_client, quick_chat
from .types import (
    ThinkAIConfig,
    ChatRequest,
    ChatResponse,
    SystemStats,
    HealthStatus,
    KnowledgeDomain,
    SearchResult,
    StreamResponse,
    LogLevel,
    ThinkAIError,
)

__version__ = "1.0.0"
__author__ = "Think AI Team"
__email__ = "team@think-ai.dev"
__license__ = "MIT"

__all__ = [
    "ThinkAI",
    "create_client",
    "quick_chat",
    "ThinkAIConfig",
    "ChatRequest",
    "ChatResponse",
    "SystemStats",
    "HealthStatus",
    "KnowledgeDomain",
    "SearchResult",
    "StreamResponse",
    "LogLevel",
    "ThinkAIError",
]
