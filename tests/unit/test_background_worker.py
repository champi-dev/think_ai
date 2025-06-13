"""Unit tests for BackgroundWorker."""

import os
import sys
from unittest.mock import Mock, patch

import numpy as np
import pytest

from background_worker import BackgroundWorker, ParallelVectorDB

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


class TestBackgroundWorker:
    """Test BackgroundWorker functionality."""

    @pytest.fixture
    def worker(self):
        """Create a test worker with minimal processes."""
        worker = BackgroundWorker(num_workers=2)
        yield worker
        # Cleanup
        if worker.running:
            worker.stop()

    def test_initialization(self) -> None:
        """Test BackgroundWorker initialization."""
        worker = BackgroundWorker(num_workers=2)

        assert worker.num_workers == 2
        assert not worker.running
        assert len(worker.workers) == 0

    @patch("background_worker.multiprocessing.Process")
    def test_start_workers(self, mock_process) -> None:
        """Test starting workers."""
        mock_proc_instance = Mock()
        mock_process.return_value = mock_proc_instance

        worker = BackgroundWorker(num_workers=2)
        worker.start()

        assert worker.running
        assert len(worker.workers) == 2
        assert mock_process.call_count == 2
        assert mock_proc_instance.start.call_count == 2

    def test_submit_task(self, worker) -> None:
        """Test submitting tasks."""
        task = {
            "type": "encode",
            "texts": ["test1", "test2"],
        }

        task_id = worker.submit_task(task)

        assert task_id.startswith("task_")
        assert "id" in task

    def test_get_result_timeout(self, worker) -> None:
        """Test getting result with timeout."""
        result = worker.get_result(timeout=0.1)
        assert result is None

    @patch("background_worker.SentenceTransformer")
    def test_process_encode_task(self, mock_model, worker) -> None:
        """Test processing encode task."""
        mock_model_instance = Mock()
        mock_model_instance.encode.return_value = np.array([[1.0, 2.0], [3.0, 4.0]])
        mock_model.return_value = mock_model_instance

        task = {
            "type": "encode",
            "texts": ["text1", "text2"],
        }

        # Create mock vector db
        mock_vector_db = Mock()

        result = worker._process_task(task, mock_model_instance, mock_vector_db)

        assert isinstance(result, list)
        assert len(result) == 2
        mock_model_instance.encode.assert_called_once_with(["text1", "text2"])

    @patch("background_worker.SentenceTransformer")
    def test_process_index_task(self, mock_model, worker) -> None:
        """Test processing index task."""
        mock_model_instance = Mock()
        mock_model_instance.encode.return_value = np.array([1.0, 2.0, 3.0])
        mock_model.return_value = mock_model_instance

        mock_vector_db = Mock()

        task = {
            "type": "index",
            "documents": [
                {"content": "doc1", "id": 1},
                {"content": "doc2", "id": 2},
            ],
        }

        result = worker._process_task(task, mock_model_instance, mock_vector_db)

        assert result == {"indexed": 2}
        assert mock_model_instance.encode.call_count == 2
        assert mock_vector_db.add.call_count == 2

    def test_process_unknown_task(self, worker) -> None:
        """Test processing unknown task type."""
        task = {"type": "unknown"}
        mock_model = Mock()
        mock_vector_db = Mock()

        with pytest.raises(ValueError, match="Unknown task type"):
            worker._process_task(task, mock_model, mock_vector_db)

    @pytest.mark.asyncio
    async def test_batch_encode_async(self, worker) -> None:
        """Test async batch encoding."""
        # Mock the worker methods
        worker.submit_task = Mock(side_effect=lambda x: f"task_{x['texts'][0]}")
        worker.get_result = Mock(
            side_effect=[
                {"task_id": "task_batch1", "status": "success", "result": [[1.0, 2.0]]},
                {"task_id": "task_batch2", "status": "success", "result": [[3.0, 4.0]]},
            ]
        )

        texts = ["batch1", "batch2"]
        results = await worker.batch_encode_async(texts, batch_size=1)

        assert len(results) == 2
        assert results == [[1.0, 2.0], [3.0, 4.0]]


class TestParallelVectorDB:
    """Test ParallelVectorDB functionality."""

    @pytest.fixture
    def parallel_db(self):
        """Create a test parallel vector DB."""
        with patch("background_worker.BackgroundWorker"):
            db = ParallelVectorDB(dimension=128, num_workers=2)
            yield db
            db.shutdown()

    def test_initialization(self) -> None:
        """Test ParallelVectorDB initialization."""
        with patch("background_worker.BackgroundWorker") as mock_worker:
            db = ParallelVectorDB(dimension=128, num_workers=2)

            assert db.dimension == 128
            assert db.cache == {}
            mock_worker.assert_called_once_with(2)

    def test_parallel_index(self, parallel_db) -> None:
        """Test parallel indexing."""
        documents = [{"id": f"doc_{i}", "content": f"content_{i}"} for i in range(10)]

        # Mock worker methods
        parallel_db.worker.submit_task = Mock(
            side_effect=lambda x: f"task_{len(x['documents'])}"
        )
        parallel_db.worker.get_result = Mock(return_value={"status": "success"})

        parallel_db.parallel_index(documents, batch_size=5)

        assert parallel_db.worker.submit_task.call_count == 2  # 10 docs / 5 batch_size
        assert parallel_db.worker.get_result.call_count == 2

    def test_parallel_search(self, parallel_db) -> None:
        """Test parallel search."""
        queries = ["query1", "query2", "query3"]

        # Mock worker methods
        parallel_db.worker.submit_task = Mock(return_value="task_123")
        parallel_db.worker.get_result = Mock(
            return_value={
                "task_id": "task_123",
                "result": [[(0.9, {"id": 1})], [(0.8, {"id": 2})], [(0.7, {"id": 3})]],
            }
        )

        results = parallel_db.parallel_search(queries, k=1)

        assert len(results) == 3
        parallel_db.worker.submit_task.assert_called_once()

    def test_shutdown(self, parallel_db) -> None:
        """Test shutdown."""
        parallel_db.worker.stop = Mock()

        parallel_db.shutdown()

        parallel_db.worker.stop.assert_called_once()
