"""Alternative vector database implementation using HTTP/REST APIs
to avoid grpcio compilation issues.
"""

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

import httpx
import numpy as np


@dataclass
class VectorSearchResult:
    """Result from vector similarity search."""

    id: str
    score: float
    metadata: Dict[str, Any]
    vector: Optional[np.ndarray] = None


class HTTPVectorDB:
    """Vector database client using HTTP/REST APIs instead of gRPC.
    Supports multiple backends with fallback options.
    """

    def __init__(self, backend: str = "qdrant", **kwargs) -> None:
        self.backend = backend
        self.config = kwargs
        self.client = httpx.AsyncClient(timeout=30.0)

        # Configure based on backend
        if backend == "qdrant":
            self.base_url = (
                f"http://{kwargs.get('host', 'localhost')}:{kwargs.get('port', 6333)}"
            )
            self.collection = kwargs.get("collection", "think_ai")
        elif backend == "chroma":
            self.base_url = (
                f"http://{kwargs.get('host', 'localhost')}:{kwargs.get('port', 8000)}"
            )
            self.collection = kwargs.get("collection", "think_ai")
        elif backend == "weaviate":
            self.base_url = f"http://{
                kwargs.get(
                    'host', 'localhost')}:{
                kwargs.get(
                    'port', 8080)}/v1"
            self.collection = kwargs.get("collection", "ThinkAI")
        else:
            msg = f"Unsupported backend: {backend}"
            raise ValueError(msg)

    async def create_collection(
            self,
            dimension: int,
            distance: str = "cosine") -> None:
        """Create a collection/index for vectors."""
        if self.backend == "qdrant":
            payload = {
                "vectors": {
                    "size": dimension,
                    "distance": distance.capitalize(),
                },
            }
            response = await self.client.put(
                f"{self.base_url}/collections/{self.collection}",
                json=payload,
            )
            response.raise_for_status()

        elif self.backend == "chroma":
            payload = {
                "name": self.collection,
                "metadata": {"dimension": dimension},
            }
            response = await self.client.post(
                f"{self.base_url}/api/v1/collections",
                json=payload,
            )
            # Chroma returns 200 even if collection exists

        elif self.backend == "weaviate":
            payload = {
                "class": self.collection,
                "vectorizer": "none",
                "properties": [
                    {"name": "content", "dataType": ["text"]},
                    {"name": "metadata", "dataType": ["object"]},
                ],
            }
            response = await self.client.post(
                f"{self.base_url}/schema",
                json=payload,
            )
            # Weaviate returns 422 if class exists, which is fine

    async def insert_vectors(
        self, vectors: List[np.ndarray], ids: List[str], metadata: List[Dict[str, Any]]
    ) -> None:
        """Insert vectors with metadata."""
        if self.backend == "qdrant":
            points = []
            for _i, (vec, id_, meta) in enumerate(
                zip(vectors, ids, metadata, strict=False)
            ):
                points.append(
                    {
                        "id": id_,
                        "vector": vec.tolist(),
                        "payload": meta,
                    }
                )

            payload = {"points": points}
            response = await self.client.put(
                f"{self.base_url}/collections/{self.collection}/points",
                json=payload,
            )
            response.raise_for_status()

        elif self.backend == "chroma":
            payload = {
                "ids": ids,
                "embeddings": [v.tolist() for v in vectors],
                "metadatas": metadata,
            }
            response = await self.client.post(
                f"{self.base_url}/api/v1/collections/{self.collection}/add",
                json=payload,
            )
            response.raise_for_status()

        elif self.backend == "weaviate":
            objects = []
            for vec, id_, meta in zip(vectors, ids, metadata, strict=False):
                objects.append(
                    {
                        "class": self.collection,
                        "id": id_,
                        "vector": vec.tolist(),
                        "properties": {
                            "content": meta.get("content", ""),
                            "metadata": meta,
                        },
                    }
                )

            payload = {"objects": objects}
            response = await self.client.post(
                f"{self.base_url}/batch/objects",
                json=payload,
            )
            response.raise_for_status()

    async def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10,
        filter_dict: Optional[Dict[str, Any]] = None,
    ) -> List[VectorSearchResult]:
        """Search for similar vectors."""
        if self.backend == "qdrant":
            payload = {
                "vector": query_vector.tolist(),
                "limit": top_k,
                "with_payload": True,
                "with_vector": False,
            }
            if filter_dict:
                payload["filter"] = {
                    "must": [
                        {"key": k, "match": {"value": v}}
                        for k, v in filter_dict.items()
                    ]
                }

            response = await self.client.post(
                f"{self.base_url}/collections/{self.collection}/points/search",
                json=payload,
            )
            response.raise_for_status()

            results = []
            for point in response.json()["result"]:
                results.append(
                    VectorSearchResult(
                        id=point["id"],
                        score=point["score"],
                        metadata=point["payload"],
                    )
                )
            return results

        if self.backend == "chroma":
            payload = {
                "query_embeddings": [query_vector.tolist()],
                "n_results": top_k,
            }
            if filter_dict:
                payload["where"] = filter_dict

            response = await self.client.post(
                f"{self.base_url}/api/v1/collections/{self.collection}/query",
                json=payload,
            )
            response.raise_for_status()

            data = response.json()
            results = []
            for i in range(len(data["ids"][0])):
                results.append(
                    VectorSearchResult(
                        id=data["ids"][0][i],
                        score=1.0
                        # Convert distance to similarity
                        - data["distances"][0][i],
                        metadata=data["metadatas"][0][i] if data["metadatas"] else {
                        },
                    )
                )
            return results

        if self.backend == "weaviate":
            # GraphQL query for Weaviate
            query = {
                "query": f"""{{
                    Get {{
                        {self.collection}(
                            nearVector: {{
                                vector: {query_vector.tolist()}
                            }}
                            limit: {top_k}
                        ) {{
                            _additional {{
                                id
                                distance
                            }}
                            content
                            metadata
                        }}
                    }}
                }}""",
            }

            response = await self.client.post(
                f"{self.base_url}/graphql",
                json=query,
            )
            response.raise_for_status()

            results = []
            data = response.json()["data"]["Get"][self.collection]
            for item in data:
                results.append(
                    VectorSearchResult(
                        id=item["_additional"]["id"],
                        score=1.0 - float(item["_additional"]["distance"]),
                        metadata=item.get("metadata", {}),
                    )
                )
            return results
        return None

    async def delete_vectors(self, ids: List[str]) -> None:
        """Delete vectors by IDs."""
        if self.backend == "qdrant":
            payload = {"points": ids}
            response = await self.client.post(
                f"{self.base_url}/collections/{self.collection}/points/delete",
                json=payload,
            )
            response.raise_for_status()

        elif self.backend == "chroma":
            payload = {"ids": ids}
            response = await self.client.post(
                f"{self.base_url}/api/v1/collections/{self.collection}/delete",
                json=payload,
            )
            response.raise_for_status()

        elif self.backend == "weaviate":
            for id_ in ids:
                response = await self.client.delete(
                    f"{self.base_url}/objects/{self.collection}/{id_}",
                )
                # 404 is fine if object doesn't exist
                if response.status_code not in [200, 404]:
                    response.raise_for_status()

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()


