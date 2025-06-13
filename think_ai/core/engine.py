"""Core Think AI engine that orchestrates all components."""

import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import uuid

from ..storage.base import StorageBackend, CachedStorageBackend, StorageItem
from ..storage.scylla import ScyllaDBBackend
from ..storage.redis_cache import RedisCache
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
        self.vector_db = None  # Will be implemented later
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
            
            # TODO: Initialize vector database
            # TODO: Initialize offline storage
            # TODO: Initialize AI models
            
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
        
        # TODO: Update vector embeddings
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
        
        # TODO: Implement semantic search using vector DB
        # TODO: Implement knowledge graph queries
        # TODO: Implement hybrid search
        
        # For now, simple prefix search
        if query.startswith("prefix:"):
            prefix = query.replace("prefix:", "").strip()
            keys = await self.storage.list_keys(prefix=prefix, limit=limit)
            
            for key in keys:
                item = await self.retrieve_knowledge(key)
                if item:
                    results.append(item)
        
        # Calculate processing time
        end_time = datetime.utcnow()
        processing_time_ms = (end_time - start_time).total_seconds() * 1000
        
        return QueryResult(
            query=query,
            results=results,
            metadata={
                "method": "prefix_search" if query.startswith("prefix:") else "exact_match",
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
        
        logger.info(f"Batch stored {len(items)} knowledge items")
        return ids
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        if not self._initialized:
            return {"status": "not_initialized"}
        
        storage_stats = await self.storage.get_stats()
        
        return {
            "status": "operational",
            "engine_version": self.config.version,
            "storage": storage_stats,
            "config": self.config.to_dict()
        }
    
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
        
        # TODO: Check vector DB health
        # TODO: Check offline storage health
        # TODO: Check model health
        
        return health
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.shutdown()