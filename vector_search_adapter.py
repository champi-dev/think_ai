"""
Vector Search Adapter - Automatic fallback from FAISS to alternatives
"""

from typing import List, Tuple

import numpy as np

# Try to import FAISS
try:
    import faiss

    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

# Try to import Annoy
try:
    import annoy

    ANNOY_AVAILABLE = True
except ImportError:
    ANNOY_AVAILABLE = False

# Import our O(1) implementation
from o1_vector_search import O1VectorSearch


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
            backend: Backend to use ("auto", "faiss", "annoy", "o1")
        """
        self.dimension = dimension
        self.backend_name = backend
        self.index = None
        self.data = []
        self.vectors = []  # For O1 backend compatibility

        # Auto-select backend
        if backend == "auto":
            if FAISS_AVAILABLE:
                backend = "faiss"
            elif ANNOY_AVAILABLE:
                backend = "annoy"
            else:
                backend = "o1"

        # Initialize selected backend
        if backend == "faiss" and FAISS_AVAILABLE:
            self.backend = "faiss"  # Use 'backend' as expected by tests
            self.backend_name = "faiss"
            self.index = faiss.IndexFlatL2(dimension)
        elif backend == "annoy" and ANNOY_AVAILABLE:
            self.backend = "annoy"  # Use 'backend' as expected by tests
            self.backend_name = "annoy"
            self.index = annoy.AnnoyIndex(dimension, "euclidean")
            self.built = False
        else:
            self.backend = "o1"  # Use 'backend' as expected by tests
            self.backend_name = "o1"
            self.index = O1VectorSearch(dimension)
            # For O1 backend, expose vectors for compatibility
            self.vectors = self.index.vectors if hasattr(self.index, "vectors") else []

    def add(self, vector: np.ndarray, data: dict = None) -> int:
        """Add a vector with optional metadata"""
        if self.backend_name == "faiss":
            idx = len(self.data)
            self.index.add(np.array([vector], dtype=np.float32))
            self.data.append(data or {})
            return idx
        elif self.backend_name == "annoy":
            idx = len(self.data)
            self.index.add_item(idx, vector)
            self.data.append(data or {})
            self.built = False
            return idx
        else:  # o1
            idx = self.index.add(vector, data)
            # Keep vectors in sync for O1 backend
            if hasattr(self.index, "vectors"):
                self.vectors = self.index.vectors
            return idx

    def search(self, query: np.ndarray, k: int = 5) -> List[Tuple[float, dict]]:
        """Search for k nearest neighbors"""
        # Handle edge cases
        if k <= 0:
            return []

        if self.backend_name == "faiss":
            if self.index.ntotal == 0:
                return []
            # Limit k to the number of vectors
            k = min(k, self.index.ntotal)
            D, I = self.index.search(np.array([query], dtype=np.float32), k)
            results = []
            for i, (dist, idx) in enumerate(zip(D[0], I[0])):
                if idx >= 0 and idx < len(self.data):
                    # Convert L2 distance to similarity score (0-1)
                    score = 1.0 / (1.0 + float(dist))
                    results.append((score, self.data[idx]))
            return results

        elif self.backend_name == "annoy":
            if len(self.data) == 0:
                return []
            if not self.built:
                self.index.build(10)  # 10 trees
                self.built = True
            # Limit k to the number of vectors
            k = min(k, len(self.data))

            indices, distances = self.index.get_nns_by_vector(query, k, include_distances=True)
            results = []
            for idx, dist in zip(indices, distances):
                if idx < len(self.data):
                    # Convert distance to similarity score
                    score = 1.0 / (1.0 + float(dist))
                    results.append((score, self.data[idx]))
            return results

        else:  # o1
            # O1VectorSearch returns (distance, vector, metadata)
            # We need to convert to (score, metadata)
            o1_results = self.index.search(query, k)
            results = []
            for distance, vector, metadata in o1_results:
                # Convert distance to similarity score
                score = 1.0 / (1.0 + float(distance))
                results.append((score, metadata))
            return results

    def get_backend_info(self) -> dict:
        """Get information about the current backend"""
        info = {
            "backend": self.backend,
            "dimension": self.dimension,
            "num_vectors": len(self),
            "faiss_available": FAISS_AVAILABLE,
            "annoy_available": ANNOY_AVAILABLE,
        }
        return info

    def __len__(self) -> int:
        """Return number of indexed vectors"""
        if self.backend_name == "faiss":
            return self.index.ntotal
        elif self.backend_name == "annoy":
            return len(self.data)
        else:  # o1
            return len(self.index.vectors) if hasattr(self.index, "vectors") else 0

    def clear(self) -> None:
        """Clear all indexed data"""
        if self.backend_name == "faiss":
            self.index.reset()
        elif self.backend_name == "annoy":
            self.index = annoy.AnnoyIndex(self.dimension, "euclidean")
            self.built = False
        else:  # o1
            self.index = O1VectorSearch(self.dimension)
        self.data = []
