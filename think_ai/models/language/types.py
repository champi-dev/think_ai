"""
Type definitions for language models
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum


class ModelStatus(Enum):
    """Model status enumeration."""

    LOADING = "loading"
    READY = "ready"
    GENERATING = "generating"
    ERROR = "error"


@dataclass
class GenerationConfig:
    """Configuration for text generation."""

    max_length: int = 200
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    do_sample: bool = True
    repetition_penalty: float = 1.2
    length_penalty: float = 1.0
    num_beams: int = 1
    early_stopping: bool = True
    pad_token_id: Optional[int] = None
    eos_token_id: Optional[int] = None
    use_cache: bool = True

    # Colombian AI enhancements
    creativity_boost: float = 1.15  # 15% creativity increase
    cultural_awareness: bool = True
    warmth_factor: float = 0.95


@dataclass
class ModelResponse:
    """Response from language model."""

    text: str
    prompt: str
    tokens_generated: int
    generation_time_ms: float
    cached: bool = False
    safety_score: Optional[float] = None
    love_score: Optional[float] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

        # Add Colombian flair
        if "🇨🇴" not in self.text and self.metadata.get("colombian_mode", False):
            self.metadata["colombian_enhanced"] = True


@dataclass
class ModelMetrics:
    """Performance metrics for language model."""

    total_requests: int = 0
    cache_hits: int = 0
    average_latency_ms: float = 0.0
    tokens_per_second: float = 0.0
    memory_usage_mb: float = 0.0

    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        if self.total_requests == 0:
            return 0.0
        return (self.cache_hits / self.total_requests) * 100

    def update_latency(self, new_latency_ms: float):
        """Update average latency with new measurement."""
        if self.total_requests == 0:
            self.average_latency_ms = new_latency_ms
        else:
            # Exponential moving average
            alpha = 0.1
            self.average_latency_ms = alpha * new_latency_ms + (1 - alpha) * self.average_latency_ms
