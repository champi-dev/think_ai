#!/usr/bin/env python3
"""
O(1) Dependency Cache System
Content-addressed storage with SQLite indexing for instant lookups
"""

import hashlib
import json
import os
import shutil
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class DependencyMetadata:
    """Metadata for cached dependencies"""

    name: str
    version: str
    platform: str
    python_version: str
    size: int
    sha256: str
    download_url: str
    cached_path: str
    metadata_vector: List[float]  # For similarity search
    timestamp: float


class O1DependencyCache:
    """
    Content-addressed dependency cache with O(1) lookup
    Similar to how Git stores objects by hash
    """

    def __init__(self, cache_dir: str = ".o1-dep-cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        # Initialize SQLite for O(1) metadata lookups
        self.db_path = self.cache_dir / "deps.db"
        self._init_db()

        # Hash-based storage directories (like Git objects)
        self.objects_dir = self.cache_dir / "objects"
        self.objects_dir.mkdir(exist_ok=True)

        # Metadata vectors for finding similar packages
        self.vectors_dir = self.cache_dir / "vectors"
        self.vectors_dir.mkdir(exist_ok=True)

    def _init_db(self):
        """Initialize SQLite database for O(1) lookups"""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS dependencies (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                version TEXT NOT NULL,
                platform TEXT NOT NULL,
                python_version TEXT NOT NULL,
                size INTEGER NOT NULL,
                sha256 TEXT UNIQUE NOT NULL,
                download_url TEXT,
                cached_path TEXT NOT NULL,
                metadata_vector BLOB,
                timestamp REAL NOT NULL,
                UNIQUE(name, version, platform, python_version)
            )
        """
        )

        # Create indexes for O(1) lookups
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sha256 ON dependencies(sha256)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_name_version ON dependencies(name, version)")
        conn.commit()
        conn.close()

    def _compute_package_vector(self, name: str, version: str) -> List[float]:
        """
        Create a vector representation of package metadata
        Used for similarity search and recommendations
        """
        # Simple hash-based vector for demo
        text = f"{name} {version}"
        hash_bytes = hashlib.sha256(text.encode()).digest()
        # Convert to normalized vector (first 32 bytes)
        vector = [b / 255.0 for b in hash_bytes[:32]]
        return vector

    def _get_object_path(self, sha256: str) -> Path:
        """Get content-addressed storage path (like Git)"""
        # Use first 2 chars as directory (like Git)
        return self.objects_dir / sha256[:2] / sha256[2:]

    def cache_dependency(self, wheel_path: Path) -> Optional[DependencyMetadata]:
        """Cache a wheel file with O(1) future lookup"""
        if not wheel_path.exists():
            return None

        # Parse wheel filename (e.g., torch-2.1.2-cp311-cp311-linux_x86_64.whl)
        filename = wheel_path.name
        parts = filename.split("-")
        if len(parts) < 5:
            return None

        name = parts[0]
        version = parts[1]
        python_version = parts[2]
        platform = "-".join(parts[3:]).replace(".whl", "")

        # Compute SHA256 for content addressing
        sha256 = self._compute_file_hash(wheel_path)

        # Check if already cached (O(1) lookup)
        if self.is_cached(sha256):
            print(f"✅ Already cached: {filename}")
            return self.get_by_hash(sha256)

        # Store in content-addressed location
        object_path = self._get_object_path(sha256)
        object_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy wheel to cache
        shutil.copy2(wheel_path, object_path)

        # Create metadata
        metadata = DependencyMetadata(
            name=name,
            version=version,
            platform=platform,
            python_version=python_version,
            size=wheel_path.stat().st_size,
            sha256=sha256,
            download_url="",
            cached_path=str(object_path),
            metadata_vector=self._compute_package_vector(name, version),
            timestamp=time.time(),
        )

        # Store in database
        self._save_metadata(metadata)

        print(f"💾 Cached: {filename} -> {sha256[:8]}...")
        return metadata

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _save_metadata(self, metadata: DependencyMetadata):
        """Save metadata to SQLite"""
        conn = sqlite3.connect(self.db_path)
        vector_blob = json.dumps(metadata.metadata_vector).encode()

        conn.execute(
            """
            INSERT OR REPLACE INTO dependencies
            (name, version, platform, python_version, size, sha256,
             download_url, cached_path, metadata_vector, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                metadata.name,
                metadata.version,
                metadata.platform,
                metadata.python_version,
                metadata.size,
                metadata.sha256,
                metadata.download_url,
                metadata.cached_path,
                vector_blob,
                metadata.timestamp,
            ),
        )
        conn.commit()
        conn.close()

    def is_cached(self, sha256: str) -> bool:
        """O(1) check if dependency is cached"""
        conn = sqlite3.connect(self.db_path)
        result = conn.execute("SELECT 1 FROM dependencies WHERE sha256 = ? LIMIT 1", (sha256,)).fetchone()
        conn.close()
        return result is not None

    def get_by_hash(self, sha256: str) -> Optional[DependencyMetadata]:
        """O(1) retrieval by content hash"""
        conn = sqlite3.connect(self.db_path)
        row = conn.execute("SELECT * FROM dependencies WHERE sha256 = ?", (sha256,)).fetchone()
        conn.close()

        if not row:
            return None

        return self._row_to_metadata(row)

    def get_by_name_version(self, name: str, version: str, platform: str = None) -> Optional[DependencyMetadata]:
        """O(1) retrieval by name and version"""
        conn = sqlite3.connect(self.db_path)

        if platform:
            row = conn.execute(
                "SELECT * FROM dependencies WHERE name = ? AND version = ? AND platform = ?", (name, version, platform)
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT * FROM dependencies WHERE name = ? AND version = ? LIMIT 1", (name, version)
            ).fetchone()

        conn.close()
        return self._row_to_metadata(row) if row else None

    def _row_to_metadata(self, row) -> DependencyMetadata:
        """Convert database row to metadata object"""
        return DependencyMetadata(
            name=row[1],
            version=row[2],
            platform=row[3],
            python_version=row[4],
            size=row[5],
            sha256=row[6],
            download_url=row[7],
            cached_path=row[8],
            metadata_vector=json.loads(row[9]),
            timestamp=row[10],
        )

    def find_similar(self, name: str, limit: int = 5) -> List[DependencyMetadata]:
        """
        Find similar packages using vector similarity
        (Demonstrates how vector search could work for package discovery)
        """
        # Get vector for query
        query_vector = self._compute_package_vector(name, "")

        # In a real implementation, use FAISS or similar for vector search
        # For now, return packages with similar names
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute("SELECT * FROM dependencies WHERE name LIKE ? LIMIT ?", (f"%{name}%", limit)).fetchall()
        conn.close()

        return [self._row_to_metadata(row) for row in rows]

    def generate_requirements_cache(self, requirements_file: str) -> Dict[str, str]:
        """Generate cache manifest for requirements.txt"""
        cache_manifest = {}

        with open(requirements_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Parse requirement (simplified)
                if "==" in line:
                    name, version = line.split("==")
                    name = name.strip()
                    version = version.strip()

                    # Check cache
                    metadata = self.get_by_name_version(name, version)
                    if metadata:
                        cache_manifest[line] = metadata.cached_path
                        print(f"✅ Found in cache: {name}=={version}")
                    else:
                        print(f"❌ Not in cache: {name}=={version}")

        return cache_manifest

    def install_from_cache(self, requirements_file: str) -> str:
        """Generate pip install command using cache"""
        manifest = self.generate_requirements_cache(requirements_file)

        if not manifest:
            return f"pip install -r {requirements_file}"

        # Build optimized install command
        wheels = list(manifest.values())
        return f"pip install {' '.join(wheels)} && pip install -r {requirements_file}"

    def cache_statistics(self) -> Dict:
        """Get cache statistics"""
        conn = sqlite3.connect(self.db_path)

        stats = {
            "total_packages": conn.execute("SELECT COUNT(*) FROM dependencies").fetchone()[0],
            "total_size": conn.execute("SELECT SUM(size) FROM dependencies").fetchone()[0] or 0,
            "unique_packages": conn.execute("SELECT COUNT(DISTINCT name) FROM dependencies").fetchone()[0],
            "platforms": conn.execute("SELECT DISTINCT platform FROM dependencies").fetchall(),
        }

        conn.close()

        # Add cache directory size
        cache_size = sum(f.stat().st_size for f in self.objects_dir.rglob("*") if f.is_file())
        stats["cache_size_bytes"] = cache_size
        stats["cache_size_mb"] = cache_size / (1024 * 1024)

        return stats


def main():
    """Demo of O(1) dependency cache"""
    cache = O1DependencyCache()

    print("🚀 O(1) Dependency Cache System")
    print("=" * 50)

    # Example: Cache some wheels
    wheels_dir = Path("railway-cache/wheels")
    if wheels_dir.exists():
        print("\n📦 Caching existing wheels...")
        for wheel in wheels_dir.glob("*.whl"):
            cache.cache_dependency(wheel)

    # Show statistics
    stats = cache.cache_statistics()
    print(f"\n📊 Cache Statistics:")
    print(f"  Total packages: {stats['total_packages']}")
    print(f"  Unique packages: {stats['unique_packages']}")
    print(f"  Cache size: {stats['cache_size_mb']:.2f} MB")

    # Example: Find package
    print("\n🔍 Testing O(1) lookup...")
    metadata = cache.get_by_name_version("numpy", "1.24.3")
    if metadata:
        print(f"  Found: {metadata.name}=={metadata.version}")
        print(f"  Location: {metadata.cached_path}")
        print(f"  SHA256: {metadata.sha256[:16]}...")

    # Generate install command
    if Path("requirements-full.txt").exists():
        print("\n⚡ Optimized install command:")
        cmd = cache.install_from_cache("requirements-full.txt")
        print(f"  {cmd[:100]}...")


if __name__ == "__main__":
    main()
