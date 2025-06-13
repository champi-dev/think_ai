"""Vector database implementations for semantic search."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import asyncio

from ..core.config import VectorDBConfig
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
        """Initialize the vector database connection."""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close the vector database connection."""
        pass
    
    @abstractmethod
    async def create_collection(self, collection_name: str, dimension: int) -> None:
        """Create a collection for storing vectors."""
        pass
    
    @abstractmethod
    async def insert_vectors(
        self,
        collection_name: str,
        vectors: List[np.ndarray],
        ids: List[str],
        metadata: List[Dict[str, Any]]
    ) -> None:
        """Insert vectors with metadata."""
        pass
    
    @abstractmethod
    async def search(
        self,
        collection_name: str,
        query_vector: np.ndarray,
        top_k: int = 10,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        """Search for similar vectors."""
        pass
    
    @abstractmethod
    async def delete_vectors(self, collection_name: str, ids: List[str]) -> None:
        """Delete vectors by IDs."""
        pass
    
    @abstractmethod
    async def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get statistics about a collection."""
        pass


class MilvusDB(VectorDB):
    """Milvus vector database implementation."""
    
    def __init__(self, config: VectorDBConfig):
        self.config = config
        self.client = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize Milvus connection."""
        if self._initialized:
            return
        
        try:
            from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
            
            # Connect to Milvus
            await asyncio.get_event_loop().run_in_executor(
                None,
                connections.connect,
                "default",
                {"host": self.config.host, "port": self.config.port}
            )
            
            self._initialized = True
            logger.info("Milvus vector database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Milvus: {e}")
            raise
    
    async def close(self) -> None:
        """Close Milvus connection."""
        if self._initialized:
            from pymilvus import connections
            connections.disconnect("default")
            self._initialized = False
    
    async def create_collection(self, collection_name: str, dimension: int) -> None:
        """Create a Milvus collection."""
        from pymilvus import Collection, FieldSchema, CollectionSchema, DataType, utility
        
        # Check if collection exists
        if await self._collection_exists(collection_name):
            logger.info(f"Collection {collection_name} already exists")
            return
        
        # Define schema
        fields = [
            FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=128),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
            FieldSchema(name="metadata", dtype=DataType.JSON)
        ]
        
        schema = CollectionSchema(
            fields=fields,
            description=f"Think AI vector collection: {collection_name}"
        )
        
        # Create collection
        collection = Collection(name=collection_name, schema=schema)
        
        # Create HNSW index for fast search
        index_params = {
            "metric_type": self.config.metric_type,
            "index_type": self.config.index_type,
            "params": {
                "M": self.config.m,
                "efConstruction": self.config.ef_construction
            }
        }
        
        await asyncio.get_event_loop().run_in_executor(
            None,
            collection.create_index,
            "vector",
            index_params
        )
        
        # Load collection to memory
        collection.load()
        
        logger.info(f"Created Milvus collection: {collection_name}")
    
    async def insert_vectors(
        self,
        collection_name: str,
        vectors: List[np.ndarray],
        ids: List[str],
        metadata: List[Dict[str, Any]]
    ) -> None:
        """Insert vectors into Milvus."""
        from pymilvus import Collection
        
        collection = Collection(collection_name)
        
        # Prepare data
        data = [
            ids,
            [vector.tolist() for vector in vectors],
            metadata
        ]
        
        # Insert
        await asyncio.get_event_loop().run_in_executor(
            None,
            collection.insert,
            data
        )
        
        # Flush to ensure persistence
        collection.flush()
        
        logger.info(f"Inserted {len(vectors)} vectors into {collection_name}")
    
    async def search(
        self,
        collection_name: str,
        query_vector: np.ndarray,
        top_k: int = 10,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        """Search for similar vectors in Milvus."""
        from pymilvus import Collection
        
        collection = Collection(collection_name)
        
        # Prepare search parameters
        search_params = {
            "metric_type": self.config.metric_type,
            "params": {"ef": 128}
        }
        
        # Build filter expression if provided
        expr = None
        if filter_dict:
            conditions = []
            for key, value in filter_dict.items():
                if isinstance(value, str):
                    conditions.append(f'metadata["{key}"] == "{value}"')
                else:
                    conditions.append(f'metadata["{key}"] == {value}')
            expr = " && ".join(conditions) if conditions else None
        
        # Search
        results = await asyncio.get_event_loop().run_in_executor(
            None,
            collection.search,
            [query_vector.tolist()],
            "vector",
            search_params,
            top_k,
            expr,
            ["id", "metadata"]
        )
        
        # Convert to VectorSearchResult
        search_results = []
        for hits in results:
            for hit in hits:
                search_results.append(VectorSearchResult(
                    id=hit.id,
                    score=hit.distance,
                    metadata=hit.entity.get("metadata", {})
                ))
        
        return search_results
    
    async def delete_vectors(self, collection_name: str, ids: List[str]) -> None:
        """Delete vectors from Milvus."""
        from pymilvus import Collection
        
        collection = Collection(collection_name)
        
        # Build delete expression
        expr = f'id in {ids}'
        
        await asyncio.get_event_loop().run_in_executor(
            None,
            collection.delete,
            expr
        )
        
        logger.info(f"Deleted {len(ids)} vectors from {collection_name}")
    
    async def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get Milvus collection statistics."""
        from pymilvus import Collection
        
        collection = Collection(collection_name)
        
        stats = {
            "name": collection_name,
            "num_entities": collection.num_entities,
            "schema": str(collection.schema),
            "indexes": []
        }
        
        # Get index info
        for field in collection.schema.fields:
            if field.name == "vector":
                index = collection.index()
                if index:
                    stats["indexes"].append({
                        "field": field.name,
                        "index_type": index.params.get("index_type"),
                        "metric_type": index.params.get("metric_type")
                    })
        
        return stats
    
    async def _collection_exists(self, collection_name: str) -> bool:
        """Check if collection exists."""
        from pymilvus import utility
        
        return await asyncio.get_event_loop().run_in_executor(
            None,
            utility.has_collection,
            collection_name
        )


class QdrantDB(VectorDB):
    """Qdrant vector database implementation."""
    
    def __init__(self, config: VectorDBConfig):
        self.config = config
        self.client = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize Qdrant connection."""
        if self._initialized:
            return
        
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models
            
            # Create client
            self.client = QdrantClient(
                host=self.config.host,
                port=self.config.port,
                prefer_grpc=True
            )
            
            # Test connection
            await asyncio.get_event_loop().run_in_executor(
                None,
                self.client.get_collections
            )
            
            self._initialized = True
            logger.info("Qdrant vector database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant: {e}")
            raise
    
    async def close(self) -> None:
        """Close Qdrant connection."""
        self._initialized = False
    
    async def create_collection(self, collection_name: str, dimension: int) -> None:
        """Create a Qdrant collection."""
        from qdrant_client.http import models
        
        # Check if collection exists
        collections = await asyncio.get_event_loop().run_in_executor(
            None,
            self.client.get_collections
        )
        
        if any(c.name == collection_name for c in collections.collections):
            logger.info(f"Collection {collection_name} already exists")
            return
        
        # Create collection with HNSW index
        await asyncio.get_event_loop().run_in_executor(
            None,
            self.client.create_collection,
            collection_name,
            models.VectorParams(
                size=dimension,
                distance=models.Distance.COSINE
                if self.config.metric_type == "COSINE" else models.Distance.EUCLID
            ),
            hnsw_config=models.HnswConfigDiff(
                m=self.config.m,
                ef_construct=self.config.ef_construction
            )
        )
        
        logger.info(f"Created Qdrant collection: {collection_name}")
    
    async def insert_vectors(
        self,
        collection_name: str,
        vectors: List[np.ndarray],
        ids: List[str],
        metadata: List[Dict[str, Any]]
    ) -> None:
        """Insert vectors into Qdrant."""
        from qdrant_client.http import models
        
        # Prepare points
        points = [
            models.PointStruct(
                id=ids[i],
                vector=vectors[i].tolist(),
                payload=metadata[i]
            )
            for i in range(len(vectors))
        ]
        
        # Upsert points
        await asyncio.get_event_loop().run_in_executor(
            None,
            self.client.upsert,
            collection_name,
            points
        )
        
        logger.info(f"Inserted {len(vectors)} vectors into {collection_name}")
    
    async def search(
        self,
        collection_name: str,
        query_vector: np.ndarray,
        top_k: int = 10,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        """Search for similar vectors in Qdrant."""
        from qdrant_client.http import models
        
        # Build filter if provided
        query_filter = None
        if filter_dict:
            must_conditions = []
            for key, value in filter_dict.items():
                must_conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    )
                )
            
            query_filter = models.Filter(must=must_conditions)
        
        # Search
        results = await asyncio.get_event_loop().run_in_executor(
            None,
            self.client.search,
            collection_name,
            query_vector.tolist(),
            limit=top_k,
            query_filter=query_filter
        )
        
        # Convert to VectorSearchResult
        return [
            VectorSearchResult(
                id=str(result.id),
                score=result.score,
                metadata=result.payload or {}
            )
            for result in results
        ]
    
    async def delete_vectors(self, collection_name: str, ids: List[str]) -> None:
        """Delete vectors from Qdrant."""
        from qdrant_client.http import models
        
        await asyncio.get_event_loop().run_in_executor(
            None,
            self.client.delete,
            collection_name,
            points_selector=models.PointIdsList(points=ids)
        )
        
        logger.info(f"Deleted {len(ids)} vectors from {collection_name}")
    
    async def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get Qdrant collection statistics."""
        info = await asyncio.get_event_loop().run_in_executor(
            None,
            self.client.get_collection,
            collection_name
        )
        
        return {
            "name": collection_name,
            "num_vectors": info.vectors_count,
            "num_indexed": info.indexed_vectors_count,
            "status": info.status,
            "config": {
                "vector_size": info.config.params.vectors.size,
                "distance": info.config.params.vectors.distance,
                "hnsw_m": info.config.hnsw_config.m,
                "hnsw_ef_construct": info.config.hnsw_config.ef_construct
            }
        }


def create_vector_db(config: VectorDBConfig) -> VectorDB:
    """Factory function to create appropriate vector database."""
    if config.provider.lower() == "milvus":
        return MilvusDB(config)
    elif config.provider.lower() == "qdrant":
        return QdrantDB(config)
    else:
        raise ValueError(f"Unsupported vector database provider: {config.provider}")