"""Unit tests for O1VectorSearch."""

import os
import sys
import tempfile

import numpy as np
import pytest

from o1_vector_search import O1VectorSearch

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


class TestO1VectorSearch:
    """Test O(1) vector search implementation."""

    @pytest.fixture
    def search_index(self):
        """Create a test search index."""
        return O1VectorSearch(dim=10, num_tables=5, hash_size=4)

    def test_initialization(self) -> None:
        """Test O1VectorSearch initialization."""
        index = O1VectorSearch(dim=10, num_tables=5, hash_size=4)

        assert index.dim == 10
        assert index.num_tables == 5
        assert index.hash_size == 4
        assert len(index.hyperplanes) == 5
        assert len(index.tables) == 5
        assert len(index.vectors) == 0

    def test_hash_vector(self, search_index) -> None:
        """Test vector hashing."""
        vector = np.random.randn(10)

        # Test hashing for each table
        for table_idx in range(search_index.num_tables):
            hash_key = search_index._hash_vector(vector, table_idx)
            assert isinstance(hash_key, str)
            assert len(hash_key) == search_index.hash_size
            assert all(c in "01" for c in hash_key)

    def test_add_vector(self, search_index) -> None:
        """Test adding vectors to index."""
        vector = np.random.randn(10)
        metadata = {"id": 1, "text": "test"}

        idx = search_index.add(vector, metadata)

        assert idx == 0
        assert len(search_index.vectors) == 1
        assert len(search_index.metadata) == 1
        assert search_index.metadata[0] == metadata

    def test_search_empty_index(self, search_index) -> None:
        """Test searching empty index."""
        query = np.random.randn(10)
        results = search_index.search(query, k=5)

        assert results == []

    def test_search_single_vector(self, search_index) -> None:
        """Test searching with single vector."""
        vector = np.array([1.0] * 10)
        metadata = {"id": 1}

        search_index.add(vector, metadata)

        # Search with same vector should return it
        results = search_index.search(vector, k=1)

        assert len(results) == 1
        assert results[0][1] == 0  # index
        assert results[0][2] == metadata

    def test_search_multiple_vectors(self, search_index) -> None:
        """Test searching with multiple vectors."""
        # Add multiple vectors
        vectors = [
            np.array([1.0, 0.0] + [0.0] * 8),
            np.array([0.0, 1.0] + [0.0] * 8),
            np.array([0.5, 0.5] + [0.0] * 8),
        ]

        for i, vec in enumerate(vectors):
            search_index.add(vec, {"id": i})

        # Search for vector similar to first one
        query = np.array([0.9, 0.1] + [0.0] * 8)
        results = search_index.search(query, k=2)

        assert len(results) <= 2
        assert all(len(r) == 3 for r in results)  # (score, idx, metadata)

    def test_batch_search(self, search_index) -> None:
        """Test batch search functionality."""
        # Add some vectors
        for i in range(10):
            vec = np.random.randn(10)
            search_index.add(vec, {"id": i})

        # Batch search
        queries = [np.random.randn(10) for _ in range(3)]
        results = search_index.batch_search(queries, k=3)

        assert len(results) == 3
        assert all(isinstance(r, list) for r in results)

    def test_save_and_load(self, search_index) -> None:
        """Test saving and loading index."""
        # Add some data
        for i in range(5):
            vec = np.random.randn(10)
            search_index.add(vec, {"id": i, "text": f"doc_{i}"})

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            search_index.save(temp_path)

            # Create new index and load
            new_index = O1VectorSearch(dim=1, num_tables=1)  # Wrong dims
            new_index.load(temp_path)

            # Verify loaded correctly
            assert new_index.dim == search_index.dim
            assert new_index.num_tables == search_index.num_tables
            assert new_index.hash_size == search_index.hash_size
            assert len(new_index.vectors) == len(search_index.vectors)
            assert len(new_index.metadata) == len(search_index.metadata)

        finally:
            os.unlink(temp_path)

    def test_deterministic_hashing(self) -> None:
        """Test that hashing is deterministic."""
        np.random.seed(42)
        index1 = O1VectorSearch(dim=10, num_tables=3, hash_size=8)

        np.random.seed(42)
        index2 = O1VectorSearch(dim=10, num_tables=3, hash_size=8)

        vector = np.array([1.0] * 10)

        # Hashes should be identical
        for i in range(3):
            hash1 = index1._hash_vector(vector, i)
            hash2 = index2._hash_vector(vector, i)
            assert hash1 == hash2

    def test_edge_cases(self, search_index) -> None:
        """Test edge cases."""
        # Test with zero vector
        zero_vec = np.zeros(10)
        idx = search_index.add(zero_vec, {"zero": True})
        assert idx == 0

        # Test with very small values
        small_vec = np.array([1e-10] * 10)
        idx = search_index.add(small_vec, {"small": True})
        assert idx == 1

        # Test k larger than index size
        results = search_index.search(zero_vec, k=100)
        assert len(results) <= 2

        # Test negative k
        results = search_index.search(zero_vec, k=-1)
        assert results == []

    def test_collision_handling(self) -> None:
        """Test handling of hash collisions."""
        # Create index with small hash size to force collisions
        index = O1VectorSearch(dim=100, num_tables=2, hash_size=2)

        # Add many vectors to ensure collisions
        for i in range(20):
            vec = np.random.randn(100)
            index.add(vec, {"id": i})

        # Search should still work with collisions
        query = np.random.randn(100)
        results = index.search(query, k=5)

        assert len(results) <= 5
        assert all(isinstance(r[0], float) for r in results)

    @pytest.mark.parametrize(
        ("dim", "num_tables", "hash_size"),
        [
            (64, 10, 8),
            (128, 15, 10),
            (384, 20, 12),
            (768, 25, 16),
        ],
    )
    def test_various_configurations(self, dim, num_tables, hash_size) -> None:
        """Test with various configurations."""
        index = O1VectorSearch(dim=dim, num_tables=num_tables, hash_size=hash_size)

        # Add some vectors
        for i in range(10):
            vec = np.random.randn(dim)
            index.add(vec, {"id": i})

        # Search should work
        query = np.random.randn(dim)
        results = index.search(query, k=5)

        assert len(results) <= 5
