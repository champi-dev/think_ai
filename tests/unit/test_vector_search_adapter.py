"""Unit tests for VectorSearchAdapter."""

import os
import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from vector_search_adapter import VectorSearchAdapter

# Add parent directory to path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


class TestVectorSearchAdapter:
    """Test VectorSearchAdapter functionality."""

    @pytest.fixture
    def mock_faiss(self):
        """Mock FAISS module."""
        with patch.dict("sys.modules", {"faiss": MagicMock()}):
            yield

    @pytest.fixture
    def mock_annoy(self):
        """Mock Annoy module."""
        with patch.dict("sys.modules", {"annoy": MagicMock()}):
            yield

    def test_auto_backend_selection_faiss(self, mock_faiss) -> None:
        """Test automatic selection of FAISS when available."""
        with patch("vector_search_adapter.FAISS_AVAILABLE", True):
            with patch("vector_search_adapter.ANNOY_AVAILABLE", True):
                adapter = VectorSearchAdapter(dimension=128)
                assert adapter.backend == "faiss"

    def test_auto_backend_selection_annoy(self, mock_annoy) -> None:
        """Test fallback to Annoy when FAISS not available."""
        with patch("vector_search_adapter.FAISS_AVAILABLE", False):
            with patch("vector_search_adapter.ANNOY_AVAILABLE", True):
                adapter = VectorSearchAdapter(dimension=128)
                assert adapter.backend == "annoy"

    def test_auto_backend_selection_o1(self) -> None:
        """Test fallback to O(1) when neither FAISS nor Annoy available."""
        with patch("vector_search_adapter.FAISS_AVAILABLE", False):
            with patch("vector_search_adapter.ANNOY_AVAILABLE", False):
                adapter = VectorSearchAdapter(dimension=128)
                assert adapter.backend == "o1"

    def test_force_backend_selection(self) -> None:
        """Test forcing specific backend."""
        adapter = VectorSearchAdapter(dimension=128, backend="o1")
        assert adapter.backend == "o1"

    def test_add_vector(self) -> None:
        """Test adding vectors."""
        adapter = VectorSearchAdapter(dimension=3, backend="o1")
        vector = np.array([1.0, 2.0, 3.0])
        metadata = {"id": 1, "text": "test"}

        idx = adapter.add(vector, metadata)
        assert idx == 0
        assert len(adapter.vectors) == 1

    def test_search_empty_index(self) -> None:
        """Test searching empty index."""
        adapter = VectorSearchAdapter(dimension=3, backend="o1")
        query = np.array([1.0, 2.0, 3.0])

        results = adapter.search(query, k=5)
        assert results == []

    def test_search_with_results(self) -> None:
        """Test searching with results."""
        adapter = VectorSearchAdapter(dimension=3, backend="o1")

        # Add some vectors
        vectors = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([0.0, 0.0, 1.0]),
        ]

        for i, vec in enumerate(vectors):
            adapter.add(vec, {"id": i})

        # Search for similar to first vector
        query = np.array([1.0, 0.1, 0.1])
        results = adapter.search(query, k=2)

        assert len(results) <= 2
        assert all(isinstance(r[0], float) for r in results)  # scores
        assert all(isinstance(r[1], dict) for r in results)  # metadata

    def test_get_backend_info(self) -> None:
        """Test getting backend information."""
        adapter = VectorSearchAdapter(dimension=128, backend="o1")
        info = adapter.get_backend_info()

        assert info["backend"] == "o1"
        assert info["dimension"] == 128
        assert "num_vectors" in info
        assert isinstance(info["faiss_available"], bool)
        assert isinstance(info["annoy_available"], bool)

    @pytest.mark.parametrize("dimension", [64, 128, 384, 768])
    def test_various_dimensions(self, dimension) -> None:
        """Test adapter with various dimensions."""
        adapter = VectorSearchAdapter(dimension=dimension, backend="o1")
        vector = np.random.rand(dimension)

        idx = adapter.add(vector, {"test": True})
        assert idx == 0

        results = adapter.search(vector, k=1)
        assert len(results) == 1

    def test_normalization(self) -> None:
        """Test vector normalization."""
        adapter = VectorSearchAdapter(dimension=3, backend="o1")

        # Add unnormalized vector
        vector = np.array([3.0, 4.0, 0.0])  # magnitude = 5
        adapter.add(vector, {"id": 1})

        # Search should work with normalization
        results = adapter.search(vector, k=1)
        assert len(results) == 1
        assert results[0][0] > 0.9  # High similarity with itself

    def test_edge_cases(self) -> None:
        """Test edge cases."""
        adapter = VectorSearchAdapter(dimension=3, backend="o1")

        # Test with zero vector
        zero_vector = np.zeros(3)
        idx = adapter.add(zero_vector, {"zero": True})
        assert idx == 0

        # Test k larger than index size
        results = adapter.search(zero_vector, k=100)
        assert len(results) <= 1

        # Test with negative k (should handle gracefully)
        results = adapter.search(zero_vector, k=-1)
        assert results == []
