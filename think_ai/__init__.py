"""Think AI: A comprehensive AI system for universal knowledge access."""

__version__ = "0.1.0"
__author__ = "Think AI Foundation"

from .core.config import Config
from .core.engine import ThinkAIEngine

__all__ = ["Config", "ThinkAIEngine", "__version__"]