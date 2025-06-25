"""Think AI - Conscious AI with Colombian Flavor: Distributed AGI Architecture with exponential intelligence growth."""

import os
import sys

__version__ = "2.1.0"
__author__ = "Champi (BDFL)"

# Import system optimizations first to configure environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Lazy import mechanism to prevent circular imports
_core_config = None
_core_engine = None
_parallel_processor = None
_intelligence_optimizer = None


def get_config():
    """Lazy load Config."""
    global _core_config
    if _core_config is None:
        from .core.config import Config

        _core_config = Config
    return _core_config


def get_engine():
    """Lazy load ThinkAIEngine."""
    global _core_engine
    if _core_engine is None:
        from .core.engine import ThinkAIEngine

        _core_engine = ThinkAIEngine
    return _core_engine


def get_parallel_processor():
    """Lazy load ParallelProcessor."""
    global _parallel_processor
    if _parallel_processor is None:
        from .parallel_processor import ParallelProcessor, parallel_processor, parallelize

        _parallel_processor = (ParallelProcessor, parallel_processor, parallelize)
    return _parallel_processor


# Only import dependency resolver on first use
_dependency_resolver = None


def get_dependency_resolver():
    """Lazy load dependency resolver."""
    global _dependency_resolver
    if _dependency_resolver is None:
        from .utils.dependency_resolver import dependency_resolver

        _dependency_resolver = dependency_resolver
    return _dependency_resolver


# For backward compatibility, create proxy objects
class _LazyProxy:
    def __init__(self, getter):
        self._getter = getter

    def __getattr__(self, name):
        return getattr(self._getter(), name)

    def __call__(self, *args, **kwargs):
        return self._getter()(*args, **kwargs)


# Export lazy proxies
Config = _LazyProxy(get_config)
ThinkAIEngine = _LazyProxy(get_engine)

# Optional imports with graceful fallback
try:
    from .intelligence_optimizer import (
        IntelligenceOptimizer,
        generate_text,
        get_embeddings,
        intelligence_optimizer,
        search_similar,
    )
    from .parallel_processor import parallel_processor, parallelize
except ImportError:
    # Graceful fallback if optimization modules not available
    parallel_processor = None
    intelligence_optimizer = None
    get_embeddings = None
    generate_text = None
    search_similar = None
    parallelize = None

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
