#!/usr/bin/env python3

"""Background Worker for Think AI
Handles parallel processing of vector operations.
"""

import asyncio
import multiprocessing
import queue
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

from vector_search_adapter import VectorSearchAdapter


class BackgroundWorker:
    """Background worker for parallel processing."""

    def __init__(self, num_workers: Optional[int] = None) -> None:
        """Initialize background worker with parallel processing."""
        self.num_workers = num_workers or multiprocessing.cpu_count()
        self.task_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()
        self.workers = []
        self.running = False

        # Initialize in main process
        torch.set_default_device("cpu")

    def start(self) -> None:
        """Start background workers."""
        self.running = True

        # Start worker processes
        for i in range(self.num_workers):
            worker = multiprocessing.Process(
                target=self._worker_loop,
                args=(i, self.task_queue, self.result_queue),
            )
            worker.start()
            self.workers.append(worker)

    def stop(self) -> None:
        """Stop all workers."""
        self.running = False

        # Send stop signal to all workers
        for _ in range(self.num_workers):
            self.task_queue.put(None)

        # Wait for workers to finish
        for worker in self.workers:
            worker.join()

    def _worker_loop(
        self, worker_id: int, task_queue: multiprocessing.Queue, result_queue: multiprocessing.Queue
    ) -> None:
        """Worker process loop."""
        # Initialize per-worker resources
        torch.set_default_device("cpu")
        model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        vector_db = VectorSearchAdapter(384)

        while True:
            task = task_queue.get()
            if task is None:
                break

            try:
                result = self._process_task(task, model, vector_db)
                result_queue.put(
                    {
                        "task_id": task["id"],
                        "status": "success",
                        "result": result,
                    }
                )
            except Exception as e:
                result_queue.put(
                    {
                        "task_id": task["id"],
                        "status": "error",
                        "error": str(e),
                    }
                )

    def _process_task(self, task: Dict, model, vector_db) -> Any:
        """Process individual task."""
        task_type = task["type"]

        if task_type == "encode":
            # Batch encoding
            texts = task["texts"]
            embeddings = model.encode(texts)
            return embeddings.tolist()

        if task_type == "index":
            # Add documents to index
            documents = task["documents"]
            for doc in documents:
                embedding = model.encode(doc["content"])
                vector_db.add(embedding, doc)
            return {"indexed": len(documents)}

        if task_type == "search":
            # Parallel search
            queries = task["queries"]
            results = []
            for query in queries:
                embedding = model.encode(query)
                search_results = vector_db.search(embedding, k=task.get("k", 5))
                results.append(search_results)
            return results

        if task_type == "analyze":
            # Code analysis
            code = task["code"]
            # Simulate analysis
            return {
                "lines": code.count("\n") + 1,
                "complexity": len(code) // 100,
                "issues": [],
            }

        msg = f"Unknown task type: {task_type}"
        raise ValueError(msg)

    def submit_task(self, task: Dict) -> str:
        """Submit task for background processing."""
        task_id = f"task_{int(time.time() * 1000)}"
        task["id"] = task_id
        self.task_queue.put(task)
        return task_id

    def get_result(self, timeout: Optional[float] = None) -> Optional[Dict]:
        """Get result from completed tasks."""
        try:
            return self.result_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    async def batch_encode_async(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Asynchronously encode texts in batches."""
        loop = asyncio.get_event_loop()

        # Split into batches
        batches = [texts[i : i + batch_size] for i in range(0, len(texts), batch_size)]

        # Submit all batches
        task_ids = []
        for batch in batches:
            task = {"type": "encode", "texts": batch}
            task_id = self.submit_task(task)
            task_ids.append(task_id)

        # Collect results
        results = []
        for _ in task_ids:
            result = await loop.run_in_executor(None, self.get_result, 10.0)
            if result and result["status"] == "success":
                results.extend(result["result"])

        return results


class ParallelVectorDB:
    """Parallel vector database with distributed operations."""

    def __init__(self, dimension: int = 384, num_workers: int = 4):
        """Initialize parallel vector database."""
        self.dimension = dimension
        self.num_workers = num_workers
        self.worker = BackgroundWorker(num_workers)
        self.worker.start()
        self.cache = {}  # Add cache attribute for tests

    def add_batch(self, embeddings: np.ndarray, metadata: List[Dict]) -> None:
        """Add batch of embeddings with metadata."""
        documents = []
        for i, (emb, meta) in enumerate(zip(embeddings, metadata)):
            documents.append(
                {"content": meta.get("content", ""), "embedding": emb.tolist(), "id": meta.get("id", i), **meta}
            )

        task = {"type": "index", "documents": documents}
        self.worker.submit_task(task)

    def parallel_index(self, documents: List[Dict], batch_size: int = 100) -> None:
        """Index documents in parallel batches."""
        # Split documents into batches
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            task = {"type": "index", "documents": batch}
            self.worker.submit_task(task)
            # Get result to ensure completion
            self.worker.get_result(timeout=10.0)

    def parallel_search(self, queries: List[str], k: int = 5) -> List[List[Tuple[float, Dict]]]:
        """Search for multiple queries in parallel."""
        task = {"type": "search", "queries": queries, "k": k}
        task_id = self.worker.submit_task(task)

        # Wait for result
        timeout = 10.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.worker.get_result(timeout=0.1)
            if result and result.get("task_id") == task_id:
                # Check if status is explicitly set to error/failure
                if result.get("status") == "error":
                    raise RuntimeError(f"Search failed: {result.get('error')}")
                # Otherwise, assume success if result is present
                return result.get("result", [])

        raise TimeoutError("Search timed out")

    def search_batch(self, queries: List[str], k: int = 5) -> List[List[Dict]]:
        """Search for multiple queries in parallel (alias for parallel_search)."""
        return self.parallel_search(queries, k)

    def shutdown(self) -> None:
        """Shutdown the parallel vector database."""
        self.worker.stop()

    def close(self) -> None:
        """Close the parallel vector database (alias for shutdown)."""
        self.shutdown()
