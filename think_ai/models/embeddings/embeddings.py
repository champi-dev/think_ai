"""Embedding models for vector generation."""

import asyncio
import hashlib
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import List, Optional

import numpy as np
import torch

from ..core.config import ModelConfig
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

    @abstractmethod
    def get_dimension(self) -> int:
        """Get the dimension of embeddings."""
        pass


class TransformerEmbeddings(EmbeddingModel):
    """Transformer-based embedding model using sentence-transformers."""

    def __init__(
            self,
            model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize the transformer embeddings model."""
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.dimension = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the transformer model."""
        if self._initialized:
            return

        try:
            # Try to import sentence-transformers
            from sentence_transformers import SentenceTransformer

            # Load model in executor to avoid blocking
            self.model = await asyncio.get_event_loop().run_in_executor(
                None, SentenceTransformer, self.model_name
            )

            # Get embedding dimension
            self.dimension = self.model.get_sentence_embedding_dimension()

            self._initialized = True
            logger.info(
                f"Initialized embedding model: {
                    self.model_name} (dim={
                    self.dimension})"
            )

        except ImportError:
            logger.warning(
                "sentence-transformers not available, using fallback embeddings"
            )
            self.model = None
            self.dimension = 384  # Standard embedding size
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}")
            raise

    async def embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts."""
        if not self._initialized:
            await self.initialize()

        if self.model is None:
            # Fallback to hash-based embeddings
            return [self._fallback_embedding(text) for text in texts]

        # Encode in executor to avoid blocking
        embeddings = await asyncio.get_event_loop().run_in_executor(
            None, self._encode_texts, texts
        )

        return [np.array(embedding) for embedding in embeddings]

    def _encode_texts(self, texts: List[str]):
        """Helper method to encode texts (runs in executor)."""
        return self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    async def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        embeddings = await self.embed_texts([text])
        return embeddings[0]

    def get_dimension(self) -> int:
        """Get the dimension of embeddings."""
        return self.dimension if self.dimension else 384

    def _fallback_embedding(self, text: str) -> np.ndarray:
        """Fallback embedding using hash-based approach."""
        # Create deterministic embedding from text hash
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()

        # Convert to normalized embedding
        embedding = np.array(
            # Normalize to [-1, 1]
            [(byte / 255.0 - 0.5) * 2 for byte in hash_bytes]
        )

        # Extend to target dimension
        target_dim = self.get_dimension()
        if len(embedding) < target_dim:
            # Repeat pattern to reach target dimension
            repeats = target_dim // len(embedding) + 1
            extended = np.tile(embedding, repeats)[:target_dim]
            return extended
        else:
            return embedding[:target_dim]


class FastEmbeddings(EmbeddingModel):
    """Fast hash-based embeddings for testing and fallback."""

    def __init__(self, dimension: int = 384):
        """Initialize fast embeddings."""
        self.dimension = dimension
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the fast embeddings."""
        self._initialized = True
        logger.info(f"Initialized fast embeddings (dim={self.dimension})")

    async def embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        """Generate fast hash-based embeddings."""
        if not self._initialized:
            await self.initialize()

        return [self._hash_embedding(text) for text in texts]

    async def embed_text(self, text: str) -> np.ndarray:
        """Generate fast embedding for single text."""
        if not self._initialized:
            await self.initialize()

        return self._hash_embedding(text)

    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self.dimension

    def _hash_embedding(self, text: str) -> np.ndarray:
        """Create hash-based embedding."""
        # Use multiple hash functions for better distribution
        hashes = []
        for i in range(4):
            hash_input = f"{text}_{i}"
            hash_obj = hashlib.sha256(hash_input.encode())
            hash_bytes = hash_obj.digest()
            hashes.extend(hash_bytes)

        # Convert to floating point embedding
        embedding = np.array(
            [
                (byte / 255.0 - 0.5) * 2  # Normalize to [-1, 1]
                for byte in hashes[: self.dimension]
            ]
        )

        # Ensure exact dimension
        if len(embedding) < self.dimension:
            padding = np.random.randn(self.dimension - len(embedding)) * 0.1
            embedding = np.concatenate([embedding, padding])

        return embedding[: self.dimension]


def create_embedding_model(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> EmbeddingModel:
    """Create an embedding model instance."""
    try:
        return TransformerEmbeddings(model_name)
    except Exception:
        logger.warning("Falling back to fast embeddings")
        return FastEmbeddings()


# Export main classes
__all__ = [
    "EmbeddingModel",
    "TransformerEmbeddings",
    "FastEmbeddings",
    "create_embedding_model",
]
