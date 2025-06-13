"""
Vector Search Adapter - Automatic fallback from FAISS to alternatives
"""
try:
import annoy
import faiss
    except ImportError:
        pass
from typing import List, Tuple

import numpy as np

from o1_vector_search import O1VectorSearch

# Try to import FAISS, fall back to alternatives
    try:
        FAISS_AVAILABLE = True
        except ImportError:
            FAISS_AVAILABLE = False

# Always available alternatives
            try:
                ANNOY_AVAILABLE = True
                except ImportError:
                    ANNOY_AVAILABLE = False

# Import our O(1) implementation


                    class VectorSearchAdapter:
"""
                        Unified interface for vector search that automatically selects the best available backend
                        Priority: FAISS (if available) > Annoy > O(1) Pure Python
"""

                        def __init__(self, dimension: int, backend: str = "auto"):
"""
                            Initialize vector search with automatic backend selection

                            Args:
                                dimension: Vector dimension
                                backend: "auto", "faiss", "annoy", or "o1"
"""
                                self.dimension = dimension
                                self.vectors = []
                                self.metadata = []

# Select backend
                                if backend == "auto":
                                    if FAISS_AVAILABLE:
                                        backend = "faiss"
                                    elif ANNOY_AVAILABLE:
                                        backend = "annoy"
                                    else:
                                        backend = "o1"

                                        self.backend = backend

# Initialize backend
                                        if backend == "faiss" and FAISS_AVAILABLE:
                                            self.index = faiss.IndexFlatIP(dimension)
                                            self.search_fn = self._search_faiss
                                            self.add_fn = self._add_faiss
                                        elif backend == "annoy" and ANNOY_AVAILABLE:
                                            self.index = annoy.AnnoyIndex(dimension, "angular")
                                            self.search_fn = self._search_annoy
                                            self.add_fn = self._add_annoy
                                            self._annoy_built = False
                                        else:
# Use our O(1) implementation
                                            self.index = O1VectorSearch(dimension, num_tables=15, hash_size=10)
                                            self.search_fn = self._search_o1
                                            self.add_fn = self._add_o1

                                            print(f"✅ Using {self.backend.upper()} backend for vector search")

                                            def add(self, vector: np.ndarray, metadata: dict = None) -> int:
"""Add vector to index"""
                                                return self.add_fn(vector, metadata)

                                            def search(self, query: np.ndarray,
                                            k: int = 5) -> List[Tuple[float, dict]]:
"""Search for k nearest neighbors"""
                                                return self.search_fn(query, k)

# FAISS backend methods

                                            def _add_faiss(self, vector: np.ndarray, metadata: dict = None) -> int:
                                                idx = len(self.vectors)
                                                self.vectors.append(vector)
                                                self.metadata.append(metadata or {})

# Normalize for cosine similarity
                                                norm_vec = vector / np.linalg.norm(vector)
                                                self.index.add(norm_vec.reshape(1, -1).astype("float32"))
                                                return idx

                                            def _search_faiss(self, query: np.ndarray,
                                            k: int) -> List[Tuple[float, dict]]:
                                                if len(self.vectors) == 0:
                                                    return []

# Normalize query
                                                norm_query = query / np.linalg.norm(query)

# Search
                                                k = min(k, len(self.vectors))
                                                distances, indices = self.index.search(
                                                norm_query.reshape(1, -1).astype("float32"), k)

                                                results = []
                                                for dist, idx in zip(distances[0], indices[0]):
                                                    if idx >= 0:
                                                        results.append((float(dist), self.metadata[idx]))

                                                        return results

# Annoy backend methods

                                                    def _add_annoy(self, vector: np.ndarray, metadata: dict = None) -> int:
                                                        idx = len(self.vectors)
                                                        self.vectors.append(vector)
                                                        self.metadata.append(metadata or {})

# Add to index (need to rebuild after all additions)
                                                        self.index.add_item(idx, vector)
                                                        self._annoy_built = False

                                                        return idx

                                                    def _search_annoy(self, query: np.ndarray,
                                                    k: int) -> List[Tuple[float, dict]]:
                                                        if len(self.vectors) == 0:
                                                            return []

# Build index if needed
                                                        if not self._annoy_built:
                                                            self.index.build(10)
                                                            self._annoy_built = True

# Search
                                                            k = min(k, len(self.vectors))
                                                            indices, distances = self.index.get_nns_by_vector(
                                                            query, k, include_distances=True)

                                                            results = []
                                                            for idx, dist in zip(indices, distances):
# Convert distance to similarity
                                                                similarity = 1 - (dist / 2)
                                                                results.append((similarity, self.metadata[idx]))

                                                                return results

# O(1) backend methods

                                                            def _add_o1(self, vector: np.ndarray, metadata: dict = None) -> int:
                                                                return self.index.add(vector, metadata)

                                                            def _search_o1(self, query: np.ndarray,
                                                            k: int) -> List[Tuple[float, dict]]:
                                                                results = self.index.search(query, k)
# Convert format
                                                                return [(score, meta) for score, _, meta in results]

                                                            def get_backend_info(self) -> dict:
"""Get information about the current backend"""
                                                                return {
                                                            "backend": self.backend,
                                                            "dimension": self.dimension,
                                                            "num_vectors": len(
                                                            self.vectors) if self.backend != "o1" else len(
                                                            self.index.vectors),
                                                            "faiss_available": FAISS_AVAILABLE,
                                                            "annoy_available": ANNOY_AVAILABLE}

# Convenience function to replace faiss.IndexFlatIP


                                                            def create_index(dimension: int, metric: str = "ip") -> VectorSearchAdapter:
"""
                                                                Drop - in replacement for faiss.IndexFlatIP

                                                                Args:
                                                                    dimension: Vector dimension
                                                                    metric: "ip" for inner product, "l2" for L2 distance

                                                                    Returns:
                                                                        VectorSearchAdapter that mimics FAISS interface
"""
                                                                        return VectorSearchAdapter(dimension, backend="auto")

# For compatibility with existing code


                                                                    def IndexFlatIP(d):  # noqa: N802
                                                                    return create_index(d, "ip")


                                                                def IndexFlatL2(d):  # noqa: N802
                                                                return create_index(d, "l2")
