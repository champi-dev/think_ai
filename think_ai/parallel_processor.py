"""Parallel processing system that ensures all libraries use full CPU/GPU resources.
Implements work stealing and dynamic load balancing for O(1) task distribution.
"""

import asyncio
import concurrent.futures
import multiprocessing as mp
import queue
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from multiprocessing import shared_memory
from typing import Any

import numpy as np
import psutil
import torch
import torch.multiprocessing as torch_mp

# Enable multiprocessing optimizations
torch_mp.set_start_method("spawn", force=True)
mp.set_start_method("spawn", force=True)


@dataclass
class TaskResult:
    """Result of a parallel task execution."""

    task_id: str
    result: Any
    execution_time: float
    worker_id: int


class ParallelProcessor:
    """High-performance parallel processor that maximizes system utilization.
    Uses work stealing and dynamic scheduling for O(1) task distribution.
    """

    def __init__(self, num_workers: int | None = None) -> None:
        self.num_workers = num_workers or mp.cpu_count()

        # Safe GPU detection with fallback
        try:
            self.gpu_available = torch.cuda.is_available()
            self.gpu_count = torch.cuda.device_count() if self.gpu_available else 0
        except Exception:
            # Fallback for environments with GPU library issues
            self.gpu_available = False
            self.gpu_count = 0

        # Thread pool for I/O bound tasks
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.num_workers * 2,
            thread_name_prefix="think-ai-io",
        )

        # Process pool for CPU bound tasks
        self.process_pool = concurrent.futures.ProcessPoolExecutor(
            max_workers=self.num_workers,
            mp_context=mp.get_context("spawn"),
        )

        # Async event loop for coroutines
        self.loop = asyncio.new_event_loop()
        self.async_thread = threading.Thread(
            target=self._run_event_loop, daemon=True)
        self.async_thread.start()

        # Work stealing queues
        self.task_queues = [queue.Queue() for _ in range(self.num_workers)]
        self.result_queue = queue.Queue()

        # Shared memory for zero-copy data transfer
        self.shared_buffers = {}

        # Start worker threads
        self.workers = []
        for i in range(self.num_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                args=(i,),
                daemon=True,
            )
            worker.start()
            self.workers.append(worker)

    def _run_event_loop(self) -> None:
        """Run the async event loop in a separate thread."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _worker_loop(self, worker_id: int) -> None:
        """Worker loop with work stealing."""
        my_queue = self.task_queues[worker_id]

        while True:
            # Try to get task from own queue
            try:
                task = my_queue.get(timeout=0.001)
            except queue.Empty:
                # Steal from other queues
                for i in range(self.num_workers):
                    if i != worker_id:
                        try:
                            task = self.task_queues[i].get_nowait()
                            break
                        except queue.Empty:
                            continue
                else:
                    time.sleep(0.001)
                    continue

            # Execute task
            if task is None:  # Shutdown signal
                break

            task_id, func, args, kwargs = task
            start_time = time.time()

            try:
                # Set CPU affinity for this worker
                p = psutil.Process()
                p.cpu_affinity([worker_id % mp.cpu_count()])

                # Execute based on function type
                if asyncio.iscoroutinefunction(func):
                    future = asyncio.run_coroutine_threadsafe(
                        func(*args, **kwargs),
                        self.loop,
                    )
                    result = future.result()
                else:
                    result = func(*args, **kwargs)

                execution_time = time.time() - start_time
                self.result_queue.put(
                    TaskResult(
                        task_id=task_id,
                        result=result,
                        execution_time=execution_time,
                        worker_id=worker_id,
                    )
                )
            except Exception as e:
                self.result_queue.put(
                    TaskResult(
                        task_id=task_id,
                        result=e,
                        execution_time=time.time() - start_time,
                        worker_id=worker_id,
                    )
                )

    def map_parallel(
        self, func: Callable, items: list[Any], batch_size: int | None = None
    ) -> list[Any]:
        """Map function over items in parallel with automatic batching.
        Uses work stealing for optimal load balancing.
        """
        if not items:
            return []

        # Determine optimal batch size
        if batch_size is None:
            batch_size = max(1, len(items) // (self.num_workers * 4))

        # Create tasks
        tasks = []
        for i in range(0, len(items), batch_size):
            batch = items[i: i + batch_size]
            task_id = f"batch_{i}_{i + batch_size}"

            # Wrap function to process batch
            def batch_func(batch_items=batch):
                return [func(item) for item in batch_items]

            tasks.append((task_id, batch_func, (), {}))

        # Distribute tasks across queues (round-robin)
        for i, task in enumerate(tasks):
            self.task_queues[i % self.num_workers].put(task)

        # Collect results
        results = {}
        for _ in range(len(tasks)):
            task_result = self.result_queue.get()
            if isinstance(task_result.result, Exception):
                raise task_result.result
            results[task_result.task_id] = task_result.result

        # Flatten results in order
        final_results = []
        for i in range(0, len(items), batch_size):
            task_id = f"batch_{i}_{i + batch_size}"
            final_results.extend(results[task_id])

        return final_results[: len(items)]

    def parallel_gpu_map(
        self, func: Callable, tensors: list[torch.Tensor]
    ) -> list[torch.Tensor]:
        """Map function over tensors using all available GPUs.
        Implements data parallelism with automatic device assignment.
        """
        if not self.gpu_available or not tensors:
            return self.map_parallel(func, tensors)

        # Distribute tensors across GPUs
        device_assignments = [i % self.gpu_count for i in range(len(tensors))]

        def gpu_wrapper(tensor, device_id):
            device = torch.device(f"cuda:{device_id}")
            tensor = tensor.to(device)
            with torch.cuda.device(device):
                result = func(tensor)
            return result.cpu()

        # Process in parallel
        futures = []
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.gpu_count
        ) as executor:
            for tensor, device_id in zip(
                    tensors, device_assignments, strict=False):
                future = executor.submit(gpu_wrapper, tensor, device_id)
                futures.append(future)

        return [future.result() for future in futures]

    def create_shared_array(
        self, shape: tuple, dtype: np.dtype = np.float32
    ) -> np.ndarray:
        """Create a shared memory array for zero-copy data transfer between processes."""
        size = np.prod(shape) * np.dtype(dtype).itemsize
        shm = shared_memory.SharedMemory(create=True, size=size)
        self.shared_buffers[shm.name] = shm

        # Create numpy array backed by shared memory
        array = np.ndarray(shape, dtype=dtype, buffer=shm.buf)
        array._shm_name = shm.name  # Store reference

        return array

    def parallel_reduce(
        self, func: Callable, items: list[Any], initializer: Any = None
    ) -> Any:
        """Parallel reduction with work stealing.
        Implements tree-based reduction for O(log n) complexity.
        """
        if not items:
            return initializer

        if len(items) == 1:
            return items[0] if initializer is None else func(
                initializer, items[0])

        # Tree-based reduction
        while len(items) > 1:
            # Pair up items
            pairs = []
            for i in range(0, len(items), 2):
                if i + 1 < len(items):
                    pairs.append((items[i], items[i + 1]))
                else:
                    pairs.append((items[i],))

            # Reduce pairs in parallel
            def reduce_pair(pair):
                if len(pair) == 1:
                    return pair[0]
                return func(pair[0], pair[1])

            items = self.map_parallel(reduce_pair, pairs)

        result = items[0]
        if initializer is not None:
            result = func(initializer, result)

        return result

    def parallel_pipeline(
            self,
            stages: list[Callable],
            items: list[Any]) -> list[Any]:
        """Execute pipeline stages in parallel with streaming.
        Each stage processes items as they become available.
        """
        if not stages or not items:
            return items

        # Create queues between stages
        queues = [queue.Queue() for _ in range(len(stages) + 1)]

        # Put initial items
        for item in items:
            queues[0].put(item)
        queues[0].put(None)  # End marker

        # Stage workers
        def stage_worker(stage_idx, stage_func) -> None:
            in_queue = queues[stage_idx]
            out_queue = queues[stage_idx + 1]

            while True:
                item = in_queue.get()
                if item is None:
                    out_task_task_queue.put(None)
                    break

                result = stage_func(item)
                out_queue.put(result)

        # Start stage threads
        threads = []
        for i, stage in enumerate(stages):
            thread = threading.Thread(
                target=stage_worker,
                args=(i, stage),
                daemon=True,
            )
            thread.start()
            threads.append(thread)

        # Collect results
        results = []
        while True:
            item = queues[-1].get()
            if item is None:
                break
            results.append(item)

        # Wait for threads
        for thread in threads:
            thread.join()

        return results

    def shutdown(self) -> None:
        """Gracefully shutdown all workers and pools."""
        # Stop workers
        for _task_queue in self.task_queues:
            task_task_queue.put(None)

        for worker in self.workers:
            worker.join()

        # Shutdown pools
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)

        # Stop event loop
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.async_thread.join()

        # Clean up shared memory
        for shm in self.shared_buffers.values():
            shm.close()
            shm.unlink()


# Global processor instance
parallel_processor = ParallelProcessor()


# Decorator for automatic parallelization
def parallelize(batch_size: int | None = None):
    """Decorator to automatically parallelize function calls."""

    def decorator(func):
        @wraps(func)
        def wrapper(items):
            if isinstance(items, (list, tuple)):
                return parallel_processor.map_parallel(func, items, batch_size)
            return func(items)

        return wrapper

    return decorator


__all__ = [
    "ParallelProcessor",
    "TaskResult",
    "parallel_processor",
    "parallelize"]
