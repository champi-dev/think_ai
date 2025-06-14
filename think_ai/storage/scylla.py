"""ScyllaDB storage backend implementation."""

import asyncio
from typing import Any, Dict, List, Optional, AsyncIterator
from datetime import datetime
import json
import uuid
from cassandra.cluster import Cluster, Session
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy, TokenAwarePolicy
from cassandra.query import SimpleStatement, BatchStatement, BatchType
from cassandra import ConsistencyLevel

from ..core.config import ScyllaDBConfig
from ..utils.logging import get_logger
from .base import StorageBackend, StorageItem


logger = get_logger(__name__)


class ScyllaDBBackend(StorageBackend):
    """ScyllaDB storage backend for O(1) key-value operations."""
    
    def __init__(self, config: ScyllaDBConfig):
        self.config = config
        self.cluster: Optional[Cluster] = None
        self.session: Optional[Session] = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize ScyllaDB connection and create keyspace/tables."""
        if self._initialized:
            return
        
        try:
            # Setup authentication if provided
            auth_provider = None
            if self.config.username and self.config.password:
                auth_provider = PlainTextAuthProvider(
                    username=self.config.username,
                    password=self.config.password
                )
            
            # Create cluster connection
            self.cluster = Cluster(
                contact_points=self.config.hosts,
                port=self.config.port,
                auth_provider=auth_provider,
                load_balancing_policy=TokenAwarePolicy(DCAwareRoundRobinPolicy()),
                protocol_version=4
            )
            
            self.session = self.cluster.connect()
            
            # Create keyspace
            await self._create_keyspace()
            
            # Use keyspace
            self.session.set_keyspace(self.config.keyspace)
            
            # Create tables
            await self._create_tables()
            
            self._initialized = True
            logger.info("ScyllaDB backend initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize ScyllaDB: {e}")
            raise
    
    async def _create_keyspace(self) -> None:
        """Create keyspace if it doesn't exist."""
        query = f"""
        CREATE KEYSPACE IF NOT EXISTS {self.config.keyspace}
        WITH replication = {{
            'class': 'SimpleStrategy',
            'replication_factor': {self.config.replication_factor}
        }}
        """
        await self._execute_async(query)
    
    async def _create_tables(self) -> None:
        """Create required tables."""
        # Main storage table
        storage_table = """
        CREATE TABLE IF NOT EXISTS storage (
            key text PRIMARY KEY,
            id text,
            content text,
            metadata text,
            created_at timestamp,
            updated_at timestamp,
            version int
        )
        """
        await self._execute_async(storage_table)
        
        # Index table for prefix queries
        index_table = """
        CREATE TABLE IF NOT EXISTS storage_index (
            prefix text,
            key text,
            created_at timestamp,
            PRIMARY KEY (prefix, key)
        ) WITH CLUSTERING ORDER BY (key ASC)
        """
        await self._execute_async(index_table)
    
    async def close(self) -> None:
        """Close ScyllaDB connection."""
        if self.cluster:
            self.cluster.shutdown()
            self._initialized = False
    
    async def put(self, key: str, item: StorageItem) -> None:
        """Store an item with O(1) performance."""
        query = """
        INSERT INTO storage (key, id, content, metadata, created_at, updated_at, version)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        # Serialize content and metadata
        content_json = json.dumps(item.content)
        metadata_json = json.dumps(item.metadata)
        
        await self._execute_async(
            query,
            [key, item.id, content_json, metadata_json, 
             item.created_at, item.updated_at, item.version]
        )
        
        # Update index for prefix queries
        await self._update_index(key)
    
    async def get(self, key: str) -> Optional[StorageItem]:
        """Retrieve an item with O(1) performance."""
        query = "SELECT * FROM storage WHERE key = %s"
        
        rows = await self._execute_async(query, [key])
        if not rows:
            return None
        
        row = rows[0]
        return StorageItem(
            id=row.id,
            content=json.loads(row.content),
            metadata=json.loads(row.metadata),
            created_at=row.created_at,
            updated_at=row.updated_at,
            version=row.version
        )
    
    async def delete(self, key: str) -> bool:
        """Delete an item."""
        # Check if exists first
        if not await self.exists(key):
            return False
        
        query = "DELETE FROM storage WHERE key = %s"
        await self._execute_async(query, [key])
        
        # Remove from index
        await self._remove_from_index(key)
        
        return True
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists with O(1) performance."""
        query = "SELECT key FROM storage WHERE key = %s LIMIT 1"
        rows = await self._execute_async(query, [key])
        return len(rows) > 0
    
    async def list_keys(self, prefix: Optional[str] = None, limit: int = 100) -> List[str]:
        """List keys with optional prefix filter."""
        if prefix:
            # Use index table for prefix queries
            query = "SELECT key FROM storage_index WHERE prefix = %s LIMIT %s"
            rows = await self._execute_async(query, [self._get_prefix(prefix), limit])
            return [row.key for row in rows if row.key.startswith(prefix)]
        else:
            # Full scan (use with caution)
            query = "SELECT key FROM storage LIMIT %s"
            rows = await self._execute_async(query, [limit])
            return [row.key for row in rows]
    
    async def batch_get(self, keys: List[str]) -> Dict[str, Optional[StorageItem]]:
        """Retrieve multiple items efficiently."""
        results = {}
        
        # Execute parallel queries for better performance
        tasks = []
        for key in keys:
            tasks.append(self.get(key))
        
        items = await asyncio.gather(*tasks)
        
        for key, item in zip(keys, items):
            results[key] = item
        
        return results
    
    async def batch_put(self, items: Dict[str, StorageItem]) -> None:
        """Store multiple items efficiently using batch statements."""
        batch = BatchStatement(batch_type=BatchType.UNLOGGED)
        
        query = """
        INSERT INTO storage (key, id, content, metadata, created_at, updated_at, version)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        for key, item in items.items():
            content_json = json.dumps(item.content)
            metadata_json = json.dumps(item.metadata)
            
            batch.add(SimpleStatement(query), 
                     (key, item.id, content_json, metadata_json,
                      item.created_at, item.updated_at, item.version))
        
        await self._execute_async(batch)
        
        # Update indexes
        for key in items.keys():
            await self._update_index(key)
    
    async def scan(
        self, 
        prefix: Optional[str] = None,
        start_key: Optional[str] = None,
        limit: int = 100
    ) -> AsyncIterator[tuple[str, StorageItem]]:
        """Scan through items with optional filters."""
        if prefix:
            # Use index for prefix scan
            query = "SELECT key FROM storage_index WHERE prefix = %s"
            params = [self._get_prefix(prefix)]
            
            if start_key:
                query += " AND key >= %s"
                params.append(start_key)
            
            query += " LIMIT %s"
            params.append(limit)
            
            rows = await self._execute_async(query, params)
            
            for row in rows:
                if row.key.startswith(prefix):
                    item = await self.get(row.key)
                    if item:
                        yield row.key, item
        else:
            # Full table scan
            query = "SELECT key FROM storage"
            
            if start_key:
                query += " WHERE token(key) > token(%s)"
                params = [start_key]
            else:
                params = []
            
            query += " LIMIT %s"
            params.append(limit)
            
            rows = await self._execute_async(query, params)
            
            for row in rows:
                item = await self.get(row.key)
                if item:
                    yield row.key, item
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        # Get table size
        count_query = "SELECT COUNT(*) as count FROM storage"
        count_rows = await self._execute_async(count_query)
        
        # Get cluster info
        cluster_info = {
            "hosts": self.config.hosts,
            "keyspace": self.config.keyspace,
            "consistency_level": self.config.consistency_level
        }
        
        return {
            "backend": "scylladb",
            "item_count": count_rows[0].count if count_rows else 0,
            "cluster_info": cluster_info,
            "initialized": self._initialized
        }
    
    async def _execute_async(self, query, parameters=None):
        """Execute query asynchronously."""
        loop = asyncio.get_event_loop()
        
        # For parameterized queries, we don't need SimpleStatement
        if parameters:
            # Execute with parameters directly
            future = loop.run_in_executor(
                None,
                lambda: self.session.execute(query, parameters)
            )
        else:
            # For non-parameterized queries, use SimpleStatement for consistency level
            if isinstance(query, str):
                statement = SimpleStatement(
                    query,
                    consistency_level=getattr(ConsistencyLevel, self.config.consistency_level)
                )
            else:
                statement = query
            
            future = loop.run_in_executor(
                None,
                self.session.execute,
                statement
            )
        
        return await future
    
    def _get_prefix(self, key: str) -> str:
        """Extract prefix for indexing (first 3 characters)."""
        return key[:3] if len(key) >= 3 else key
    
    async def _update_index(self, key: str) -> None:
        """Update prefix index for a key."""
        prefix = self._get_prefix(key)
        query = """
        INSERT INTO storage_index (prefix, key, created_at)
        VALUES (%s, %s, %s)
        """
        await self._execute_async(query, [prefix, key, datetime.utcnow()])
    
    async def _remove_from_index(self, key: str) -> None:
        """Remove key from prefix index."""
        prefix = self._get_prefix(key)
        query = "DELETE FROM storage_index WHERE prefix = %s AND key = %s"
        await self._execute_async(query, [prefix, key])