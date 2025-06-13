"""Offline storage implementation using SQLite with FTS5."""

import sqlite3
import json
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, AsyncIterator
from datetime import datetime
import aiosqlite
from contextlib import asynccontextmanager

from ..core.config import OfflineStorageConfig
from ..utils.logging import get_logger
from .base import StorageBackend, StorageItem


logger = get_logger(__name__)


class OfflineStorage(StorageBackend):
    """SQLite-based offline storage with full-text search."""
    
    def __init__(self, config: OfflineStorageConfig):
        self.config = config
        self.db_path = config.db_path
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize SQLite database and create tables."""
        if self._initialized:
            return
        
        try:
            # Ensure directory exists
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create database and tables
            async with self._get_connection() as db:
                # Enable WAL mode for better concurrency
                if self.config.wal_mode:
                    await db.execute("PRAGMA journal_mode=WAL")
                
                # Set cache size
                cache_size_kb = self.config.cache_size_mb * 1024
                await db.execute(f"PRAGMA cache_size=-{cache_size_kb}")
                
                # Create main storage table
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS storage (
                        key TEXT PRIMARY KEY,
                        id TEXT NOT NULL,
                        content TEXT NOT NULL,
                        metadata TEXT NOT NULL,
                        created_at TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP NOT NULL,
                        version INTEGER NOT NULL,
                        synced BOOLEAN DEFAULT FALSE,
                        sync_timestamp TIMESTAMP
                    )
                """)
                
                # Create indexes
                await db.execute("""
                    CREATE INDEX IF NOT EXISTS idx_storage_updated 
                    ON storage(updated_at DESC)
                """)
                
                await db.execute("""
                    CREATE INDEX IF NOT EXISTS idx_storage_synced 
                    ON storage(synced, sync_timestamp)
                """)
                
                # Create FTS5 table for full-text search
                if self.config.enable_fts:
                    await db.execute("""
                        CREATE VIRTUAL TABLE IF NOT EXISTS storage_fts
                        USING fts5(
                            key UNINDEXED,
                            content,
                            metadata,
                            content=storage,
                            content_rowid=rowid
                        )
                    """)
                    
                    # Create triggers to keep FTS in sync
                    await db.execute("""
                        CREATE TRIGGER IF NOT EXISTS storage_fts_insert
                        AFTER INSERT ON storage
                        BEGIN
                            INSERT INTO storage_fts(rowid, key, content, metadata)
                            VALUES (new.rowid, new.key, new.content, new.metadata);
                        END
                    """)
                    
                    await db.execute("""
                        CREATE TRIGGER IF NOT EXISTS storage_fts_update
                        AFTER UPDATE ON storage
                        BEGIN
                            UPDATE storage_fts
                            SET content = new.content, metadata = new.metadata
                            WHERE rowid = new.rowid;
                        END
                    """)
                    
                    await db.execute("""
                        CREATE TRIGGER IF NOT EXISTS storage_fts_delete
                        AFTER DELETE ON storage
                        BEGIN
                            DELETE FROM storage_fts WHERE rowid = old.rowid;
                        END
                    """)
                
                await db.commit()
            
            self._initialized = True
            logger.info(f"Offline storage initialized at {self.db_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize offline storage: {e}")
            raise
    
    @asynccontextmanager
    async def _get_connection(self):
        """Get a database connection with proper settings."""
        async with aiosqlite.connect(self.db_path) as db:
            # Enable foreign keys
            await db.execute("PRAGMA foreign_keys=ON")
            yield db
    
    async def close(self) -> None:
        """Close the storage backend."""
        self._initialized = False
    
    async def put(self, key: str, item: StorageItem) -> None:
        """Store an item in offline storage."""
        async with self._get_connection() as db:
            await db.execute("""
                INSERT OR REPLACE INTO storage
                (key, id, content, metadata, created_at, updated_at, version, synced)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                key,
                item.id,
                json.dumps(item.content),
                json.dumps(item.metadata),
                item.created_at.isoformat(),
                item.updated_at.isoformat(),
                item.version,
                False  # Mark as not synced
            ))
            await db.commit()
    
    async def get(self, key: str) -> Optional[StorageItem]:
        """Retrieve an item from offline storage."""
        async with self._get_connection() as db:
            async with db.execute(
                "SELECT * FROM storage WHERE key = ?", (key,)
            ) as cursor:
                row = await cursor.fetchone()
                
                if not row:
                    return None
                
                return self._row_to_item(row)
    
    async def delete(self, key: str) -> bool:
        """Delete an item from offline storage."""
        async with self._get_connection() as db:
            cursor = await db.execute(
                "DELETE FROM storage WHERE key = ?", (key,)
            )
            await db.commit()
            return cursor.rowcount > 0
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists in offline storage."""
        async with self._get_connection() as db:
            async with db.execute(
                "SELECT 1 FROM storage WHERE key = ? LIMIT 1", (key,)
            ) as cursor:
                return await cursor.fetchone() is not None
    
    async def list_keys(self, prefix: Optional[str] = None, limit: int = 100) -> List[str]:
        """List keys with optional prefix filter."""
        async with self._get_connection() as db:
            if prefix:
                query = "SELECT key FROM storage WHERE key LIKE ? ORDER BY key LIMIT ?"
                params = (f"{prefix}%", limit)
            else:
                query = "SELECT key FROM storage ORDER BY key LIMIT ?"
                params = (limit,)
            
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
    
    async def batch_get(self, keys: List[str]) -> Dict[str, Optional[StorageItem]]:
        """Retrieve multiple items by keys."""
        if not keys:
            return {}
        
        results = {}
        
        async with self._get_connection() as db:
            placeholders = ",".join(["?" for _ in keys])
            query = f"SELECT * FROM storage WHERE key IN ({placeholders})"
            
            async with db.execute(query, keys) as cursor:
                async for row in cursor:
                    item = self._row_to_item(row)
                    results[row[0]] = item  # row[0] is the key
        
        # Fill in None for missing keys
        for key in keys:
            if key not in results:
                results[key] = None
        
        return results
    
    async def batch_put(self, items: Dict[str, StorageItem]) -> None:
        """Store multiple items efficiently."""
        if not items:
            return
        
        async with self._get_connection() as db:
            data = [
                (
                    key,
                    item.id,
                    json.dumps(item.content),
                    json.dumps(item.metadata),
                    item.created_at.isoformat(),
                    item.updated_at.isoformat(),
                    item.version,
                    False  # Not synced
                )
                for key, item in items.items()
            ]
            
            await db.executemany("""
                INSERT OR REPLACE INTO storage
                (key, id, content, metadata, created_at, updated_at, version, synced)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            
            await db.commit()
    
    async def scan(
        self, 
        prefix: Optional[str] = None,
        start_key: Optional[str] = None,
        limit: int = 100
    ) -> AsyncIterator[tuple[str, StorageItem]]:
        """Scan through items with optional filters."""
        async with self._get_connection() as db:
            query = "SELECT * FROM storage WHERE 1=1"
            params = []
            
            if prefix:
                query += " AND key LIKE ?"
                params.append(f"{prefix}%")
            
            if start_key:
                query += " AND key >= ?"
                params.append(start_key)
            
            query += " ORDER BY key LIMIT ?"
            params.append(limit)
            
            async with db.execute(query, params) as cursor:
                async for row in cursor:
                    yield row[0], self._row_to_item(row)  # row[0] is the key
    
    async def search_text(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Full-text search using FTS5."""
        if not self.config.enable_fts:
            raise RuntimeError("Full-text search is not enabled")
        
        async with self._get_connection() as db:
            # Use FTS5 match syntax
            fts_query = f'"{query}"' if " " in query else query
            
            async with db.execute("""
                SELECT s.*, rank
                FROM storage s
                JOIN storage_fts fts ON s.rowid = fts.rowid
                WHERE storage_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (fts_query, limit)) as cursor:
                
                results = []
                async for row in cursor:
                    item = self._row_to_item(row[:-1])  # Exclude rank column
                    results.append({
                        "key": row[0],
                        "item": item,
                        "rank": row[-1]
                    })
                
                return results
    
    async def get_unsynced_items(self, limit: int = 100) -> List[tuple[str, StorageItem]]:
        """Get items that haven't been synced to online storage."""
        async with self._get_connection() as db:
            async with db.execute("""
                SELECT * FROM storage
                WHERE synced = 0
                ORDER BY updated_at DESC
                LIMIT ?
            """, (limit,)) as cursor:
                
                items = []
                async for row in cursor:
                    items.append((row[0], self._row_to_item(row)))
                
                return items
    
    async def mark_synced(self, keys: List[str]) -> None:
        """Mark items as synced to online storage."""
        if not keys:
            return
        
        async with self._get_connection() as db:
            placeholders = ",".join(["?" for _ in keys])
            await db.execute(f"""
                UPDATE storage
                SET synced = 1, sync_timestamp = ?
                WHERE key IN ({placeholders})
            """, [datetime.utcnow().isoformat()] + keys)
            
            await db.commit()
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        async with self._get_connection() as db:
            # Get total count
            async with db.execute("SELECT COUNT(*) FROM storage") as cursor:
                total_count = (await cursor.fetchone())[0]
            
            # Get unsynced count
            async with db.execute("SELECT COUNT(*) FROM storage WHERE synced = 0") as cursor:
                unsynced_count = (await cursor.fetchone())[0]
            
            # Get database size
            db_size = self.db_path.stat().st_size if self.db_path.exists() else 0
            
            return {
                "backend": "sqlite",
                "path": str(self.db_path),
                "total_items": total_count,
                "unsynced_items": unsynced_count,
                "database_size_bytes": db_size,
                "database_size_mb": round(db_size / (1024 * 1024), 2),
                "fts_enabled": self.config.enable_fts,
                "wal_mode": self.config.wal_mode
            }
    
    def _row_to_item(self, row: tuple) -> StorageItem:
        """Convert a database row to a StorageItem."""
        return StorageItem(
            id=row[1],
            content=json.loads(row[2]),
            metadata=json.loads(row[3]),
            created_at=datetime.fromisoformat(row[4]),
            updated_at=datetime.fromisoformat(row[5]),
            version=row[6]
        )


class OfflineSyncManager:
    """Manages synchronization between offline and online storage."""
    
    def __init__(
        self,
        offline_storage: OfflineStorage,
        online_storage: StorageBackend
    ):
        self.offline = offline_storage
        self.online = online_storage
        self.is_syncing = False
    
    async def sync_to_online(self, batch_size: int = 100) -> Dict[str, Any]:
        """Sync unsynced items from offline to online storage."""
        if self.is_syncing:
            return {"status": "already_syncing"}
        
        self.is_syncing = True
        sync_stats = {
            "started_at": datetime.utcnow(),
            "items_synced": 0,
            "errors": []
        }
        
        try:
            while True:
                # Get batch of unsynced items
                unsynced = await self.offline.get_unsynced_items(batch_size)
                
                if not unsynced:
                    break
                
                # Prepare batch for online storage
                items_to_sync = {}
                keys_to_mark = []
                
                for key, item in unsynced:
                    items_to_sync[key] = item
                    keys_to_mark.append(key)
                
                try:
                    # Sync to online storage
                    await self.online.batch_put(items_to_sync)
                    
                    # Mark as synced
                    await self.offline.mark_synced(keys_to_mark)
                    
                    sync_stats["items_synced"] += len(items_to_sync)
                    
                except Exception as e:
                    logger.error(f"Error syncing batch: {e}")
                    sync_stats["errors"].append(str(e))
                    break
            
            sync_stats["completed_at"] = datetime.utcnow()
            sync_stats["duration_seconds"] = (
                sync_stats["completed_at"] - sync_stats["started_at"]
            ).total_seconds()
            
            return sync_stats
            
        finally:
            self.is_syncing = False
    
    async def sync_from_online(
        self,
        keys: Optional[List[str]] = None,
        prefix: Optional[str] = None,
        limit: int = 1000
    ) -> Dict[str, Any]:
        """Sync items from online to offline storage."""
        sync_stats = {
            "started_at": datetime.utcnow(),
            "items_synced": 0,
            "errors": []
        }
        
        try:
            if keys:
                # Sync specific keys
                items = await self.online.batch_get(keys)
                
                # Filter out None values and prepare for offline storage
                items_to_store = {
                    k: v for k, v in items.items() if v is not None
                }
                
                if items_to_store:
                    await self.offline.batch_put(items_to_store)
                    sync_stats["items_synced"] = len(items_to_store)
            
            else:
                # Sync by prefix or all
                count = 0
                async for key, item in self.online.scan(prefix=prefix, limit=limit):
                    await self.offline.put(key, item)
                    count += 1
                
                sync_stats["items_synced"] = count
            
            sync_stats["completed_at"] = datetime.utcnow()
            sync_stats["duration_seconds"] = (
                sync_stats["completed_at"] - sync_stats["started_at"]
            ).total_seconds()
            
            return sync_stats
            
        except Exception as e:
            logger.error(f"Error syncing from online: {e}")
            sync_stats["errors"].append(str(e))
            return sync_stats