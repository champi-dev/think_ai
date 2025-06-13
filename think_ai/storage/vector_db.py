"""Vector database abstraction for Think AI."""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class VectorSearchResult:
    """Result from vector similarity search."""

    id: str
    score: float
    metadata: Dict[str, Any]
    vector: Optional[np.ndarray] = None


class VectorDB(ABC):
    """Abstract base class for vector databases."""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the vector database."""
        pass

    @abstractmethod
    async def add_vectors(
        self, vectors: List[np.ndarray], ids: List[str], metadata: List[Dict[str, Any]]
    ) -> None:
        """Add vectors to the database."""
        pass

    @abstractmethod
    async def search(
        self, query_vector: np.ndarray, top_k: int = 10
    ) -> List[VectorSearchResult]:
        """Search for similar vectors."""
        pass

    @abstractmethod
    async def delete(self, ids: List[str]) -> None:
        """Delete vectors by IDs."""
        pass

    @abstractmethod
    async def get_vector_count(self) -> int:
        """Get total number of vectors."""
        pass


class InMemoryVectorDB(VectorDB):
    """Simple in-memory vector database for testing."""

    def __init__(self, dimension: int):
        """Initialize in-memory vector database."""
        self.dimension = dimension
        self.vectors = {}
        self.metadata = {}
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the in-memory database."""
        self._initialized = True
        logger.info(f"Initialized in-memory vector DB (dim={self.dimension})")

    async def add_vectors(
        self, vectors: List[np.ndarray], ids: List[str], metadata: List[Dict[str, Any]]
    ) -> None:
        """Add vectors to memory."""
        if not self._initialized:
            await self.initialize()

        for vector, vector_id, meta in zip(vectors, ids, metadata):
            if len(vector) != self.dimension:
                raise ValueError(
                    f"Vector dimension mismatch: expected {
                        self.dimension}, got {
                        len(vector)}"
                )

            self.vectors[vector_id] = vector.copy()
            self.metadata[vector_id] = meta.copy()

        logger.debug(f"Added {len(vectors)} vectors to in-memory DB")

    async def search(
        self, query_vector: np.ndarray, top_k: int = 10
    ) -> List[VectorSearchResult]:
        """Search for similar vectors using cosine similarity."""
        if not self._initialized:
            await self.initialize()

        if len(query_vector) != self.dimension:
            raise ValueError(
                f"Query vector dimension mismatch: expected {
                    self.dimension}, got {
                    len(query_vector)}"
            )

        if not self.vectors:
            return []

        # Calculate similarities
        similarities = []
        for vector_id, vector in self.vectors.items():
            # Cosine similarity
            dot_product = np.dot(query_vector, vector)
            norm_query = np.linalg.norm(query_vector)
            norm_vector = np.linalg.norm(vector)

            if norm_query > 0 and norm_vector > 0:
                similarity = dot_product / (norm_query * norm_vector)
            else:
                similarity = 0.0

            similarities.append((vector_id, similarity))

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top-k results
        results = []
        for vector_id, score in similarities[:top_k]:
            result = VectorSearchResult(
                id=vector_id,
                score=score,
                metadata=self.metadata[vector_id],
                vector=self.vectors[vector_id],
            )
            results.append(result)

        return results

    async def delete(self, ids: List[str]) -> None:
        """Delete vectors by IDs."""
        for vector_id in ids:
            self.vectors.pop(vector_id, None)
            self.metadata.pop(vector_id, None)

        logger.debug(f"Deleted {len(ids)} vectors from in-memory DB")

    async def get_vector_count(self) -> int:
        """Get total number of vectors."""
        return len(self.vectors)


class FaissVectorDB(VectorDB):
    """FAISS-based vector database for high performance."""

    def __init__(self, dimension: int, index_type: str = "FlatIP"):
        """Initialize FAISS vector database."""
        self.dimension = dimension
        self.index_type = index_type
        self.index = None
        self.id_map = {}
        self.metadata = {}
        self._next_id = 0
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize FAISS index."""
        if self._initialized:
            return

        try:
            import faiss

            # Create FAISS index
            if self.index_type == "FlatIP":
                self.index = faiss.IndexFlatIP(self.dimension)
            elif self.index_type == "FlatL2":
                self.index = faiss.IndexFlatL2(self.dimension)
            else:
                raise ValueError(f"Unsupported index type: {self.index_type}")

            self._initialized = True
            logger.info(
                f"Initialized FAISS vector DB (dim={
                    self.dimension}, type={
                    self.index_type})"
            )

        except ImportError:
            logger.warning(
                "FAISS not available, falling back to in-memory implementation"
            )
            # Fallback to in-memory
            self._fallback = InMemoryVectorDB(self.dimension)
            await self._fallback.initialize()
            self._initialized = True

    async def add_vectors(
        self, vectors: List[np.ndarray], ids: List[str], metadata: List[Dict[str, Any]]
    ) -> None:
        """Add vectors to FAISS index."""
        if not self._initialized:
            await self.initialize()

        if hasattr(self, "_fallback"):
            return await self._fallback.add_vectors(vectors, ids, metadata)

        # Convert to float32 numpy array
        vector_array = np.array(vectors, dtype=np.float32)

        # Add to FAISS index
        start_idx = self.index.ntotal
        self.index.add(vector_array)

        # Update mappings
        for i, (vector_id, meta) in enumerate(zip(ids, metadata)):
            faiss_idx = start_idx + i
            self.id_map[faiss_idx] = vector_id
            self.metadata[vector_id] = meta

        logger.debug(f"Added {len(vectors)} vectors to FAISS DB")

    async def search(
        self, query_vector: np.ndarray, top_k: int = 10
    ) -> List[VectorSearchResult]:
        """Search using FAISS index."""
        if not self._initialized:
            await self.initialize()

        if hasattr(self, "_fallback"):
            return await self._fallback.search(query_vector, top_k)

        # Prepare query
        query_array = np.array([query_vector], dtype=np.float32)

        # Search
        scores, indices = self.index.search(query_array, top_k)

        # Convert results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and idx in self.id_map:
                vector_id = self.id_map[idx]
                result = VectorSearchResult(
                    id=vector_id,
                    score=float(score),
                    metadata=self.metadata[vector_id])
                results.append(result)

        return results

    async def delete(self, ids: List[str]) -> None:
        """Delete vectors (not efficiently supported by FAISS)."""
        if hasattr(self, "_fallback"):
            return await self._fallback.delete(ids)

        # Remove from metadata
        for vector_id in ids:
            self.metadata.pop(vector_id, None)

        # Note: FAISS doesn't support efficient deletion
        # In production, you'd rebuild the index periodically
        logger.warning(
            "FAISS deletion is not efficient - consider rebuilding index")

    async def get_vector_count(self) -> int:
        """Get total number of vectors."""
        if hasattr(self, "_fallback"):
            return await self._fallback.get_vector_count()

        return self.index.ntotal if self.index else 0


def create_vector_db(dimension: int, db_type: str = "memory") -> VectorDB:
    """Create a vector database instance."""
    if db_type == "memory":
        return InMemoryVectorDB(dimension)
    elif db_type == "faiss":
        return FaissVectorDB(dimension)
    else:
        raise ValueError(f"Unsupported vector DB type: {db_type}")


# Export main classes
__all__ = [
    "VectorDB",
    "VectorSearchResult",
    "InMemoryVectorDB",
    "FaissVectorDB",
    "create_vector_db",
]
