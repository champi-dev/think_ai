"""Base storage interface for Think AI system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, AsyncIterator
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class StorageItem:
    """Base storage item with metadata."""
    id: str
    content: Any
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    version: int = 1
    
    @classmethod
    def create(cls, content: Any, metadata: Optional[Dict[str, Any]] = None) -> "StorageItem":
        """Create a new storage item."""
        now = datetime.utcnow()
        return cls(
            id=str(uuid.uuid4()),
            content=content,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
            version=1
        )


class StorageBackend(ABC):
    """Abstract base class for storage backends."""
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the storage backend."""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close the storage backend connection."""
        pass
    
    @abstractmethod
    async def put(self, key: str, item: StorageItem) -> None:
        """Store an item."""
        pass
    
    @abstractmethod
    async def get(self, key: str) -> Optional[StorageItem]:
        """Retrieve an item by key."""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete an item by key."""
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a key exists."""
        pass
    
    @abstractmethod
    async def list_keys(self, prefix: Optional[str] = None, limit: int = 100) -> List[str]:
        """List keys with optional prefix filter."""
        pass
    
    @abstractmethod
    async def batch_get(self, keys: List[str]) -> Dict[str, Optional[StorageItem]]:
        """Retrieve multiple items by keys."""
        pass
    
    @abstractmethod
    async def batch_put(self, items: Dict[str, StorageItem]) -> None:
        """Store multiple items."""
        pass
    
    @abstractmethod
    async def scan(
        self, 
        prefix: Optional[str] = None,
        start_key: Optional[str] = None,
        limit: int = 100
    ) -> AsyncIterator[tuple[str, StorageItem]]:
        """Scan through items with optional filters."""
        pass
    
    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        pass


class CachedStorageBackend(StorageBackend):
    """Storage backend with caching layer."""
    
    def __init__(self, primary: StorageBackend, cache: StorageBackend):
        self.primary = primary
        self.cache = cache
    
    async def initialize(self) -> None:
        """Initialize both storage backends."""
        await self.primary.initialize()
        await self.cache.initialize()
    
    async def close(self) -> None:
        """Close both storage backends."""
        await self.primary.close()
        await self.cache.close()
    
    async def get(self, key: str) -> Optional[StorageItem]:
        """Get item from cache first, then primary."""
        # Try cache first
        item = await self.cache.get(key)
        if item:
            return item
        
        # Fallback to primary
        item = await self.primary.get(key)
        if item:
            # Update cache
            await self.cache.put(key, item)
        
        return item
    
    async def put(self, key: str, item: StorageItem) -> None:
        """Put item in both primary and cache."""
        await self.primary.put(key, item)
        await self.cache.put(key, item)
    
    async def delete(self, key: str) -> bool:
        """Delete from both primary and cache."""
        cache_result = await self.cache.delete(key)
        primary_result = await self.primary.delete(key)
        return primary_result or cache_result
    
    async def exists(self, key: str) -> bool:
        """Check existence in cache first, then primary."""
        if await self.cache.exists(key):
            return True
        return await self.primary.exists(key)
    
    async def list_keys(self, prefix: Optional[str] = None, limit: int = 100) -> List[str]:
        """List keys from primary storage."""
        return await self.primary.list_keys(prefix, limit)
    
    async def batch_get(self, keys: List[str]) -> Dict[str, Optional[StorageItem]]:
        """Batch get with cache optimization."""
        results = {}
        cache_misses = []
        
        # Check cache first
        cache_results = await self.cache.batch_get(keys)
        for key, item in cache_results.items():
            if item:
                results[key] = item
            else:
                cache_misses.append(key)
        
        # Get missing items from primary
        if cache_misses:
            primary_results = await self.primary.batch_get(cache_misses)
            for key, item in primary_results.items():
                if item:
                    results[key] = item
                    # Update cache
                    await self.cache.put(key, item)
        
        return results
    
    async def batch_put(self, items: Dict[str, StorageItem]) -> None:
        """Batch put to both storages."""
        await self.primary.batch_put(items)
        await self.cache.batch_put(items)
    
    async def scan(
        self, 
        prefix: Optional[str] = None,
        start_key: Optional[str] = None,
        limit: int = 100
    ) -> AsyncIterator[tuple[str, StorageItem]]:
        """Scan from primary storage."""
        async for key, item in self.primary.scan(prefix, start_key, limit):
            yield key, item
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get combined statistics."""
        primary_stats = await self.primary.get_stats()
        cache_stats = await self.cache.get_stats()
        return {
            "primary": primary_stats,
            "cache": cache_stats
        }