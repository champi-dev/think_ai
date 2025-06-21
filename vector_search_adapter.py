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
            self.backend_name = "faiss"
            self.index = faiss.IndexFlatL2(dimension)
        elif backend == "annoy" and ANNOY_AVAILABLE:
            self.backend_name = "annoy"
            self.index = annoy.AnnoyIndex(dimension, "euclidean")
            self.built = False
        else:
            self.backend_name = "o1"
            self.index = O1VectorSearch(dimension)

    def add(self, vector: np.ndarray, data: dict = None) -> None:
        """Add a vector with optional metadata"""
        if self.backend_name == "faiss":
            self.index.add(np.array([vector], dtype=np.float32))
            self.data.append(data or {})
        elif self.backend_name == "annoy":
            idx = len(self.data)
            self.index.add_item(idx, vector)
            self.data.append(data or {})
            self.built = False
        else:  # o1
            self.index.add(vector, data)

    def search(self, query: np.ndarray, k: int = 5) -> List[Tuple[float, dict]]:
        """Search for k nearest neighbors"""
        if self.backend_name == "faiss":
            D, I = self.index.search(np.array([query], dtype=np.float32), k)
            results = []
            for i, (dist, idx) in enumerate(zip(D[0], I[0])):
                if idx >= 0 and idx < len(self.data):
                    results.append((float(dist), self.data[idx]))
            return results

        elif self.backend_name == "annoy":
            if not self.built:
                self.index.build(10)  # 10 trees
                self.built = True

            indices, distances = self.index.get_nns_by_vector(query, k, include_distances=True)
            results = []
            for idx, dist in zip(indices, distances):
                if idx < len(self.data):
                    results.append((dist, self.data[idx]))
            return results

        else:  # o1
            return self.index.search(query, k)

    def __len__(self) -> int:
        """Return number of indexed vectors"""
        if self.backend_name == "faiss":
            return self.index.ntotal
        elif self.backend_name in ["annoy", "o1"]:
            return len(self.data)
        return 0

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
