"""Distributed storage implementations."""

from .indexed_storage import IndexedStorage
from .scylla import ScyllaDB

__all__ = ["ScyllaDB", "IndexedStorage"]
