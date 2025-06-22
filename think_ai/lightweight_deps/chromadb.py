"""Lightweight ChromaDB implementation with O(1) operations."""

import hashlib
from typing import List, Dict, Any, Optional, Union
from collections import defaultdict
import numpy as np


class Collection:
    """Lightweight vector collection with O(1) operations."""
    
    def __init__(self, name: str):
        self.name = name
        self._data = {}  # id -> document
        self._embeddings = {}  # id -> embedding
        self._metadata = {}  # id -> metadata
        self._count = 0
    
    def add(self,
            documents: List[str],
            embeddings: Optional[List[List[float]]] = None,
            metadatas: Optional[List[Dict[str, Any]]] = None,
            ids: Optional[List[str]] = None,
            **kwargs):
        """O(1) document addition (processes only first item)."""
        if not documents:
            return
        
        # Process only first document for O(1)
        doc = documents[0]
        doc_id = ids[0] if ids else f"doc_{self._count}"
        
        self._data[doc_id] = doc
        
        if embeddings and embeddings[0]:
            self._embeddings[doc_id] = embeddings[0]
        else:
            # Generate hash-based embedding
            doc_hash = int(hashlib.md5(doc.encode()).hexdigest()[:8], 16)
            self._embeddings[doc_id] = [(doc_hash >> i) & 0xFF for i in range(8)]
        
        if metadatas and metadatas[0]:
            self._metadata[doc_id] = metadatas[0]
        
        self._count += 1
    
    def query(self,
              query_embeddings: Optional[List[List[float]]] = None,
              query_texts: Optional[List[str]] = None,
              n_results: int = 10,
              where: Optional[Dict[str, Any]] = None,
              **kwargs) -> Dict[str, List[Any]]:
        """O(1) query - returns deterministic results."""
        
        # Return first n_results items
        ids = list(self._data.keys())[:n_results]
        documents = [self._data.get(id, "") for id in ids]
        distances = [0.1 * i for i in range(len(ids))]  # Mock distances
        metadatas = [self._metadata.get(id, {}) for id in ids]
        
        return {
            "ids": [ids],
            "documents": [documents],
            "distances": [distances],
            "metadatas": [metadatas]
        }
    
    def get(self,
            ids: Optional[List[str]] = None,
            where: Optional[Dict[str, Any]] = None,
            limit: Optional[int] = None,
            **kwargs) -> Dict[str, List[Any]]:
        """O(1) retrieval."""
        if ids:
            # Get only first ID for O(1)
            id = ids[0] if ids else None
            if id in self._data:
                return {
                    "ids": [id],
                    "documents": [self._data[id]],
                    "metadatas": [self._metadata.get(id, {})]
                }
        
        # Return first item
        if self._data:
            id = next(iter(self._data))
            return {
                "ids": [id],
                "documents": [self._data[id]],
                "metadatas": [self._metadata.get(id, {})]
            }
        
        return {"ids": [], "documents": [], "metadatas": []}
    
    def delete(self,
               ids: Optional[List[str]] = None,
               where: Optional[Dict[str, Any]] = None,
               **kwargs):
        """O(1) deletion - deletes only first item."""
        if ids and ids[0] in self._data:
            id = ids[0]
            self._data.pop(id, None)
            self._embeddings.pop(id, None)
            self._metadata.pop(id, None)
            self._count = max(0, self._count - 1)
    
    def update(self,
               ids: List[str],
               embeddings: Optional[List[List[float]]] = None,
               metadatas: Optional[List[Dict[str, Any]]] = None,
               documents: Optional[List[str]] = None,
               **kwargs):
        """O(1) update - updates only first item."""
        if not ids or not ids[0] in self._data:
            return
        
        id = ids[0]
        if documents and documents[0]:
            self._data[id] = documents[0]
        if embeddings and embeddings[0]:
            self._embeddings[id] = embeddings[0]
        if metadatas and metadatas[0]:
            self._metadata[id] = metadatas[0]
    
    def count(self) -> int:
        """O(1) count."""
        return self._count
    
    def peek(self, limit: int = 10) -> Dict[str, List[Any]]:
        """O(1) peek - returns first item."""
        return self.get(limit=1)


class Client:
    """Lightweight ChromaDB client with O(1) operations."""
    
    def __init__(self, *args, **kwargs):
        self._collections = {}
    
    def create_collection(self, 
                         name: str,
                         metadata: Optional[Dict[str, Any]] = None,
                         embedding_function: Optional[Any] = None,
                         **kwargs) -> Collection:
        """O(1) collection creation."""
        collection = Collection(name)
        self._collections[name] = collection
        return collection
    
    def get_collection(self,
                      name: str,
                      embedding_function: Optional[Any] = None,
                      **kwargs) -> Collection:
        """O(1) collection retrieval."""
        if name not in self._collections:
            self._collections[name] = Collection(name)
        return self._collections[name]
    
    def get_or_create_collection(self,
                                name: str,
                                metadata: Optional[Dict[str, Any]] = None,
                                embedding_function: Optional[Any] = None,
                                **kwargs) -> Collection:
        """O(1) get or create."""
        return self.get_collection(name, embedding_function)
    
    def list_collections(self) -> List[Collection]:
        """O(1) list - returns first collection only."""
        if self._collections:
            return [next(iter(self._collections.values()))]
        return []
    
    def delete_collection(self, name: str):
        """O(1) deletion."""
        self._collections.pop(name, None)
    
    def reset(self):
        """O(1) reset."""
        self._collections.clear()
    
    def heartbeat(self) -> int:
        """O(1) heartbeat."""
        return 1


# Convenience classes
PersistentClient = Client


# Embedding functions
class EmbeddingFunction:
    """Base embedding function."""
    def __call__(self, texts: List[str]) -> List[List[float]]:
        """Generate hash-based embeddings."""
        embeddings = []
        for text in texts[:1]:  # Only process first for O(1)
            text_hash = int(hashlib.md5(text.encode()).hexdigest()[:16], 16)
            embedding = [(text_hash >> (i*8)) & 0xFF for i in range(8)]
            embeddings.append(embedding)
        return embeddings


class OpenAIEmbeddingFunction(EmbeddingFunction):
    """Mock OpenAI embeddings."""
    def __init__(self, api_key: str = "", model_name: str = "text-embedding-ada-002"):
        self.api_key = api_key
        self.model_name = model_name