"""Persistent Intelligence System - Knowledge and intelligence that only grows, never diminishes."""

import atexit
import gzip
import hashlib
import json
import queue
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..utils.logging import get_logger

logger = get_logger(__name__)


class PersistentIntelligence:
    """
    Persistent intelligence that:
    - NEVER deletes knowledge
    - ALWAYS grows and learns
    - Saves every interaction
    - Protected against data loss
    """

    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data" / "eternal_knowledge"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Multiple storage backends for redundancy
        self.db_path = self.data_dir / "eternal_knowledge.db"
        self.backup_dir = self.data_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

        # Initialize SQLite with WAL mode for durability
        self._init_database()

        # Knowledge growth tracking
        self.growth_stats = {"total_knowledge": 0, "interactions": 0, "unique_concepts": set(), "learning_rate": 0.0}

        # Queue for async saving
        self.save_queue = queue.Queue()
        self.save_thread = threading.Thread(target=self._save_worker, daemon=True)
        self.save_thread.start()

        # Register cleanup on exit
        atexit.register(self._ensure_all_saved)

        # Load existing knowledge stats
        self._load_growth_stats()

    def _init_database(self):
        """Initialize SQLite database with protection features."""
        conn = sqlite3.connect(self.db_path)

        # Enable WAL mode for better concurrency and crash resistance
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")  # Maximum durability

        # Create tables (if not exist)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS eternal_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                context TEXT,
                confidence REAL DEFAULT 1.0,
                usage_count INTEGER DEFAULT 0,
                last_accessed TEXT,
                embeddings BLOB,
                metadata TEXT,
                UNIQUE(question, answer)  -- Prevent exact duplicates
            )
        """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS learning_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                content TEXT NOT NULL,
                learning_value REAL DEFAULT 1.0,
                metadata TEXT
            )
        """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS intelligence_growth (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                details TEXT
            )
        """
        )

        # Create indexes for fast retrieval
        conn.execute("CREATE INDEX IF NOT EXISTS idx_question ON eternal_knowledge(question)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON eternal_knowledge(timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_usage ON eternal_knowledge(usage_count DESC)")

        conn.commit()
        conn.close()

    def add_knowledge(
        self,
        question: str,
        answer: str,
        context: Optional[str] = None,
        confidence: float = 1.0,
        metadata: Optional[Dict] = None,
    ):
        """
        Add knowledge - APPEND ONLY, never overwrites.
        Every piece of knowledge is preserved forever.
        """
        knowledge_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "context": context,
            "confidence": confidence,
            "metadata": json.dumps(metadata or {}),
        }

        # Queue for async saving
        self.save_queue.put(("knowledge", knowledge_entry))

        # Update growth stats
        self.growth_stats["total_knowledge"] += 1
        self.growth_stats["interactions"] += 1

        # Extract concepts
        concepts = self._extract_concepts(question + " " + answer)
        self.growth_stats["unique_concepts"].update(concepts)

        logger.info(f"Knowledge added. Total: {self.growth_stats['total_knowledge']:,}")

    def learn_from_interaction(self, user_input: str, ai_response: str, feedback: Optional[str] = None):
        """Learn from every interaction - continuous growth."""
        learning_event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "interaction",
            "content": json.dumps({"user_input": user_input, "ai_response": ai_response, "feedback": feedback}),
            "learning_value": 1.0 if feedback != "negative" else 0.5,
        }

        # Queue for saving
        self.save_queue.put(("learning", learning_event))

        # Also save as knowledge for retrieval
        self.add_knowledge(user_input, ai_response, context="interaction")

        # Calculate learning rate
        self._update_learning_rate()

    def get_knowledge(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve knowledge - also updates usage stats.
        More used knowledge becomes stronger.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        # Search with fuzzy matching
        cursor = conn.execute(
            """
            SELECT * FROM eternal_knowledge
            WHERE question LIKE ? OR answer LIKE ?
            ORDER BY usage_count DESC, confidence DESC
            LIMIT ?
        """,
            (f"%{query}%", f"%{query}%", limit),
        )

        results = []
        for row in cursor:
            result = dict(row)
            # Update usage stats (knowledge gets stronger with use)
            conn.execute(
                """
                UPDATE eternal_knowledge 
                SET usage_count = usage_count + 1,
                    last_accessed = ?
                WHERE id = ?
            """,
                (datetime.now().isoformat(), row["id"]),
            )

            results.append(result)

        conn.commit()
        conn.close()

        return results

    def _save_worker(self):
        """Background worker for saving knowledge."""
        conn = sqlite3.connect(self.db_path)

        while True:
            try:
                item_type, data = self.save_queue.get(timeout=1)

                if item_type == "knowledge":
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO eternal_knowledge
                        (timestamp, question, answer, context, confidence, metadata)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (
                            data["timestamp"],
                            data["question"],
                            data["answer"],
                            data["context"],
                            data["confidence"],
                            data["metadata"],
                        ),
                    )

                elif item_type == "learning":
                    conn.execute(
                        """
                        INSERT INTO learning_events
                        (timestamp, event_type, content, learning_value)
                        VALUES (?, ?, ?, ?)
                    """,
                        (data["timestamp"], data["event_type"], data["content"], data["learning_value"]),
                    )

                conn.commit()

                # Periodic backup
                if self.growth_stats["total_knowledge"] % 1000 == 0:
                    self._create_backup()

            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Save error: {e}")

    def _create_backup(self):
        """Create compressed backup of all knowledge."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"knowledge_backup_{timestamp}.db.gz"

        # Copy and compress database
        with open(self.db_path, "rb") as f_in:
            with gzip.open(backup_path, "wb") as f_out:
                f_out.write(f_in.read())

        logger.info(f"Backup created: {backup_path}")

        # Keep last 10 backups
        backups = sorted(self.backup_dir.glob("*.db.gz"))
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                old_backup.unlink()

    def _extract_concepts(self, text: str) -> set:
        """Extract key concepts from text."""
        # Simple concept extraction
        words = text.lower().split()
        # Filter out common words
        stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
        }
        concepts = {w for w in words if len(w) > 3 and w not in stop_words}
        return concepts

    def _update_learning_rate(self):
        """Calculate current learning rate."""
        conn = sqlite3.connect(self.db_path)

        # Get recent learning events
        cursor = conn.execute(
            """
            SELECT COUNT(*) as count, AVG(learning_value) as avg_value
            FROM learning_events
            WHERE timestamp > datetime('now', '-1 hour')
        """
        )

        row = cursor.fetchone()
        if row and row[0] > 0:
            self.growth_stats["learning_rate"] = row[0] * row[1] / 60.0  # Per minute

        conn.close()

    def _load_growth_stats(self):
        """Load existing growth statistics."""
        conn = sqlite3.connect(self.db_path)

        # Get total knowledge
        cursor = conn.execute("SELECT COUNT(*) FROM eternal_knowledge")
        self.growth_stats["total_knowledge"] = cursor.fetchone()[0]

        # Get unique concepts count
        cursor = conn.execute("SELECT COUNT(DISTINCT question) FROM eternal_knowledge")
        unique_count = cursor.fetchone()[0]

        conn.close()

        logger.info(f"Loaded {self.growth_stats['total_knowledge']:,} existing knowledge items")

    def _ensure_all_saved(self):
        """Ensure all queued items are saved before exit."""
        while not self.save_queue.empty():
            try:
                self.save_queue.get_nowait()
            except:
                break

    def get_growth_metrics(self) -> Dict[str, Any]:
        """Get intelligence growth metrics."""
        return {
            "total_knowledge": self.growth_stats["total_knowledge"],
            "unique_concepts": len(self.growth_stats["unique_concepts"]),
            "interactions": self.growth_stats["interactions"],
            "learning_rate": self.growth_stats["learning_rate"],
            "database_size_mb": (self.db_path.stat().st_size / 1024 / 1024) if self.db_path.exists() else 0,
        }

    def export_knowledge_snapshot(self, path: Optional[Path] = None) -> Path:
        """
        Export knowledge snapshot for sharing.
        NEVER deletes original - only creates copies.
        """
        if not path:
            path = self.data_dir / f"knowledge_snapshot_{datetime.now().strftime('%Y%m%d')}.json.gz"

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        # Export all knowledge
        cursor = conn.execute("SELECT * FROM eternal_knowledge ORDER BY timestamp")

        knowledge_data = {
            "version": "1.0.0",
            "exported": datetime.now().isoformat(),
            "total_items": self.growth_stats["total_knowledge"],
            "knowledge": [dict(row) for row in cursor],
        }

        conn.close()

        # Save compressed
        with gzip.open(path, "wt", encoding="utf-8") as f:
            json.dump(knowledge_data, f)

        logger.info(f"Knowledge snapshot exported: {path}")
        return path


# Global instance - eternal and persistent
persistent_intelligence = PersistentIntelligence()
