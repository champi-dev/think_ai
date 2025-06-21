"""Distributed storage implementations."""

from .scylla import ScyllaDB
from .indexed_storage import IndexedStorage

__all__ = ['ScyllaDB', 'IndexedStorage']