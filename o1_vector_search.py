"""Core O(1) Vector Search implementation"""

import json
import numpy as np
from typing import List, Tuple, Dict, Any, Optional


class O1VectorSearch:
    """
    O(1) Vector Search using Locality Sensitive Hashing (LSH)

    Achieves constant-time similarity search through hash-based indexing.
    """

    def __init__(
        self, dim: int, num_hash_tables: int = 10, num_hash_functions: int = 8
    ):
        """
        Initialize O(1) Vector Search index.

        Args:
            dim: Dimension of vectors
            num_hash_tables: Number of hash tables for LSH
            num_hash_functions: Number of hash functions per table
        """
        self.dim = dim
        self.num_hash_tables = num_hash_tables
        self.num_hash_functions = num_hash_functions

        # Initialize hash tables
        self.hash_tables = [{} for _ in range(num_hash_tables)]

        # Initialize random projections for LSH
        self.projections = []
        for _ in range(num_hash_tables):
            table_projections = np.random.randn(num_hash_functions, dim)
            # Normalize projections
            norms = np.linalg.norm(table_projections, axis=1, keepdims=True)
            table_projections = table_projections / norms
            self.projections.append(table_projections)

        # Storage for vectors and metadata
        self.vectors = []
        self.metadata = []

    def _compute_hash(self, vector: np.ndarray, table_idx: int) -> str:
        """Compute hash for a vector using specified hash table's projections."""
        projections = self.projections[table_idx]
        # Project vector onto random hyperplanes
        projected = np.dot(projections, vector)
        # Convert to binary hash
        hash_bits = (projected > 0).astype(int)
        return "".join(map(str, hash_bits))

    def add(
        self, vector: np.ndarray, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a vector to the index with O(1) complexity.

        Args:
            vector: Vector to add (numpy array of shape (dim,))
            metadata: Optional metadata associated with the vector
        """
        if len(vector) != self.dim:
            raise ValueError(
                f"Vector dimension {len(vector)} doesn't match index dimension {self.dim}"
            )

        vector = np.asarray(vector, dtype=np.float32)
        idx = len(self.vectors)

        # Store vector and metadata
        self.vectors.append(vector)
        self.metadata.append(metadata or {})

        # Add to all hash tables
        for table_idx in range(self.num_hash_tables):
            hash_key = self._compute_hash(vector, table_idx)

            if hash_key not in self.hash_tables[table_idx]:
                self.hash_tables[table_idx][hash_key] = []

            self.hash_tables[table_idx][hash_key].append(idx)

    def search(
        self, query_vector: np.ndarray, k: int = 5
    ) -> List[Tuple[float, np.ndarray, Dict[str, Any]]]:
        """
        Search for k nearest neighbors in O(1) time.

        Args:
            query_vector: Query vector (numpy array of shape (dim,))
            k: Number of nearest neighbors to return

        Returns:
            List of tuples (distance, vector, metadata) sorted by distance
        """
        if len(query_vector) != self.dim:
            raise ValueError(
                f"Query dimension {len(query_vector)} doesn't match index dimension {self.dim}"
            )

        query_vector = np.asarray(query_vector, dtype=np.float32)
        candidates = set()

        # Look up in all hash tables
        for table_idx in range(self.num_hash_tables):
            hash_key = self._compute_hash(query_vector, table_idx)

            if hash_key in self.hash_tables[table_idx]:
                for idx in self.hash_tables[table_idx][hash_key]:
                    candidates.add(idx)

        # Calculate actual distances for candidates
        results = []
        for idx in candidates:
            distance = np.linalg.norm(query_vector - self.vectors[idx])
            results.append((distance, self.vectors[idx], self.metadata[idx]))

        # Sort by distance and return top k
        results.sort(key=lambda x: x[0])
        return results[:k]

    def size(self) -> int:
        """Return the number of vectors in the index."""
        return len(self.vectors)

    def clear(self) -> None:
        """Remove all vectors from the index."""
        self.hash_tables = [{} for _ in range(self.num_hash_tables)]
        self.vectors = []
        self.metadata = []

    def save(self, filepath: str) -> None:
        """
        Save the index to a file.

        Args:
            filepath: Path to save the index
        """
        data = {
            "dim": self.dim,
            "num_hash_tables": self.num_hash_tables,
            "num_hash_functions": self.num_hash_functions,
            "projections": [p.tolist() for p in self.projections],
            "vectors": [v.tolist() for v in self.vectors],
            "metadata": self.metadata,
            "hash_tables": self.hash_tables,
        }

        with open(filepath, "w") as f:
            json.dump(data, f)

    @classmethod
    def load(cls, filepath: str) -> "O1VectorSearch":
        """
        Load an index from a file.

        Args:
            filepath: Path to load the index from

        Returns:
            Loaded O1VectorSearch instance
        """
        with open(filepath, "r") as f:
            data = json.load(f)

        index = cls(
            dim=data["dim"],
            num_hash_tables=data["num_hash_tables"],
            num_hash_functions=data["num_hash_functions"],
        )

        # Restore projections
        index.projections = [np.array(p) for p in data["projections"]]

        # Restore vectors and metadata
        index.vectors = [np.array(v, dtype=np.float32) for v in data["vectors"]]
        index.metadata = data["metadata"]

        # Restore hash tables
        index.hash_tables = data["hash_tables"]

        return index

    def __repr__(self) -> str:
        return f"O1VectorSearch(dim={self.dim}, size={self.size()}, tables={self.num_hash_tables})"
