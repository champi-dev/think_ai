"""Storage backend with learned index integration for O(1) access."""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json

from .scylla import ScyllaDBBackend
from .redis_cache import RedisCache
from .learned_index import LearnedIndexManager, LearnedIndex
from ..utils.logging import get_logger


logger = get_logger(__name__)


class IndexedStorageBackend:
    """Storage backend that uses learned indexes for O(1) key access."""
    
    def __init__(
        self,
        scylla_backend: ScyllaDBBackend,
        redis_cache: Optional[RedisCache] = None,
        index_manager: Optional[LearnedIndexManager] = None
    ):
        self.scylla = scylla_backend
        self.redis = redis_cache
        self.index_manager = index_manager or LearnedIndexManager()
        
        # Index configuration
        self.index_prefix_length = 3  # Use first 3 chars for index selection
        self.rebuild_threshold = 10000  # Rebuild index after this many changes
        self.changes_since_rebuild: Dict[str, int] = {}
        
        # Performance metrics
        self.metrics = {
            "index_hits": 0,
            "index_misses": 0,
            "fallback_scans": 0,
            "average_scan_size": 0
        }
    
    async def initialize(self) -> None:
        """Initialize storage and load indexes."""
        # Initialize backends
        await self.scylla.connect()
        if self.redis:
            await self.redis.connect()
        
        # Load or build indexes
        await self._initialize_indexes()
    
    async def put(
        self,
        key: str,
        value: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store with index update."""
        try:
            # Store in ScyllaDB
            success = await self.scylla.put(key, value, metadata)
            
            if success:
                # Update cache
                if self.redis:
                    await self.redis.set(key, value, metadata=metadata)
                
                # Track changes for index rebuild
                index_name = self._get_index_name(key)
                self.changes_since_rebuild[index_name] = \
                    self.changes_since_rebuild.get(index_name, 0) + 1
                
                # Check if rebuild needed
                if self.changes_since_rebuild[index_name] >= self.rebuild_threshold:
                    asyncio.create_task(self._rebuild_index(index_name))
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to store {key}: {e}")
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """Retrieve using learned index for O(1) access."""
        try:
            # Check cache first
            if self.redis:
                cached = await self.redis.get(key)
                if cached is not None:
                    self.metrics["index_hits"] += 1
                    return cached
            
            # Use learned index to find position
            index_name = self._get_index_name(key)
            index = self.index_manager.get_index(index_name)
            
            if index and index.trained:
                # Get predicted position range
                start, end = index.predict(key)
                scan_size = end - start
                
                # Update metrics
                self.metrics["average_scan_size"] = (
                    0.9 * self.metrics["average_scan_size"] + 0.1 * scan_size
                )
                
                # Scan only the predicted range
                result = await self._scan_range(key, start, end)
                
                if result is not None:
                    self.metrics["index_hits"] += 1
                    
                    # Update cache
                    if self.redis:
                        await self.redis.set(key, result)
                    
                    return result
                else:
                    self.metrics["index_misses"] += 1
            
            # Fallback to direct lookup
            self.metrics["fallback_scans"] += 1
            result = await self.scylla.get(key)
            
            if result is not None and self.redis:
                await self.redis.set(key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to retrieve {key}: {e}")
            return None
    
    async def batch_get(self, keys: List[str]) -> Dict[str, Any]:
        """Batch retrieve using learned indexes."""
        results = {}
        
        # Group keys by index
        key_groups: Dict[str, List[str]] = {}
        for key in keys:
            index_name = self._get_index_name(key)
            if index_name not in key_groups:
                key_groups[index_name] = []
            key_groups[index_name].append(key)
        
        # Process each group
        tasks = []
        for index_name, group_keys in key_groups.items():
            index = self.index_manager.get_index(index_name)
            
            if index and index.trained:
                # Use index for efficient retrieval
                task = self._batch_get_with_index(group_keys, index)
            else:
                # Fallback to regular batch get
                task = self._batch_get_fallback(group_keys)
            
            tasks.append(task)
        
        # Gather results
        group_results = await asyncio.gather(*tasks)
        for group_result in group_results:
            results.update(group_result)
        
        return results
    
    async def delete(self, key: str) -> bool:
        """Delete with index update tracking."""
        success = await self.scylla.delete(key)
        
        if success:
            # Remove from cache
            if self.redis:
                await self.redis.delete(key)
            
            # Track change
            index_name = self._get_index_name(key)
            self.changes_since_rebuild[index_name] = \
                self.changes_since_rebuild.get(index_name, 0) + 1
        
        return success
    
    async def search_prefix(
        self,
        prefix: str,
        limit: int = 100
    ) -> List[Tuple[str, Any]]:
        """Search by prefix using index."""
        # Use index for the prefix
        index_name = self._get_index_name(prefix)
        index = self.index_manager.get_index(index_name)
        
        if index and index.trained:
            # Get range for prefix
            start_key = prefix
            end_key = prefix + "~"  # ~ is after most chars
            
            start_pos, _ = index.predict(start_key)
            _, end_pos = index.predict(end_key)
            
            # Scan the range
            results = []
            scan_limit = min(end_pos - start_pos, limit * 2)  # Some buffer
            
            candidates = await self._scan_range_full(start_pos, end_pos, scan_limit)
            
            for key, value in candidates:
                if key.startswith(prefix):
                    results.append((key, value))
                    if len(results) >= limit:
                        break
            
            return results
        
        # Fallback to ScyllaDB prefix search
        return await self.scylla.scan(prefix=prefix, limit=limit)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        total_accesses = (
            self.metrics["index_hits"] +
            self.metrics["index_misses"] +
            self.metrics["fallback_scans"]
        )
        
        hit_rate = (
            self.metrics["index_hits"] / total_accesses
            if total_accesses > 0 else 0
        )
        
        return {
            "total_accesses": total_accesses,
            "index_hit_rate": hit_rate,
            "average_scan_size": self.metrics["average_scan_size"],
            "fallback_rate": (
                self.metrics["fallback_scans"] / total_accesses
                if total_accesses > 0 else 0
            ),
            "indexes_loaded": len(self.index_manager.list_indexes())
        }
    
    async def _initialize_indexes(self) -> None:
        """Initialize learned indexes from existing data."""
        # Get sample of keys for each prefix
        prefixes = await self._get_key_prefixes()
        
        for prefix in prefixes[:10]:  # Limit initial indexes
            index_name = f"prefix_{prefix}"
            
            # Check if index exists
            if self.index_manager.get_index(index_name):
                continue
            
            # Get keys for this prefix
            keys_data = await self.scylla.scan(prefix=prefix, limit=10000)
            
            if len(keys_data) >= 100:  # Minimum keys for index
                keys = [k for k, _ in keys_data]
                positions = list(range(len(keys)))
                
                # Create index
                self.index_manager.create_index(
                    index_name,
                    keys,
                    positions,
                    index_type="auto"
                )
                
                logger.info(f"Created index {index_name} with {len(keys)} keys")
    
    async def _rebuild_index(self, index_name: str) -> None:
        """Rebuild a learned index with current data."""
        try:
            prefix = index_name.replace("prefix_", "")
            
            # Get current keys
            keys_data = await self.scylla.scan(prefix=prefix, limit=50000)
            
            if len(keys_data) >= 100:
                keys = [k for k, _ in keys_data]
                positions = list(range(len(keys)))
                
                # Rebuild index
                self.index_manager.create_index(
                    index_name,
                    keys,
                    positions,
                    index_type="auto"
                )
                
                # Reset change counter
                self.changes_since_rebuild[index_name] = 0
                
                logger.info(f"Rebuilt index {index_name} with {len(keys)} keys")
                
        except Exception as e:
            logger.error(f"Failed to rebuild index {index_name}: {e}")
    
    async def _scan_range(
        self,
        key: str,
        start: int,
        end: int
    ) -> Optional[Any]:
        """Scan a position range for a key."""
        # This is a simplified implementation
        # In production, you'd map positions to actual storage locations
        
        # For now, fall back to direct lookup
        return await self.scylla.get(key)
    
    async def _scan_range_full(
        self,
        start: int,
        end: int,
        limit: int
    ) -> List[Tuple[str, Any]]:
        """Scan a position range and return all key-value pairs."""
        # Simplified implementation
        # In production, this would use position mapping
        
        results = []
        # Fallback to scan
        all_data = await self.scylla.scan(limit=limit)
        
        # Simulate position-based filtering
        for i, (key, value) in enumerate(all_data):
            if start <= i <= end:
                results.append((key, value))
                if len(results) >= limit:
                    break
        
        return results
    
    async def _batch_get_with_index(
        self,
        keys: List[str],
        index: LearnedIndex
    ) -> Dict[str, Any]:
        """Batch get using learned index."""
        results = {}
        
        # Get position ranges for all keys
        positions = []
        for key in keys:
            start, end = index.predict(key)
            positions.append((key, start, end))
        
        # Sort by start position for efficient scanning
        positions.sort(key=lambda x: x[1])
        
        # Scan ranges (simplified)
        for key, start, end in positions:
            value = await self._scan_range(key, start, end)
            if value is not None:
                results[key] = value
        
        return results
    
    async def _batch_get_fallback(self, keys: List[str]) -> Dict[str, Any]:
        """Fallback batch get without index."""
        results = {}
        
        for key in keys:
            value = await self.scylla.get(key)
            if value is not None:
                results[key] = value
        
        return results
    
    def _get_index_name(self, key: str) -> str:
        """Get index name for a key based on prefix."""
        if len(key) >= self.index_prefix_length:
            prefix = key[:self.index_prefix_length]
        else:
            prefix = key
        
        return f"prefix_{prefix}"
    
    async def _get_key_prefixes(self) -> List[str]:
        """Get common key prefixes for index creation."""
        # Sample keys to find common prefixes
        sample = await self.scylla.scan(limit=1000)
        
        prefix_counts: Dict[str, int] = {}
        for key, _ in sample:
            if len(key) >= self.index_prefix_length:
                prefix = key[:self.index_prefix_length]
                prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
        
        # Sort by frequency
        sorted_prefixes = sorted(
            prefix_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [prefix for prefix, _ in sorted_prefixes]