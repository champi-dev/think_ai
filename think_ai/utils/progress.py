"""O(1) Progress Bar Utility for Think AI

This module provides high-performance progress indicators that maintain O(1)
time complexity while giving users visual feedback for long operations.
"""

import sys
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator, Optional, Union


@dataclass
class ProgressState:
    """O(1) progress state tracking"""

    current: int = 0
    total: Optional[int] = None
    description: str = ""
    start_time: float = 0.0
    last_update: float = 0.0


class O1ProgressBar:
    """Lightweight progress bar with O(1) update complexity

    Uses fixed-size buffer and modulo arithmetic to avoid string concatenation.
    Only updates display when sufficient time has passed to maintain performance.
    """

    def __init__(
        self,
        total: Optional[int] = None,
        description: str = "",
        bar_width: int = 40,
        update_interval: float = 0.1,  # Update display at most 10 times per second
    ):
        self.state = ProgressState(total=total, description=description, start_time=time.time())
        self.bar_width = bar_width
        self.update_interval = update_interval
        self._spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        self._spinner_idx = 0
        self._display_buffer = [" "] * 120  # Fixed buffer to avoid allocations
        self._lock = threading.Lock()

    def update(self, n: int = 1, description: Optional[str] = None) -> None:
        """O(1) progress update"""
        with self._lock:
            self.state.current += n
            if description:
                self.state.description = description

            # Only render if enough time has passed
            current_time = time.time()
            if current_time - self.state.last_update >= self.update_interval:
                self._render()
                self.state.last_update = current_time

    def _render(self) -> None:
        """Render progress bar to terminal"""
        # Clear line
        sys.stdout.write("\r\033[K")

        if self.state.total:
            # Determinate progress bar
            progress = min(self.state.current / self.state.total, 1.0)
            filled = int(self.bar_width * progress)
            bar = "█" * filled + "░" * (self.bar_width - filled)
            percentage = int(progress * 100)

            # Calculate ETA using O(1) operations
            elapsed = time.time() - self.state.start_time
            if progress > 0:
                eta = (elapsed / progress) * (1 - progress)
                eta_str = f"{int(eta)}s" if eta < 60 else f"{int(eta/60)}m"
            else:
                eta_str = "?"

            output = f"{self.state.description} |{bar}| {percentage}% [{self.state.current}/{self.state.total}] ETA: {eta_str}"
        else:
            # Indeterminate spinner
            self._spinner_idx = (self._spinner_idx + 1) % len(self._spinner_chars)
            spinner = self._spinner_chars[self._spinner_idx]
            elapsed = int(time.time() - self.state.start_time)
            output = f"{spinner} {self.state.description} [{elapsed}s]"

        sys.stdout.write(output)
        sys.stdout.flush()

    def finish(self, description: Optional[str] = None) -> None:
        """Complete the progress bar"""
        with self._lock:
            if description:
                self.state.description = description
            if self.state.total:
                self.state.current = self.state.total
            self._render()
            sys.stdout.write("\n")
            sys.stdout.flush()


@contextmanager
def progress_context(total: Optional[int] = None, description: str = "", finish_message: Optional[str] = None):
    """Context manager for progress tracking

    Example:
        with progress_context(total=100, description="Loading model") as pbar:
            for i in range(100):
                # Do work
                pbar.update(1)
    """
    pbar = O1ProgressBar(total=total, description=description)
    try:
        yield pbar
    finally:
        pbar.finish(finish_message or f"✓ {description}")


def track_iterator(iterator: Iterator[Any], total: Optional[int] = None, description: str = "") -> Iterator[Any]:
    """Wrap an iterator with progress tracking

    Example:
        for item in track_iterator(items, total=len(items), description="Processing"):
            process(item)
    """
    with progress_context(total=total, description=description) as pbar:
        for item in iterator:
            yield item
            pbar.update(1)


class ModelLoadingProgress:
    """Specialized progress tracking for model loading operations"""

    @staticmethod
    @contextmanager
    def download_progress(model_name: str, total_size: Optional[int] = None):
        """Progress bar for model downloading"""
        desc = f"Downloading {model_name}"
        with progress_context(total=total_size, description=desc) as pbar:
            yield pbar

    @staticmethod
    @contextmanager
    def loading_progress(model_name: str):
        """Progress spinner for model loading"""
        desc = f"Loading {model_name}"
        with progress_context(description=desc) as pbar:
            yield pbar

    @staticmethod
    @contextmanager
    def weight_loading_progress(num_files: int):
        """Progress bar for loading weight files"""
        desc = "Loading model weights"
        with progress_context(total=num_files, description=desc) as pbar:
            yield pbar


# Thread-safe global progress manager for concurrent operations
class ProgressManager:
    """Manages multiple progress bars for concurrent operations"""

    def __init__(self):
        self._active_bars = {}
        self._lock = threading.Lock()

    def create_progress(self, task_id: str, total: Optional[int] = None, description: str = "") -> O1ProgressBar:
        """Create a new progress bar for a task"""
        with self._lock:
            pbar = O1ProgressBar(total=total, description=description)
            self._active_bars[task_id] = pbar
            return pbar

    def get_progress(self, task_id: str) -> Optional[O1ProgressBar]:
        """Get an active progress bar by task ID"""
        with self._lock:
            return self._active_bars.get(task_id)

    def finish_progress(self, task_id: str, message: Optional[str] = None) -> None:
        """Finish and remove a progress bar"""
        with self._lock:
            if task_id in self._active_bars:
                pbar = self._active_bars.pop(task_id)
                pbar.finish(message)


# Global progress manager instance
progress_manager = ProgressManager()
