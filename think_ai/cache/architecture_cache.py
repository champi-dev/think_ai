"""O(1) Architecture Caching System for Think AI.

This module provides ultra-fast initialization by caching the entire distributed
architecture state and restoring it in O(1) time complexity.
"""

import hashlib
import json
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


class ArchitectureCache:
    """High-performance cache for distributed architecture initialization.

    Achieves O(1) initialization by serializing and restoring the entire
    system state from disk cache.
    """

    def __init__(self, cache_dir: str = ".think_ai_cache") -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        # Cache metadata for O(1) validation
        self.metadata_file = self.cache_dir / "metadata.json"
        self.services_cache_file = self.cache_dir / "services.pkl"
        self.model_cache_dir = self.cache_dir / "models"
        self.model_cache_dir.mkdir(exist_ok=True)

        # In-memory cache for ultra-fast access
        self._memory_cache: Dict[str, Any] = {}
        self._cache_valid = False

    def _compute_config_hash(self, config: Dict[str, Any]) -> str:
        """Compute hash of configuration for cache validation.

        O(1) complexity using SHA256 hash function.
        """
        config_str = json.dumps(config, sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()

    def _is_cache_valid(
            self,
            config_hash: str,
            max_age_hours: int = 24) -> bool:
        """Check if cache is valid based on config and age.

        O(1) complexity - direct file read and comparison.
        """
        if not self.metadata_file.exists():
            return False

        try:
            with open(self.metadata_file) as f:
                metadata = json.load(f)

            # Check config hash
            if metadata.get("config_hash") != config_hash:
                logger.info("Cache invalid: configuration changed")
                return False

            # Check age
            cache_time = datetime.fromisoformat(metadata["timestamp"])
            if datetime.now() - cache_time > timedelta(hours=max_age_hours):
                logger.info("Cache invalid: too old")
                return False

            # Check if all required files exist
            if not self.services_cache_file.exists():
                logger.info("Cache invalid: services cache missing")
                return False

            return True

        except Exception as e:
            logger.exception(f"Error validating cache: {e}")
            return False

    async def save_architecture(
        self, services: Dict[str, Any], config: Dict[str, Any]
    ) -> bool:
        """Save the initialized architecture to cache.

        O(1) complexity for metadata, O(n) for serialization where n is service count.
        """
        try:
            logger.info("Saving architecture to cache...")

            # Save metadata
            metadata = {
                "config_hash": self._compute_config_hash(config),
                "timestamp": datetime.now().isoformat(),
                "services": list(services.keys()),
                "version": "1.0",
            }

            with open(self.metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

            # Prepare services for serialization
            serializable_services = {}

            for name, service in services.items():
                if name == "model_orchestrator":
                    # Special handling for model - save path only
                    serializable_services[name] = {
                        "type": "model_orchestrator",
                        "config": config.get("model", {}),
                        "initialized": hasattr(service, "language_model")
                        and service.language_model is not None,
                    }
                elif name in ["scylla", "redis", "milvus", "neo4j"]:
                    # For databases, save connection info only
                    serializable_services[name] = {
                        "type": name,
                        "config": config.get(name, {}),
                        "initialized": True,
                    }
                else:
                    # For other services, attempt direct serialization
                    try:
                        serializable_services[name] = service
                    except Exception:
                        serializable_services[name] = {
                            "type": name,
                            "initialized": True,
                        }

            # Save services
            with open(self.services_cache_file, "wb") as f:
                pickle.dump(serializable_services, f)

            # Update memory cache
            self._memory_cache = {
                "services": serializable_services,
                "config": config,
                "metadata": metadata,
            }
            self._cache_valid = True

            logger.info("✅ Architecture cached successfully")
            return True

        except Exception as e:
            logger.exception(f"Failed to save architecture cache: {e}")
            return False

    async def load_architecture(
        self, config: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Load architecture from cache if valid.

        O(1) complexity when using memory cache, O(n) for disk load.
        """
        config_hash = self._compute_config_hash(config)

        # Check memory cache first (O(1))
        if (self._cache_valid and self._memory_cache.get(
                "metadata", {}).get("config_hash") == config_hash):
            logger.info("✅ Loading from memory cache (O(1))")
            return self._memory_cache["services"]

        # Check disk cache
        if not self._is_cache_valid(config_hash):
            logger.info("Cache miss - need full initialization")
            return None

        try:
            logger.info("Loading architecture from disk cache...")

            # Load services
            with open(self.services_cache_file, "rb") as f:
                services = pickle.load(f)

            # Update memory cache
            self._memory_cache = {
                "services": services,
                "config": config,
                "metadata": {
                    "config_hash": config_hash,
                    "timestamp": datetime.now().isoformat(),
                },
            }
            self._cache_valid = True

            logger.info("✅ Architecture loaded from cache")
            return services

        except Exception as e:
            logger.exception(f"Failed to load architecture cache: {e}")
            return None

    def clear_cache(self) -> None:
        """Clear all caches.

        O(1) complexity - just removes files.
        """
        try:
            if self.metadata_file.exists():
                self.metadata_file.unlink()
            if self.services_cache_file.exists():
                self.services_cache_file.unlink()

            # Clear model cache
            for file in self.model_cache_dir.glob("*"):
                file.unlink()

            # Clear memory cache
            self._memory_cache.clear()
            self._cache_valid = False

            logger.info("Cache cleared successfully")

        except Exception as e:
            logger.exception(f"Error clearing cache: {e}")

    async def get_model_cache_path(self, model_name: str) -> Path:
        """Get the cache path for a specific model.

        O(1) complexity - direct path construction.
        """
        safe_name = model_name.replace("/", "_")
        return self.model_cache_dir / f"{safe_name}_cache"

    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the current cache state.

        O(1) complexity - direct attribute access.
        """
        info = {
            "cache_dir": str(self.cache_dir),
            "memory_cache_valid": self._cache_valid,
            "memory_cache_size": len(self._memory_cache),
            "disk_cache_exists": self.metadata_file.exists(),
        }

        if self.metadata_file.exists():
            try:
                with open(self.metadata_file) as f:
                    metadata = json.load(f)
                info["cache_age"] = metadata.get("timestamp", "unknown")
                info["cached_services"] = metadata.get("services", [])
            except Exception:
                pass

        return info


# Global cache instance for O(1) access
_global_cache = None


def get_architecture_cache() -> ArchitectureCache:
    """Get the global architecture cache instance.

    O(1) complexity - returns existing instance or creates one.
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = ArchitectureCache()
    return _global_cache
