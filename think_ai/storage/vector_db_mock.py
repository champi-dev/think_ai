"""Mock vector database implementation."""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class VectorSearchResult:
    """Vector search result."""
    id: str
    content: str
    distance: float
    metadata: Dict[str, Any]


class MilvusDB:
    """Mock Milvus vector database."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._vectors = {}
        self._metadata = {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize mock Milvus."""
        logger.info("Initializing mock Milvus vector database")
        self._initialized = True
    
    async def create_collection(self, collection_name: str, dimension: int) -> None:
        """Create mock collection."""
        logger.info(f"Created mock collection: {collection_name}")
    
    async def insert(self, collection_name: str, vectors: List[List[float]], 
                    metadata: List[Dict[str, Any]]) -> List[str]:
        """Insert vectors."""
        ids = []
        for i, (vec, meta) in enumerate(zip(vectors, metadata)):
            vec_id = f"{collection_name}_{len(self._vectors)}"
            self._vectors[vec_id] = np.array(vec)
            self._metadata[vec_id] = meta
            ids.append(vec_id)
        return ids
    
    async def search(self, collection_name: str, query_vectors: List[List[float]], 
                    top_k: int = 10) -> List[List[VectorSearchResult]]:
        """Search similar vectors."""
        results = []
        for query_vec in query_vectors:
            query_vec = np.array(query_vec)
            distances = []
            
            for vec_id, vec in self._vectors.items():
                if vec_id.startswith(collection_name):
                    dist = np.linalg.norm(query_vec - vec)
                    distances.append((vec_id, dist))
            
            distances.sort(key=lambda x: x[1])
            
            search_results = []
            for vec_id, dist in distances[:top_k]:
                meta = self._metadata.get(vec_id, {})
                search_results.append(VectorSearchResult(
                    id=vec_id,
                    content=meta.get("content", ""),
                    distance=dist,
                    metadata=meta
                ))
            results.append(search_results)
        
        return results
    
    async def close(self) -> None:
        """Close mock Milvus."""
        self._initialized = False
        logger.info("Mock Milvus closed")


class VectorDB:
    """Alias for MilvusDB."""
    pass


def create_vector_db(db_type: str = "milvus", config: Optional[Dict[str, Any]] = None) -> MilvusDB:
    """Create mock vector database."""
    return MilvusDB(config)