# Convenience class for backward compatibility
class QdrantHTTPClient:
    """Qdrant client using HTTP instead of gRPC."""

    def __init__(
            self,
            host: str = "localhost",
            port: int = 6333,
            **kwargs) -> None:
        self.db = HTTPVectorDB(
            backend="qdrant",
            host=host,
            port=port,
            **kwargs)
        self.loop = asyncio.new_event_loop()

    def create_collection(self, name: str, vectors_config: Dict[str, Any]):
        """Synchronous wrapper for create_collection."""
        dimension = vectors_config.get("size", 384)
        distance = vectors_config.get("distance", "Cosine").lower()
        return self.loop.run_until_complete(
            self.db.create_collection(dimension, distance),
        )

    def upsert(self, collection_name: str, points: List[Dict[str, Any]]):
        """Synchronous wrapper for insert_vectors."""
        ids = [p["id"] for p in points]
        vectors = [np.array(p["vector"]) for p in points]
        metadata = [p.get("payload", {}) for p in points]
        return self.loop.run_until_complete(
            self.db.insert_vectors(vectors, ids, metadata),
        )

    def search(
            self,
            collection_name: str,
            query_vector: list[float],
            limit: int = 10,
            **kwargs):
        """Synchronous wrapper for search."""
        results = self.loop.run_until_complete(
            self.db.search(np.array(query_vector), limit),
        )
        # Convert to Qdrant-like format
        return [
            {
                "id": r.id,
                "score": r.score,
                "payload": r.metadata,
            }
            for r in results
        ]


__all__ = ["HTTPVectorDB", "QdrantHTTPClient", "VectorSearchResult"]
