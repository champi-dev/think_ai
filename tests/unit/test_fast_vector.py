"""Fast vector search tests"""

import os
import sys

import lz4.frame
import time
from o1_vector_search import O1VectorSearch
from vector_search_adapter import VectorSearchAdapter
import numpy as np

sys.path.insert(
    0, os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))


class TestFastVector:
    """Optimized vector tests"""

    def test_init_performance(self):
        """Test initialization is fast"""
        start = time.time()
        VectorSearchAdapter(dimension=128, backend="o1")
        elapsed = time.time() - start
        assert elapsed < 0.1  # Should init in under 100ms

    def test_batch_operations(self):
        """Test batch operations work"""
        search = O1VectorSearch(dim=64)

        # Batch add
        vectors = np.random.rand(100, 64)
        for i, vec in enumerate(vectors):
            search.add(vec, {"id": i})

        # Batch search
        queries = np.random.rand(10, 64)
        for query in queries:
            results = search.search(query, k=5)
            assert len(results) <= 5

    def test_compression(self):
        """Test data compression"""

        # Generate test data
        data = np.random.rand(1000, 128).tobytes()

        # Compress
        compressed = lz4.frame.compress(data)
        ratio = len(compressed) / len(data)

        assert ratio < 0.9  # Should achieve some compression

        # Decompress and verify
        decompressed = lz4.frame.decompress(compressed)
        assert decompressed == data
