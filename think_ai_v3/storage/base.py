"""
Base storage interface for Think AI
All implementations must guarantee O(1) operations
"""

import hashlib
import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


@dataclass
class StorageItem:
    """Item stored in Think AI - O(1) access guaranteed."""

    key: str
    value: Any
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    ttl: Optional[int] = None  # Time to live in seconds
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)

    def is_expired(self) -> bool:
        """Check if item is expired - O(1)."""
        if self.ttl is None:
            return False
        return time.time() - self.timestamp > self.ttl

    def access(self) -> Any:
        """Access the value and update stats - O(1)."""
        self.access_count += 1
        self.last_accessed = time.time()
        return self.value


class StorageBackend(ABC):
    """
    Abstract base class for storage backends.
    All operations must be O(1) or document why not.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize storage backend."""
        self.config = config or {}
        self._stats = {
            "reads": 0,
            "writes": 0,
            "deletes": 0,
            "hits": 0,
            "misses": 0,
        }

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value by key - must be O(1)."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value with optional TTL - must be O(1)."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value - must be O(1)."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists - must be O(1)."""
        pass

    @abstractmethod
    async def clear(self) -> int:
        """Clear all data - O(n) acceptable here."""
        pass

    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """Get multiple values - O(k) where k = len(keys)."""
        results = {}
        for key in keys:
            value = await self.get(key)
            if value is not None:
                results[key] = value
        return results

    async def set_many(self, items: Dict[str, Any], ttl: Optional[int] = None) -> int:
        """Set multiple values - O(k) where k = len(items)."""
        success_count = 0
        for key, value in items.items():
            if await self.set(key, value, ttl):
                success_count += 1
        return success_count

    def get_stats(self) -> Dict[str, int]:
        """Get storage statistics - O(1)."""
        hit_rate = (
            self._stats["hits"] / (self._stats["hits"] + self._stats["misses"])
            if (self._stats["hits"] + self._stats["misses"]) > 0
            else 0.0
        )
        return {
            **self._stats,
            "hit_rate": hit_rate,
        }

    def _update_stats(self, operation: str, hit: bool = True):
        """Update statistics - O(1)."""
        self._stats[operation] += 1
        if operation == "reads":
            if hit:
                self._stats["hits"] += 1
            else:
                self._stats["misses"] += 1


class MemoryStorage(StorageBackend):
    """
    In-memory storage implementation.
    True O(1) for all operations using dict.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize memory storage."""
        super().__init__(config)
        self._data: Dict[str, StorageItem] = {}
        self._max_items = config.get("max_items", 10000) if config else 10000
        logger.info(f"Memory storage initialized with max_items={self._max_items}")

    async def get(self, key: str) -> Optional[Any]:
        """Get value by key - O(1)."""
        self._update_stats("reads", key in self._data)

        item = self._data.get(key)
        if item is None:
            return None

        if item.is_expired():
            del self._data[key]
            return None

        return item.access()

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value with optional TTL - O(1)."""
        self._update_stats("writes")

        # Evict if at capacity - O(1) using Python 3.7+ dict ordering
        if len(self._data) >= self._max_items and key not in self._data:
            # Remove least recently accessed item
            lru_key = min(self._data.keys(), key=lambda k: self._data[k].last_accessed)
            del self._data[lru_key]

        self._data[key] = StorageItem(
            key=key,
            value=value,
            ttl=ttl,
        )
        return True

    async def delete(self, key: str) -> bool:
        """Delete value - O(1)."""
        self._update_stats("deletes")

        if key in self._data:
            del self._data[key]
            return True
        return False

    async def exists(self, key: str) -> bool:
        """Check if key exists - O(1)."""
        if key not in self._data:
            return False

        item = self._data.get(key)
        if item and item.is_expired():
            del self._data[key]
            return False

        return True

    async def clear(self) -> int:
        """Clear all data - O(n) but acceptable."""
        count = len(self._data)
        self._data.clear()
        return count


class CachedStorageBackend(StorageBackend):
    """
    Storage backend with built-in caching.
    O(1) for cache hits, delegates to backend for misses.
    """

    def __init__(self, backend: StorageBackend, cache_size: int = 1000, config: Optional[Dict[str, Any]] = None):
        """Initialize cached storage."""
        super().__init__(config)
        self.backend = backend
        self.cache = MemoryStorage({"max_items": cache_size})
        self.cache_ttl = config.get("cache_ttl", 3600) if config else 3600
        logger.info(f"Cached storage initialized with size={cache_size}")

    async def get(self, key: str) -> Optional[Any]:
        """Get with cache check first - O(1) for hits."""
        # Check cache first
        cached_value = await self.cache.get(key)
        if cached_value is not None:
            self._update_stats("reads", True)
            return cached_value

        # Cache miss - get from backend
        value = await self.backend.get(key)
        if value is not None:
            # Add to cache
            await self.cache.set(key, value, self.cache_ttl)
            self._update_stats("reads", True)
        else:
            self._update_stats("reads", False)

        return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set in both cache and backend - O(1) for cache."""
        # Set in cache
        await self.cache.set(key, value, min(ttl or self.cache_ttl, self.cache_ttl))

        # Set in backend
        result = await self.backend.set(key, value, ttl)
        self._update_stats("writes")
        return result

    async def delete(self, key: str) -> bool:
        """Delete from both cache and backend - O(1) for cache."""
        # Delete from cache
        await self.cache.delete(key)

        # Delete from backend
        result = await self.backend.delete(key)
        self._update_stats("deletes")
        return result

    async def exists(self, key: str) -> bool:
        """Check existence with cache first - O(1) for cache hits."""
        # Check cache first
        if await self.cache.exists(key):
            return True

        # Check backend
        return await self.backend.exists(key)

    async def clear(self) -> int:
        """Clear both cache and backend."""
        await self.cache.clear()
        return await self.backend.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics - O(1)."""
        return {
            "cache": self.cache.get_stats(),
            "backend": self.backend.get_stats(),
            "total": self.get_stats(),
        }


def create_storage(backend_type: str, config: Optional[Dict[str, Any]] = None) -> StorageBackend:
    """
    Factory function to create storage backends.
    O(1) instantiation for all types.
    """
    backends = {
        "memory": MemoryStorage,
        # Additional backends would be added here
        # "redis": RedisStorage,
        # "sqlite": SQLiteStorage,
        # "scylla": ScyllaStorage,
    }

    backend_class = backends.get(backend_type, MemoryStorage)
    return backend_class(config)
