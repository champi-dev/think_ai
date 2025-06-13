"""Redis caching layer implementation."""

import asyncio
import json
import pickle
from typing import Any, Dict, List, Optional, AsyncIterator
from datetime import datetime, timedelta
import redis.asyncio as redis
from redis.asyncio.cluster import RedisCluster

from ..core.config import RedisConfig
from ..utils.logging import get_logger
from .base import StorageBackend, StorageItem


logger = get_logger(__name__)


class RedisCache(StorageBackend):
    """Redis caching backend for high-performance O(1) operations."""
    
    def __init__(self, config: RedisConfig, ttl_seconds: int = 3600):
        self.config = config
        self.ttl_seconds = ttl_seconds
        self.client: Optional[redis.Redis] = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize Redis connection."""
        if self._initialized:
            return
        
        try:
            if self.config.cluster_mode:
                # Connect to Redis cluster
                self.client = RedisCluster(
                    host=self.config.host,
                    port=self.config.port,
                    password=self.config.password,
                    decode_responses=False,  # We'll handle encoding/decoding
                    max_connections=self.config.max_connections
                )
            else:
                # Connect to single Redis instance
                self.client = redis.Redis(
                    host=self.config.host,
                    port=self.config.port,
                    db=self.config.db,
                    password=self.config.password,
                    decode_responses=False,
                    max_connections=self.config.max_connections
                )
            
            # Test connection
            await self.client.ping()
            
            self._initialized = True
            logger.info("Redis cache initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            raise
    
    async def close(self) -> None:
        """Close Redis connection."""
        if self.client:
            await self.client.close()
            self._initialized = False
    
    async def put(self, key: str, item: StorageItem) -> None:
        """Store an item in cache with TTL."""
        # Serialize the item
        value = self._serialize_item(item)
        
        # Store with TTL
        await self.client.setex(
            self._make_key(key),
            self.ttl_seconds,
            value
        )
        
        # Update index for prefix queries
        await self._add_to_index(key)
    
    async def get(self, key: str) -> Optional[StorageItem]:
        """Retrieve an item from cache."""
        value = await self.client.get(self._make_key(key))
        
        if value is None:
            return None
        
        return self._deserialize_item(value)
    
    async def delete(self, key: str) -> bool:
        """Delete an item from cache."""
        result = await self.client.delete(self._make_key(key))
        
        if result > 0:
            await self._remove_from_index(key)
            return True
        
        return False
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists in cache."""
        return await self.client.exists(self._make_key(key)) > 0
    
    async def list_keys(self, prefix: Optional[str] = None, limit: int = 100) -> List[str]:
        """List keys with optional prefix filter."""
        if prefix:
            # Use sorted set for prefix queries
            index_key = f"idx:prefix:{prefix[:3]}"
            keys = await self.client.zrange(index_key, 0, limit - 1)
            
            # Filter by full prefix and decode
            result = []
            for key_bytes in keys:
                key = key_bytes.decode('utf-8')
                if key.startswith(prefix):
                    result.append(key)
            
            return result
        else:
            # Scan all keys (use with caution)
            cursor = b'0'
            keys = []
            
            while cursor and len(keys) < limit:
                cursor, batch = await self.client.scan(
                    cursor,
                    match=f"{self.config.db}:*",
                    count=min(100, limit - len(keys))
                )
                
                for key_bytes in batch:
                    key = key_bytes.decode('utf-8')
                    # Remove namespace prefix
                    clean_key = key.replace(f"{self.config.db}:", "", 1)
                    keys.append(clean_key)
                    
                    if len(keys) >= limit:
                        break
            
            return keys[:limit]
    
    async def batch_get(self, keys: List[str]) -> Dict[str, Optional[StorageItem]]:
        """Retrieve multiple items efficiently using pipeline."""
        if not keys:
            return {}
        
        # Use pipeline for batch operations
        async with self.client.pipeline() as pipe:
            for key in keys:
                pipe.get(self._make_key(key))
            
            values = await pipe.execute()
        
        # Build results
        results = {}
        for key, value in zip(keys, values):
            if value is not None:
                results[key] = self._deserialize_item(value)
            else:
                results[key] = None
        
        return results
    
    async def batch_put(self, items: Dict[str, StorageItem]) -> None:
        """Store multiple items efficiently using pipeline."""
        if not items:
            return
        
        # Use pipeline for batch operations
        async with self.client.pipeline() as pipe:
            for key, item in items.items():
                value = self._serialize_item(item)
                pipe.setex(self._make_key(key), self.ttl_seconds, value)
            
            await pipe.execute()
        
        # Update indexes
        for key in items.keys():
            await self._add_to_index(key)
    
    async def scan(
        self, 
        prefix: Optional[str] = None,
        start_key: Optional[str] = None,
        limit: int = 100
    ) -> AsyncIterator[tuple[str, StorageItem]]:
        """Scan through cache items."""
        if prefix:
            # Use index for prefix scan
            index_key = f"idx:prefix:{prefix[:3]}"
            
            # Determine start position
            start_rank = 0
            if start_key:
                rank = await self.client.zrank(index_key, start_key.encode('utf-8'))
                if rank is not None:
                    start_rank = rank
            
            # Get keys from sorted set
            keys = await self.client.zrange(index_key, start_rank, start_rank + limit - 1)
            
            for key_bytes in keys:
                key = key_bytes.decode('utf-8')
                if key.startswith(prefix):
                    item = await self.get(key)
                    if item:
                        yield key, item
        else:
            # Full scan
            cursor = b'0'
            count = 0
            
            while cursor and count < limit:
                cursor, batch = await self.client.scan(
                    cursor,
                    match=f"{self.config.db}:*",
                    count=min(100, limit - count)
                )
                
                for key_bytes in batch:
                    if count >= limit:
                        break
                    
                    key = key_bytes.decode('utf-8')
                    clean_key = key.replace(f"{self.config.db}:", "", 1)
                    
                    if start_key and clean_key < start_key:
                        continue
                    
                    item = await self.get(clean_key)
                    if item:
                        yield clean_key, item
                        count += 1
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        info = await self.client.info()
        
        # Extract relevant stats
        memory_info = info.get('memory', {})
        stats_info = info.get('stats', {})
        
        return {
            "backend": "redis",
            "used_memory_human": memory_info.get('used_memory_human', 'N/A'),
            "used_memory_bytes": memory_info.get('used_memory', 0),
            "connected_clients": info.get('connected_clients', 0),
            "total_connections_received": stats_info.get('total_connections_received', 0),
            "total_commands_processed": stats_info.get('total_commands_processed', 0),
            "instantaneous_ops_per_sec": stats_info.get('instantaneous_ops_per_sec', 0),
            "keyspace_hits": stats_info.get('keyspace_hits', 0),
            "keyspace_misses": stats_info.get('keyspace_misses', 0),
            "hit_rate": self._calculate_hit_rate(
                stats_info.get('keyspace_hits', 0),
                stats_info.get('keyspace_misses', 0)
            ),
            "evicted_keys": stats_info.get('evicted_keys', 0),
            "expired_keys": stats_info.get('expired_keys', 0),
            "config": {
                "host": self.config.host,
                "port": self.config.port,
                "db": self.config.db,
                "cluster_mode": self.config.cluster_mode,
                "ttl_seconds": self.ttl_seconds
            }
        }
    
    def _make_key(self, key: str) -> str:
        """Create namespaced key."""
        return f"{self.config.db}:{key}"
    
    def _serialize_item(self, item: StorageItem) -> bytes:
        """Serialize StorageItem to bytes."""
        # Convert to dict for serialization
        data = {
            'id': item.id,
            'content': item.content,
            'metadata': item.metadata,
            'created_at': item.created_at.isoformat(),
            'updated_at': item.updated_at.isoformat(),
            'version': item.version
        }
        
        # Use pickle for complex objects, with json as metadata
        return pickle.dumps(data)
    
    def _deserialize_item(self, data: bytes) -> StorageItem:
        """Deserialize bytes to StorageItem."""
        # Unpickle the data
        item_dict = pickle.loads(data)
        
        # Reconstruct StorageItem
        return StorageItem(
            id=item_dict['id'],
            content=item_dict['content'],
            metadata=item_dict['metadata'],
            created_at=datetime.fromisoformat(item_dict['created_at']),
            updated_at=datetime.fromisoformat(item_dict['updated_at']),
            version=item_dict['version']
        )
    
    async def _add_to_index(self, key: str) -> None:
        """Add key to prefix index."""
        prefix = key[:3] if len(key) >= 3 else key
        index_key = f"idx:prefix:{prefix}"
        
        # Add to sorted set with timestamp as score
        timestamp = datetime.utcnow().timestamp()
        await self.client.zadd(index_key, {key.encode('utf-8'): timestamp})
        
        # Set TTL on index
        await self.client.expire(index_key, self.ttl_seconds * 2)
    
    async def _remove_from_index(self, key: str) -> None:
        """Remove key from prefix index."""
        prefix = key[:3] if len(key) >= 3 else key
        index_key = f"idx:prefix:{prefix}"
        
        await self.client.zrem(index_key, key.encode('utf-8'))
    
    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """Calculate cache hit rate."""
        total = hits + misses
        if total == 0:
            return 0.0
        return (hits / total) * 100


class MultiLevelCache(StorageBackend):
    """Multi-level cache implementation for optimal performance."""
    
    def __init__(self, l1_cache: RedisCache, l2_cache: StorageBackend):
        self.l1_cache = l1_cache  # Fast Redis cache
        self.l2_cache = l2_cache  # Slower but larger cache (could be another Redis with longer TTL)
        
    async def initialize(self) -> None:
        """Initialize both cache levels."""
        await self.l1_cache.initialize()
        await self.l2_cache.initialize()
    
    async def get(self, key: str) -> Optional[StorageItem]:
        """Get with cache hierarchy."""
        # Try L1 first
        item = await self.l1_cache.get(key)
        if item:
            return item
        
        # Try L2
        item = await self.l2_cache.get(key)
        if item:
            # Promote to L1
            await self.l1_cache.put(key, item)
        
        return item
    
    async def put(self, key: str, item: StorageItem) -> None:
        """Put in both cache levels."""
        await self.l1_cache.put(key, item)
        await self.l2_cache.put(key, item)
    
    # Implement other methods similarly...