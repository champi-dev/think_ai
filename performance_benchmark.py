#! / usr / bin / env python3

"""Performance benchmark showing real - world vector database performance."""

import time

import faiss
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

# Force CPU usage
torch.set_default_device("cpu")

# System info

# Initialize model
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

# Generate test data
test_sizes = [100, 1000, 10000, 50000]
documents = []

# Real - world - like documents
templates = [
"The {} algorithm is used for {} in machine learning applications",
"Database systems optimize {} operations using {} techniques",
"Neural networks process {} data through {} layers of computation",
"Vector search enables {} similarity matching with {} performance",
"Cloud computing provides {} resources for {} workloads",
]

for i in range(max(test_sizes)):
    template = templates[i % len(templates)]
    doc = template.format(f"advanced-{i}", f"optimization-{i}")
    documents.append(doc)

# Benchmark different scales
    for size in test_sizes:

        subset_docs = documents[:size]

# Encoding benchmark
        start = time.time()
        embeddings = model.encode(subset_docs, show_progress_bar=False)
        encoding_time = time.time() - start

# FAISS indexing
        start = time.time()
        index = faiss.IndexFlatIP(embeddings.shape[1])
        faiss.normalize_L2(embeddings)
        index.add(embeddings.astype("float32"))
        indexing_time = time.time() - start

# Search benchmark
        queries = [
        "machine learning optimization",
        "database performance",
        "neural network architecture"]
        query_embeddings = model.encode(queries, show_progress_bar=False)
        faiss.normalize_L2(query_embeddings)

# Single query
        start = time.time()
        D, I = index.search(query_embeddings[0:1].astype("float32"), 10)
        single_time = time.time() - start

# Batch queries
        num_queries = 1000
        batch_queries = np.repeat(query_embeddings, num_queries / / 3, axis=0)

        start = time.time()
        D, I = index.search(batch_queries.astype("float32"), 10)
        batch_time = time.time() - start

# Memory usage
        index_size = index.ntotal * index.d * 4 / (1024 * * 2)  # MB

# Advanced FAISS features

# Test different index types
        embeddings = model.encode(documents[:10000])
        faiss.normalize_L2(embeddings)

        index_types = [
        ("Flat (exact search)",
        faiss.IndexFlatIP(384)),
        ("IVF (approximate)",
        faiss.index_factory(
        384,
        "IVF100, Flat",
        faiss.METRIC_INNER_PRODUCT)),
        ("HNSW (graph - based)",
        faiss.IndexHNSWFlat(
        384,
        32,
        faiss.METRIC_INNER_PRODUCT)),
        ]

        for _name, index in index_types:
            if hasattr(index, "train") and not index.is_trained:
                index.train(embeddings.astype("float32"))

                start = time.time()
                index.add(embeddings.astype("float32"))
                add_time = time.time() - start

                query = query_embeddings[0:1].astype("float32")

# Warmup
                index.search(query, 10)

# Benchmark
                start = time.time()
                for _ in range(100):
                    D, I = index.search(query, 10)
                    search_time = (time.time() - start) / 100
