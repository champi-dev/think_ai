"""Mock ScyllaDB storage backend for compatibility."""

import asyncio
from typing import Any, Dict, List, Optional, AsyncIterator, Tuple
from datetime import datetime
import json
import uuid

from ..core.config import ScyllaDBConfig
from ..utils.logging import get_logger
from .base import StorageBackend, StorageItem


logger = get_logger(__name__)


class ScyllaDBBackend(StorageBackend):
    """Mock ScyllaDB storage backend for testing."""
    
    def __init__(self, config: ScyllaDBConfig):
        self.config = config
        self._storage = {}  # In-memory storage
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize mock storage."""
        if self._initialized:
            return
        
        logger.info("Initializing mock ScyllaDB backend")
        self._initialized = True
    
    async def store(self, item: StorageItem) -> str:
        """Store an item."""
        item_id = str(uuid.uuid4())
        self._storage[item_id] = {
            'id': item_id,
            'content': item.content,
            'metadata': item.metadata,
            'embedding': item.embedding,
            'timestamp': datetime.utcnow().isoformat()
        }
        return item_id
    
    async def retrieve(self, item_id: str) -> Optional[StorageItem]:
        """Retrieve an item by ID."""
        if item_id in self._storage:
            data = self._storage[item_id]
            return StorageItem(
                id=data['id'],
                content=data['content'],
                metadata=data.get('metadata', {}),
                embedding=data.get('embedding')
            )
        return None
    
    async def search(
        self,
        query: Optional[str] = None,
        metadata_filter: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> List[StorageItem]:
        """Search for items."""
        results = []
        for data in self._storage.values():
            if query and query.lower() not in data['content'].lower():
                continue
            if metadata_filter:
                match = all(
                    data.get('metadata', {}).get(k) == v
                    for k, v in metadata_filter.items()
                )
                if not match:
                    continue
            results.append(StorageItem(
                id=data['id'],
                content=data['content'],
                metadata=data.get('metadata', {}),
                embedding=data.get('embedding')
            ))
            if len(results) >= limit:
                break
        return results
    
    async def update(self, item_id: str, item: StorageItem) -> bool:
        """Update an item."""
        if item_id in self._storage:
            self._storage[item_id].update({
                'content': item.content,
                'metadata': item.metadata,
                'embedding': item.embedding,
                'timestamp': datetime.utcnow().isoformat()
            })
            return True
        return False
    
    async def delete(self, item_id: str) -> bool:
        """Delete an item."""
        if item_id in self._storage:
            del self._storage[item_id]
            return True
        return False
    
    async def batch_store(self, items: List[StorageItem]) -> List[str]:
        """Store multiple items."""
        ids = []
        for item in items:
            item_id = await self.store(item)
            ids.append(item_id)
        return ids
    
    async def close(self) -> None:
        """Close the mock backend."""
        self._initialized = False
        logger.info("Mock ScyllaDB backend closed")
    
    async def put(self, key: str, value: Any) -> None:
        """Put a key-value pair."""
        self._storage[key] = value
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value by key."""
        return self._storage.get(key)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return key in self._storage
    
    async def batch_put(self, items: Dict[str, Any]) -> None:
        """Put multiple key-value pairs."""
        self._storage.update(items)
    
    async def batch_get(self, keys: List[str]) -> Dict[str, Any]:
        """Get multiple values by keys."""
        return {k: self._storage.get(k) for k in keys if k in self._storage}
    
    async def list_keys(self, prefix: Optional[str] = None) -> List[str]:
        """List all keys with optional prefix."""
        if prefix:
            return [k for k in self._storage.keys() if k.startswith(prefix)]
        return list(self._storage.keys())
    
    async def scan(self, start_key: Optional[str] = None, limit: int = 100) -> AsyncIterator[Tuple[str, Any]]:
        """Scan through key-value pairs."""
        keys = sorted(self._storage.keys())
        if start_key:
            keys = [k for k in keys if k >= start_key]
        
        for i, key in enumerate(keys[:limit]):
            yield key, self._storage[key]
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        return {
            "total_items": len(self._storage),
            "backend": "mock_scylla",
            "initialized": self._initialized
        }