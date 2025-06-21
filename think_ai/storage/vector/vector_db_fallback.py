"""Fallback vector database implementation that works without faiss.
Uses pure Python/NumPy for vector similarity search.
"""

import json
import logging
import pickle
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Tuple

import numpy as np

from .fast_vector_db import FastVectorDB

logger = logging.getLogger(__name__)


@dataclass
class VectorResult:
    """Result from vector similarity search."""

    id: str
    score: float
    metadata: dict[str, Any]
    vector: np.ndarray | None = None


class NumpyVectorDB:
    """Pure NumPy-based vector database for fallback when faiss is not available.

    This implementation uses NumPy for all vector operations,
    providing:
        - Cosine similarity search
        - In-memory storage with disk persistence
        - No external dependencies beyond NumPy
    """

    def __init__(self, dimension: int = 384, cache_dir: str = None):
        self.dimension = dimension
        # Use provided cache_dir or create a temporary directory that's
        # writable
        if cache_dir is None:
            cache_dir = Path(tempfile.gettempdir()) / \
                "think_ai_vectordb_fallback"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # In-memory storage
        self.vectors = []
        self.ids = []
        self.metadata = []

        # Load existing data if available
        self._load_from_disk()

    def add(
            self,
            vectors: np.ndarray,
            ids: List[str],
            metadata: List[dict] = None):
        """Add vectors to the database."""
        if metadata is None:
            metadata = [{}] * len(ids)

        # Normalize vectors for cosine similarity
        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)

        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        normalized_vectors = vectors / (norms + 1e-10)

        self.vectors.extend(normalized_vectors)
        self.ids.extend(ids)
        self.metadata.extend(metadata)

        # Save to disk
        self._save_to_disk()

    def search(self, query_vector: np.ndarray,
               k: int = 10) -> List[VectorResult]:
        """Search for k nearest neighbors using cosine similarity."""
        if len(self.vectors) == 0:
            return []

        # Normalize query vector
        query_norm = np.linalg.norm(query_vector)
        if query_norm > 0:
            query_vector = query_vector / query_norm

        # Compute cosine similarities
        vectors_array = np.array(self.vectors)
        similarities = np.dot(vectors_array, query_vector)

        # Get top k indices
        k = min(k, len(self.vectors))
        top_indices = np.argpartition(similarities, -k)[-k:]
        top_indices = top_indices[np.argsort(similarities[top_indices])[::-1]]

        # Build results
        results = []
        for idx in top_indices:
            results.append(
                VectorResult(
                    id=self.ids[idx],
                    score=float(similarities[idx]),
                    metadata=self.metadata[idx],
                    vector=self.vectors[idx],
                )
            )

        return results

    def delete(self, ids: List[str]):
        """Delete vectors by ID."""
        indices_to_remove = [i for i, id_ in enumerate(self.ids) if id_ in ids]

        for idx in sorted(indices_to_remove, reverse=True):
            del self.vectors[idx]
            del self.ids[idx]
            del self.metadata[idx]

        self._save_to_disk()

    def _save_to_disk(self):
        """Save the database to disk."""
        data = {
            "vectors": self.vectors,
            "ids": self.ids,
            "metadata": self.metadata}

        save_path = self.cache_dir / "numpy_vectors.pkl"
        with open(save_path, "wb") as f:
            pickle.dump(data, f)

    def _load_from_disk(self):
        """Load the database from disk."""
        save_path = self.cache_dir / "numpy_vectors.pkl"

        if save_path.exists():
            try:
                with open(save_path, "rb") as f:
                    data = pickle.load(f)
                    self.vectors = data.get("vectors", [])
                    self.ids = data.get("ids", [])
                    self.metadata = data.get("metadata", [])
                    logger.info(
                        f"Loaded {len(self.vectors)} vectors from disk")
            except Exception as e:
                logger.warning(f"Failed to load vectors from disk: {e}")


class VectorDBAdapter:
    """Adapter that automatically selects the best available vector database implementation."""

    def __init__(self, dimension: int = 384, cache_dir: str = None, **kwargs):
        self.dimension = dimension
        # Use provided cache_dir or let individual DBs use their defaults
        if cache_dir is None:
            cache_dir = Path(tempfile.gettempdir()) / \
                "think_ai_vectordb_adapter"
        self.cache_dir = cache_dir
        self.db = None

        # Try to import and use faiss if available
        try:
            self.db = FastVectorDB(
                dimension=dimension, cache_dir=str(cache_dir), **kwargs
            )
            logger.info("Using FAISS vector database")
        except ImportError:
            logger.info("FAISS not available, using NumPy fallback")
            self.db = NumpyVectorDB(
                dimension=dimension,
                cache_dir=str(cache_dir))

    def add(
            self,
            vectors: np.ndarray,
            ids: List[str],
            metadata: List[dict] = None):
        """Add vectors to the database."""
        if hasattr(self.db, "add"):
            return self.db.add(vectors, ids, metadata)
        elif hasattr(self.db, "add_vectors"):
            return self.db.add_vectors(vectors, ids, metadata)
        else:
            raise AttributeError(
                "Vector database does not support adding vectors")

    def search(self, query_vector: np.ndarray, k: int = 10):
        """Search for k nearest neighbors."""
        return self.db.search(query_vector, k)

    def delete(self, ids: List[str]):
        """Delete vectors by ID."""
        if hasattr(self.db, "delete"):
            return self.db.delete(ids)
        else:
            logger.warning("Vector database does not support deletion")
