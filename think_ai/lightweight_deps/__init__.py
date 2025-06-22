"""Lightweight dependency replacements for Think AI.

These modules provide O(1) minimal implementations of external dependencies
to ensure the system can run without heavy ML libraries.
"""

from . import transformers
from . import chromadb
from . import tqdm
from . import opentelemetry
from . import sentence_transformers
from . import huggingface_hub

__all__ = [
    "transformers",
    "chromadb", 
    "tqdm",
    "opentelemetry",
    "sentence_transformers",
    "huggingface_hub"
]