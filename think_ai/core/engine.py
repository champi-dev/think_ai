"""Core Think AI engine that orchestrates all components."""

import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import uuid
import numpy as np

from ..storage.base import StorageBackend, CachedStorageBackend, StorageItem
from ..storage.scylla import ScyllaDBBackend
from ..storage.redis_cache import RedisCache
from ..storage.vector_db import VectorDB, create_vector_db, VectorSearchResult
from ..models.embeddings import EmbeddingModel, create_embedding_model
from ..core.config import Config
from ..utils.logging import get_logger


logger = get_logger(__name__)


@dataclass
class QueryResult:
    """Result of a knowledge query."""
    query: str
    results: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    timestamp: datetime
    processing_time_ms: float


class ThinkAIEngine:
    """Main engine orchestrating Think AI components."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.from_env()
        self.storage: Optional[StorageBackend] = None
        self.cache: Optional[RedisCache] = None
        self.vector_db: Optional[VectorDB] = None
        self.embedding_model: Optional[EmbeddingModel] = None
        self.offline_storage = None  # Will be implemented later
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize all components."""
        if self._initialized:
            return
        
        logger.info("Initializing Think AI Engine...")
        
        try:
            # Initialize ScyllaDB primary storage
            logger.info("Initializing ScyllaDB backend...")
            scylla_backend = ScyllaDBBackend(self.config.scylla)
            await scylla_backend.initialize()
            
            # Initialize Redis cache
            logger.info("Initializing Redis cache...")
            self.cache = RedisCache(self.config.redis)
            await self.cache.initialize()
            
            # Create cached storage backend
            self.storage = CachedStorageBackend(
                primary=scylla_backend,
                cache=self.cache
            )
            
            # Initialize vector database
            logger.info("Initializing vector database...")
            self.vector_db = create_vector_db(self.config.vector_db)
            await self.vector_db.initialize()
            await self.vector_db.create_collection(
                self.config.vector_db.collection_name,
                self.config.vector_db.dimension
            )
            
            # Initialize embedding model
            logger.info("Initializing embedding model...")
            self.embedding_model = create_embedding_model(
                model_type="transformer",
                use_cache=True
            )
            await self.embedding_model.initialize()
            
            # TODO: Initialize offline storage
            
            self._initialized = True
            logger.info("Think AI Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Think AI Engine: {e}")
            await self.shutdown()
            raise
    
    async def shutdown(self) -> None:
        """Shutdown all components gracefully."""
        logger.info("Shutting down Think AI Engine...")
        
        if self.storage:
            await self.storage.close()
        
        if self.vector_db:
            await self.vector_db.close()
        
        self._initialized = False
        logger.info("Think AI Engine shutdown complete")
    
    async def store_knowledge(
        self, 
        key: str, 
        content: Any, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Store knowledge in the system."""
        if not self._initialized:
            raise RuntimeError("Engine not initialized")
        
        # Create storage item
        item = StorageItem.create(content, metadata)
        
        # Store in primary storage (will also cache)
        await self.storage.put(key, item)
        
        # Generate and store vector embedding
        if self.embedding_model and self.vector_db:
            try:
                # Generate embedding
                embedding = await self.embedding_model.embed_text(str(content))
                
                # Store in vector database
                await self.vector_db.insert_vectors(
                    self.config.vector_db.collection_name,
                    [embedding],
                    [key],
                    [{"key": key, "type": "content", **(metadata or {})}]
                )
                
                logger.debug(f"Stored vector embedding for key: {key}")
            except Exception as e:
                logger.error(f"Failed to store vector embedding: {e}")
        
        # TODO: Update knowledge graph
        
        logger.info(f"Stored knowledge: {key}")
        return item.id
    
    async def retrieve_knowledge(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve knowledge by key."""
        if not self._initialized:
            raise RuntimeError("Engine not initialized")
        
        item = await self.storage.get(key)
        
        if item:
            return {
                "id": item.id,
                "key": key,
                "content": item.content,
                "metadata": item.metadata,
                "created_at": item.created_at.isoformat(),
                "updated_at": item.updated_at.isoformat(),
                "version": item.version
            }
        
        return None
    
    async def query_knowledge(
        self, 
        query: str,
        limit: int = 10,
        use_semantic_search: bool = True
    ) -> QueryResult:
        """Query knowledge using various methods."""
        if not self._initialized:
            raise RuntimeError("Engine not initialized")
        
        start_time = datetime.utcnow()
        results = []
        
        # Determine search method
        if use_semantic_search and self.embedding_model and self.vector_db:
            # Semantic search using vector similarity
            try:
                # Generate query embedding
                query_embedding = await self.embedding_model.embed_text(query)
                
                # Search in vector database
                vector_results = await self.vector_db.search(
                    self.config.vector_db.collection_name,
                    query_embedding,
                    top_k=limit
                )
                
                # Retrieve full items for each result
                for vr in vector_results:
                    item = await self.retrieve_knowledge(vr.id)
                    if item:
                        item['similarity_score'] = float(vr.score)
                        results.append(item)
                
                logger.info(f"Semantic search found {len(results)} results")
                
            except Exception as e:
                logger.error(f"Semantic search failed: {e}")
                # Fall back to prefix search
                use_semantic_search = False
        
        # Prefix search as fallback or explicit choice
        if not use_semantic_search or not results:
            if query.startswith("prefix:"):
                prefix = query.replace("prefix:", "").strip()
                keys = await self.storage.list_keys(prefix=prefix, limit=limit)
                
                for key in keys:
                    item = await self.retrieve_knowledge(key)
                    if item:
                        results.append(item)
        
        # TODO: Implement knowledge graph queries
        # TODO: Implement hybrid search combining multiple methods
        
        # Calculate processing time
        end_time = datetime.utcnow()
        processing_time_ms = (end_time - start_time).total_seconds() * 1000
        
        return QueryResult(
            query=query,
            results=results,
            metadata={
                "method": "semantic_search" if use_semantic_search and results else "prefix_search" if query.startswith("prefix:") else "exact_match",
                "limit": limit,
                "use_semantic_search": use_semantic_search
            },
            timestamp=end_time,
            processing_time_ms=processing_time_ms
        )
    
    async def batch_store_knowledge(
        self, 
        items: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Store multiple knowledge items efficiently."""
        if not self._initialized:
            raise RuntimeError("Engine not initialized")
        
        # Create storage items
        storage_items = {}
        ids = []
        
        for key, content in items.items():
            item = StorageItem.create(content, metadata)
            storage_items[key] = item
            ids.append(item.id)
        
        # Batch store
        await self.storage.batch_put(storage_items)
        
        # Generate and store vector embeddings
        if self.embedding_model and self.vector_db:
            try:
                # Generate embeddings for all content
                texts = [str(content) for content in items.values()]
                embeddings = await self.embedding_model.embed_texts(texts)
                
                # Prepare metadata
                metadatas = [
                    {"key": key, "type": "content", **(metadata or {})}
                    for key in items.keys()
                ]
                
                # Store in vector database
                await self.vector_db.insert_vectors(
                    self.config.vector_db.collection_name,
                    embeddings,
                    list(items.keys()),
                    metadatas
                )
                
                logger.debug(f"Stored {len(embeddings)} vector embeddings")
            except Exception as e:
                logger.error(f"Failed to store vector embeddings: {e}")
        
        logger.info(f"Batch stored {len(items)} knowledge items")
        return ids
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        if not self._initialized:
            return {"status": "not_initialized"}
        
        storage_stats = await self.storage.get_stats()
        
        stats = {
            "status": "operational",
            "engine_version": self.config.version,
            "storage": storage_stats,
            "config": self.config.to_dict()
        }
        
        # Add vector database stats
        if self.vector_db:
            try:
                vector_stats = await self.vector_db.get_collection_stats(
                    self.config.vector_db.collection_name
                )
                stats["vector_db"] = vector_stats
            except Exception as e:
                logger.error(f"Failed to get vector DB stats: {e}")
                stats["vector_db"] = {"error": str(e)}
        
        # Add embedding model info
        if self.embedding_model:
            stats["embedding_model"] = {
                "dimension": self.embedding_model.get_dimension(),
                "initialized": True
            }
        
        return stats
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all components."""
        health = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {}
        }
        
        # Check storage
        try:
            test_key = f"health_check_{uuid.uuid4()}"
            test_item = StorageItem.create({"test": "data"})
            await self.storage.put(test_key, test_item)
            retrieved = await self.storage.get(test_key)
            await self.storage.delete(test_key)
            
            health["components"]["storage"] = {
                "status": "healthy" if retrieved else "unhealthy",
                "type": "scylla_with_redis_cache"
            }
        except Exception as e:
            health["components"]["storage"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health["status"] = "unhealthy"
        
        # Check vector DB health
        if self.vector_db:
            try:
                # Try to get collection stats as health check
                stats = await self.vector_db.get_collection_stats(
                    self.config.vector_db.collection_name
                )
                health["components"]["vector_db"] = {
                    "status": "healthy",
                    "provider": self.config.vector_db.provider,
                    "vectors": stats.get("num_vectors", stats.get("num_entities", 0))
                }
            except Exception as e:
                health["components"]["vector_db"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                health["status"] = "unhealthy"
        
        # Check embedding model health
        if self.embedding_model:
            try:
                # Try to generate a test embedding
                test_embedding = await self.embedding_model.embed_text("health check")
                health["components"]["embedding_model"] = {
                    "status": "healthy" if test_embedding is not None else "unhealthy",
                    "dimension": self.embedding_model.get_dimension()
                }
            except Exception as e:
                health["components"]["embedding_model"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                health["status"] = "unhealthy"
        
        # TODO: Check offline storage health
        
        return health
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.shutdown()