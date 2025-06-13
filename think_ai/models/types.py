"""
Think AI Model Types and Configurations
Shared types to avoid circular imports
"""

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class GenerationConfig:
    """Configuration for text generation."""

    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    do_sample: bool = True
    stream: bool = False

    def get_valid_generation_params(self) -> Dict[str, Any]:
        """Return only valid generation parameters based on configuration.

        O(1) complexity using direct attribute access and conditional logic.
        """
        # Always include these core parameters
        params = {
            "max_new_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "repetition_penalty": self.repetition_penalty,
            "do_sample": self.do_sample,
        }

        return params


@dataclass
class ModelResponse:
    """Response from a language model."""

    text: str
    tokens_generated: int = 0
    generation_time: float = 0.0
    model_name: str = ""
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Initialize metadata if not provided."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ModelInstance:
    """A single model instance in the pool."""

    model_id: str
    model: Optional[Any] = None
    tokenizer: Optional[Any] = None
    is_busy: bool = False
    last_used: float = 0.0

    def __post_init__(self):
        """Initialize last_used timestamp."""
        if self.last_used == 0.0:
            self.last_used = time.time()
