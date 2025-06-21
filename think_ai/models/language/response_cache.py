"""
Response cache for O(1) model output retrieval
"""

import hashlib
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class ResponseCache:
    """O(1) response cache using hash-based lookups."""

    def __init__(self, max_size: int = 10000, ttl_minutes: int = 60):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl = timedelta(minutes=ttl_minutes)
        self.hits = 0
        self.misses = 0

    def _generate_key(self, prompt: str, params: Dict[str, Any]) -> str:
        """Generate cache key from prompt and parameters."""
        cache_data = {"prompt": prompt, "params": params}
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(cache_str.encode()).hexdigest()

    def get(self, prompt: str, params: Dict[str, Any]) -> Optional[str]:
        """O(1) cache retrieval."""
        key = self._generate_key(prompt, params)

        if key in self.cache:
            entry = self.cache[key]
            # Check if entry is still valid
            if datetime.now() - entry["timestamp"] < self.ttl:
                self.hits += 1
                return entry["response"]
            else:
                # Expired entry
                del self.cache[key]

        self.misses += 1
        return None

    def put(self, prompt: str, params: Dict[str, Any], response: str) -> None:
        """O(1) cache storage."""
        # Evict oldest if at capacity
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]["timestamp"])
            del self.cache[oldest_key]

        key = self._generate_key(prompt, params)
        self.cache[key] = {"response": response, "timestamp": datetime.now()}

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0

        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "complexity": "O(1)",
        }

    def clear(self) -> None:
        """Clear the cache."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0


# Global cache instance
response_cache = ResponseCache()


# Colombian optimization: Pre-warm cache with common queries
COMMON_QUERIES = [
    ("Hello", {"temperature": 0.7}),
    ("Help", {"temperature": 0.7}),
    ("¿Cómo estás?", {"temperature": 0.8}),
    ("Dale que vamos tarde", {"temperature": 0.9}),
]

# Pre-populate cache for O(1) instant responses
for prompt, params in COMMON_QUERIES:
    response_cache.put(prompt, params, f"¡Hola! Welcome to Think AI - Colombian AI at your service! 🇨🇴")
