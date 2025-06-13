"""Think AI - Conscious AI with Colombian Flavor: Distributed AGI Architecture with exponential intelligence growth."""

import os
import sys

from .core.config import Config
from .core.engine import ThinkAIEngine
from .parallel_processor import ParallelProcessor, parallel_processor, parallelize
from .system_config import SYSTEM_CONFIG, system_optimizer

# 🇨🇴 Initialize Think AI Dependency Resolver first - ¡Dale que vamos tarde!
# This provides optimized Colombian AI alternatives for problematic
# dependencies
from .utils.dependency_resolver import dependency_resolver

__version__ = "2.1.0"
__author__ = "Champi (BDFL)"

# Import system optimizations first to configure environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from .intelligence_optimizer import (
        IntelligenceOptimizer,
        generate_text,
        get_embeddings,
        intelligence_optimizer,
        search_similar,
    )

    # Apply optimizations on import
    _ = SYSTEM_CONFIG  # Trigger optimization application
except ImportError:
    # Graceful fallback if optimization modules not available
    parallel_processor = None
    intelligence_optimizer = None
    get_embeddings = None
    generate_text = None
    search_similar = None

# Core imports

__all__ = [
    "Config",
    "ThinkAIEngine",
    "__version__",
    "parallel_processor",
    "intelligence_optimizer",
    "get_embeddings",
    "generate_text",
    "search_similar",
    "parallelize",
]
