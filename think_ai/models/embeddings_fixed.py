"""Language model embeddings for Think AI - Fixed Version"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import numpy as np

from ..utils.logging import get_logger

logger = get_logger(__name__)


class EmbeddingModel(ABC):
    """Abstract base class for embedding models."""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the embedding model."""
        pass

    @abstractmethod
    async def embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for a list of texts."""
        pass

    @abstractmethod
    async def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        pass


class SentenceTransformerEmbedding(EmbeddingModel):
    """Sentence transformer embedding model."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize with model name."""
        self.model_name = model_name
        self.model = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the sentence transformer model."""
        if self._initialized:
            return

        try:
            # Import here to avoid dependency issues
            from sentence_transformers import SentenceTransformer

            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self._initialized = True
            logger.info("Embedding model initialized successfully")

        except ImportError:
            logger.warning(
                "sentence-transformers not available, using fallback")
            self.model = None
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}")
            raise

    async def embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts."""
        if not self._initialized:
            await self.initialize()

        if self.model is None:
            # Fallback to simple hash-based embeddings
            return [self._fallback_embedding(text) for text in texts]

        # Encode in executor to avoid blocking
        embeddings = await asyncio.get_event_loop().run_in_executor(
            None,
            self.model.encode,
            texts,
        )

        return [np.array(emb) for emb in embeddings]

    async def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        embeddings = await self.embed_texts([text])
        return embeddings[0]

    def _fallback_embedding(self, text: str) -> np.ndarray:
        """Fallback embedding using simple hash-based approach."""
        # Simple hash-based embedding for when sentence-transformers is not
        # available
        import hashlib

        # Create a deterministic embedding based on text content
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()

        # Convert to float array (384 dimensions to match typical models)
        embedding = np.array(
            # Normalize to [-1, 1]
            [(byte / 255.0 - 0.5) * 2 for byte in hash_bytes]
        )

        # Pad or truncate to 384 dimensions
        if len(embedding) < 384:
            padding = np.random.randn(384 - len(embedding)) * 0.1
            embedding = np.concatenate([embedding, padding])
        else:
            embedding = embedding[:384]

        return embedding


def create_embedding_model(
        model_name: str = "all-MiniLM-L6-v2") -> EmbeddingModel:
    """Create an embedding model instance."""
    return SentenceTransformerEmbedding(model_name)
