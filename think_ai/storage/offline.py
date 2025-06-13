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
        online_storage: StorageBackend,
        vector_db = None,
        embedding_model = None
    ):
        self.offline = offline_storage
        self.online = online_storage
        self.vector_db = vector_db
        self.embedding_model = embedding_model
        self.is_syncing = False
        self.sync_history: List[Dict[str, Any]] = []
    
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
                    
                    # Sync vector embeddings if available
                    if self.vector_db and self.embedding_model:
                        await self._sync_vectors(items_to_sync)
                    
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
            
            # Record sync history
            self.sync_history.append(sync_stats)
            
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
    
    async def _sync_vectors(self, items: Dict[str, StorageItem]) -> None:
        """Sync vector embeddings for items."""
        try:
            # Generate embeddings
            texts = [str(item.content) for item in items.values()]
            embeddings = await self.embedding_model.embed_texts(texts)
            
            # Prepare metadata
            keys = list(items.keys())
            metadatas = [
                {"key": key, "synced_from": "offline", **items[key].metadata}
                for key in keys
            ]
            
            # Store in vector database
            await self.vector_db.insert_vectors(
                "think_ai_vectors",  # Collection name
                embeddings,
                keys,
                metadatas
            )
            
            logger.info(f"Synced {len(embeddings)} vector embeddings")
            
        except Exception as e:
            logger.error(f"Failed to sync vectors: {e}")
    
    async def get_sync_status(self) -> Dict[str, Any]:
        """Get comprehensive sync status."""
        offline_stats = await self.offline.get_stats()
        
        status = {
            "is_syncing": self.is_syncing,
            "offline_items": offline_stats["total_items"],
            "unsynced_items": offline_stats["unsynced_items"],
            "sync_percentage": (
                (offline_stats["total_items"] - offline_stats["unsynced_items"]) /
                max(offline_stats["total_items"], 1) * 100
            ),
            "last_sync": self.sync_history[-1] if self.sync_history else None,
            "total_syncs": len(self.sync_history),
            "sync_health": self._calculate_sync_health()
        }
        
        return status
    
    def _calculate_sync_health(self) -> str:
        """Calculate overall sync health."""
        if not self.sync_history:
            return "no_data"
        
        recent_syncs = self.sync_history[-5:]
        error_rate = sum(1 for s in recent_syncs if s.get("errors")) / len(recent_syncs)
        
        if error_rate == 0:
            return "excellent"
        elif error_rate < 0.2:
            return "good"
        elif error_rate < 0.5:
            return "fair"
        else:
            return "poor"


class AdvancedOfflineManager:
    """Advanced offline capabilities with conflict resolution."""
    
    def __init__(
        self,
        offline_storage: OfflineStorage,
        sync_manager: OfflineSyncManager
    ):
        self.offline = offline_storage
        self.sync_manager = sync_manager
        self.conflict_resolution_strategy = "last_write_wins"
    
    async def handle_conflict(
        self,
        local_item: StorageItem,
        remote_item: StorageItem,
        key: str
    ) -> StorageItem:
        """Resolve conflicts between local and remote versions."""
        if self.conflict_resolution_strategy == "last_write_wins":
            # Choose the most recently updated version
            if local_item.updated_at > remote_item.updated_at:
                logger.info(f"Conflict for {key}: choosing local version")
                return local_item
            else:
                logger.info(f"Conflict for {key}: choosing remote version")
                return remote_item
        
        elif self.conflict_resolution_strategy == "merge":
            # Merge metadata and choose longer content
            merged_metadata = {**remote_item.metadata, **local_item.metadata}
            
            if len(str(local_item.content)) > len(str(remote_item.content)):
                content = local_item.content
            else:
                content = remote_item.content
            
            return StorageItem(
                id=local_item.id,
                content=content,
                metadata=merged_metadata,
                created_at=min(local_item.created_at, remote_item.created_at),
                updated_at=max(local_item.updated_at, remote_item.updated_at),
                version=max(local_item.version, remote_item.version) + 1
            )
        
        else:
            # Default to remote
            return remote_item
    
    async def smart_sync(self) -> Dict[str, Any]:
        """Perform intelligent sync with conflict resolution."""
        sync_report = {
            "started_at": datetime.utcnow(),
            "conflicts_resolved": 0,
            "items_uploaded": 0,
            "items_downloaded": 0,
            "errors": []
        }
        
        try:
            # Get unsynced items
            unsynced = await self.offline.get_unsynced_items(limit=1000)
            
            # Check for conflicts
            for key, local_item in unsynced:
                remote_item = await self.sync_manager.online.get(key)
                
                if remote_item and remote_item.version != local_item.version:
                    # Conflict detected
                    resolved_item = await self.handle_conflict(
                        local_item, remote_item, key
                    )
                    
                    # Update both local and remote with resolved version
                    await self.offline.put(key, resolved_item)
                    await self.sync_manager.online.put(key, resolved_item)
                    
                    sync_report["conflicts_resolved"] += 1
                else:
                    # No conflict, proceed with normal sync
                    await self.sync_manager.online.put(key, local_item)
                    sync_report["items_uploaded"] += 1
            
            # Mark all as synced
            await self.offline.mark_synced([key for key, _ in unsynced])
            
            # Download new items from online
            # (In production, track last sync timestamp for efficiency)
            
            sync_report["completed_at"] = datetime.utcnow()
            sync_report["success"] = True
            
        except Exception as e:
            sync_report["errors"].append(str(e))
            sync_report["success"] = False
            logger.error(f"Smart sync failed: {e}")
        
        return sync_report
    
    async def enable_offline_mode(self) -> None:
        """Enable full offline mode with local-first operation."""
        logger.info("Enabling offline mode - all operations will be local-first")
        # Set flags for offline operation
        # In production, this would configure the entire system for offline mode
    
    async def prepare_for_offline(self, prefetch_keys: List[str]) -> Dict[str, Any]:
        """Prefetch content for offline usage."""
        results = {
            "prefetched": 0,
            "failed": 0,
            "already_cached": 0
        }
        
        for key in prefetch_keys:
            # Check if already in offline storage
            if await self.offline.exists(key):
                results["already_cached"] += 1
                continue
            
            try:
                # Fetch from online
                item = await self.sync_manager.online.get(key)
                if item:
                    # Store offline
                    await self.offline.put(key, item)
                    results["prefetched"] += 1
                else:
                    results["failed"] += 1
            except Exception as e:
                logger.error(f"Failed to prefetch {key}: {e}")
                results["failed"] += 1
        
        return results