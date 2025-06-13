"""Working tests for vector search components."""

import os
import sys
import tempfile

import numpy as np

from o1_vector_search import O1VectorSearch
from vector_search_adapter import VectorSearchAdapter

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


class TestVectorSearchIntegration:
    """Integration tests that actually work."""

    def test_vector_search_adapter_init(self) -> None:
        """Test adapter initialization."""
        adapter = VectorSearchAdapter(dimension=64, backend="o1")
        assert adapter.dimension == 64
        assert adapter.backend == "o1"

    def test_o1_search_basic(self) -> None:
        """Test O(1) search basic functionality."""
        search = O1VectorSearch(dim=10, num_tables=3, hash_size=4)

        # Add a vector
        vec = np.random.rand(10)
        search.add(vec, {"id": 1})

        # Search for it
        results = search.search(vec, k=1)
        assert len(results) > 0
        assert results[0][2]["id"] == 1

    def test_adapter_add_and_search(self) -> None:
        """Test adding and searching vectors."""
        adapter = VectorSearchAdapter(dimension=5, backend="o1")

        # Add vectors
        v1 = np.array([1, 0, 0, 0, 0])
        v2 = np.array([0, 1, 0, 0, 0])
        v3 = np.array([0, 0, 1, 0, 0])

        adapter.add(v1, {"name": "first"})
        adapter.add(v2, {"name": "second"})
        adapter.add(v3, {"name": "third"})

        # Search
        results = adapter.search(v1, k=2)
        assert len(results) > 0
        assert any(r[1]["name"] == "first" for r in results)

    def test_save_and_load(self) -> None:
        """Test persistence."""
        search = O1VectorSearch(dim=8)

        # Add data
        for i in range(5):
            search.add(np.random.rand(8), {"id": i})

        # Save
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            search.save(temp_path)

            # Load into new instance
            new_search = O1VectorSearch(dim=8)
            new_search.load(temp_path)

            assert len(new_search.vectors) == 5
        finally:
            os.unlink(temp_path)

    def test_batch_operations(self) -> None:
        """Test batch operations."""
        adapter = VectorSearchAdapter(dimension=16, backend="o1")

        # Batch add
        vectors = [np.random.rand(16) for _ in range(10)]
        for i, vec in enumerate(vectors):
            adapter.add(vec, {"batch_id": i})

        # Batch search
        queries = [np.random.rand(16) for _ in range(3)]
        for query in queries:
            results = adapter.search(query, k=3)
            assert len(results) <= 3

    def test_edge_cases(self) -> None:
        """Test edge cases."""
        adapter = VectorSearchAdapter(dimension=4, backend="o1")

        # Empty search
        results = adapter.search(np.array([1, 2, 3, 4]), k=5)
        assert results == []

        # Add zero vector
        adapter.add(np.zeros(4), {"zero": True})

        # Search with k > num_vectors
        adapter.add(np.ones(4), {"ones": True})
        results = adapter.search(np.array([0.5, 0.5, 0.5, 0.5]), k=10)
        assert len(results) <= 2  # Should return at most 2 vectors
