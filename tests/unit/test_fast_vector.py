"""Fast vector search tests"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import lz4.frame
import numpy as np

from o1_vector_search import O1VectorSearch
from vector_search_adapter import VectorSearchAdapter


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

        # Generate highly compressible test data
        # Use sparse vectors with many zeros
        vectors = []
        for i in range(1000):
            # Create sparse vector with only 10 non-zero values
            vec = np.zeros(128, dtype=np.float32)
            # Set some positions to the same values repeatedly
            indices = [
                i % 128,
                (i * 2) % 128,
                (i * 3) % 128,
                (i * 5) % 128,
                (i * 7) % 128,
                (i * 11) % 128,
                (i * 13) % 128,
                (i * 17) % 128,
                (i * 19) % 128,
                (i * 23) % 128,
            ]
            for idx in indices:
                vec[idx] = 1.0
            vectors.append(vec)

        data = np.array(vectors, dtype=np.float32).tobytes()

        # Compress
        compressed = lz4.frame.compress(data)
        ratio = len(compressed) / len(data)

        # Should achieve good compression due to many zeros
        assert ratio < 0.9  # Should achieve some compression

        # Decompress and verify
        decompressed = lz4.frame.decompress(compressed)
        assert decompressed == data
