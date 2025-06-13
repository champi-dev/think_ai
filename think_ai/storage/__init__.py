"""Storage layer implementations for Think AI."""

# Import modules without circular reference
# Make ScyllaDB import optional to avoid Cassandra driver dependency
# issues in CI
try:
    from . import scylla

    SCYLLA_AVAILABLE = True
    __all__ = ["scylla"]
except ImportError:
    SCYLLA_AVAILABLE = False
    __all__ = []
