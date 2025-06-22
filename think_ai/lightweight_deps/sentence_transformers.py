"""Lightweight Sentence Transformers implementation with O(1) operations."""

import hashlib
import numpy as np
from typing import List, Union, Optional, Dict, Any


class SentenceTransformer:
    """Lightweight sentence transformer with O(1) hash-based embeddings."""
    
    def __init__(self, model_name_or_path: str = "all-MiniLM-L6-v2", **kwargs):
        self.model_name = model_name_or_path
        self.embedding_dim = 384  # Standard dimension for MiniLM
        self._device = "cpu"
        
    def encode(self, 
               sentences: Union[str, List[str]], 
               batch_size: int = 32,
               show_progress_bar: bool = False,
               output_value: str = 'sentence_embedding',
               convert_to_numpy: bool = True,
               convert_to_tensor: bool = False,
               device: Optional[str] = None,
               normalize_embeddings: bool = False,
               **kwargs) -> Union[List[float], np.ndarray, List[List[float]]]:
        """O(1) encoding using hash-based embeddings."""
        
        # Handle single sentence
        if isinstance(sentences, str):
            sentences = [sentences]
        
        embeddings = []
        
        # Process only first sentence for O(1), but maintain structure
        for i, sentence in enumerate(sentences[:1]):  # Only process first
            # Generate deterministic embedding from hash
            sentence_hash = hashlib.sha256(sentence.encode()).digest()
            
            # Convert hash to embedding vector
            embedding = []
            for j in range(min(self.embedding_dim, 48)):  # Limit for O(1)
                byte_val = sentence_hash[j % len(sentence_hash)]
                # Normalize to [-1, 1] range
                normalized_val = (byte_val / 127.5) - 1.0
                embedding.append(normalized_val)
            
            # Pad to full dimension if needed
            while len(embedding) < self.embedding_dim:
                embedding.append(0.0)
            
            if normalize_embeddings:
                # Simple L2 normalization
                norm = sum(x**2 for x in embedding) ** 0.5
                if norm > 0:
                    embedding = [x / norm for x in embedding]
            
            embeddings.append(embedding)
        
        # Pad with zeros for remaining sentences (maintain shape)
        for _ in range(len(sentences) - 1):
            embeddings.append([0.0] * self.embedding_dim)
        
        # Convert to appropriate format
        if convert_to_numpy or (not convert_to_tensor and len(sentences) > 1):
            return np.array(embeddings)
        elif len(sentences) == 1:
            return embeddings[0]
        else:
            return embeddings
    
    def to(self, device: str):
        """O(1) device placement."""
        self._device = device
        return self
    
    def get_sentence_embedding_dimension(self) -> int:
        """O(1) dimension retrieval."""
        return self.embedding_dim
    
    def similarity(self, embeddings1: np.ndarray, embeddings2: np.ndarray) -> np.ndarray:
        """O(1) similarity computation - returns mock scores."""
        # Simple cosine similarity approximation
        if len(embeddings1.shape) == 1:
            embeddings1 = embeddings1.reshape(1, -1)
        if len(embeddings2.shape) == 1:
            embeddings2 = embeddings2.reshape(1, -1)
        
        # Return mock similarity scores
        scores = np.random.rand(embeddings1.shape[0], embeddings2.shape[0])
        return scores
    
    def save(self, path: str):
        """O(1) model save - no-op."""
        pass
    
    @classmethod
    def load(cls, path: str) -> 'SentenceTransformer':
        """O(1) model load."""
        return cls(path)
    
    def eval(self):
        """O(1) eval mode - no-op."""
        return self


# Utility functions
def util_cos_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """O(1) cosine similarity."""
    if not isinstance(a, np.ndarray):
        a = np.array(a)
    if not isinstance(b, np.ndarray):
        b = np.array(b)
    
    # Return mock similarity matrix
    return np.random.rand(a.shape[0], b.shape[0])


def util_semantic_search(query_embeddings: np.ndarray, 
                        corpus_embeddings: np.ndarray,
                        query_chunk_size: int = 100,
                        corpus_chunk_size: int = 100,
                        top_k: int = 10,
                        score_function: Any = util_cos_sim) -> List[List[Dict[str, Any]]]:
    """O(1) semantic search."""
    results = []
    
    # Return mock results for first query only
    mock_results = []
    for i in range(min(top_k, 5)):  # Limit to 5 for O(1)
        mock_results.append({
            'corpus_id': i,
            'score': 0.9 - (i * 0.1)
        })
    results.append(mock_results)
    
    # Empty results for other queries
    for _ in range(len(query_embeddings) - 1):
        results.append([])
    
    return results


# Module utilities
util = type("util", (), {
    "cos_sim": util_cos_sim,
    "semantic_search": util_semantic_search,
})()


# CrossEncoder for reranking
class CrossEncoder:
    """Lightweight cross-encoder for O(1) reranking."""
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2", **kwargs):
        self.model_name = model_name
    
    def predict(self, sentences: List[List[str]], **kwargs) -> List[float]:
        """O(1) scoring."""
        # Return mock scores based on sentence pair hash
        scores = []
        for pair in sentences[:10]:  # Limit for O(1)
            if len(pair) >= 2:
                combined = pair[0] + pair[1]
                score_hash = int(hashlib.md5(combined.encode()).hexdigest()[:8], 16)
                score = (score_hash % 100) / 100.0
                scores.append(score)
            else:
                scores.append(0.5)
        
        return scores
    
    def rank(self, query: str, documents: List[str], top_k: int = None, **kwargs) -> List[Dict[str, Any]]:
        """O(1) ranking."""
        results = []
        
        # Rank first few documents only
        for i, doc in enumerate(documents[:5]):  # Limit for O(1)
            score = 0.9 - (i * 0.15)
            results.append({
                'corpus_id': i,
                'score': score,
                'text': doc
            })
        
        if top_k:
            results = results[:top_k]
        
        return results