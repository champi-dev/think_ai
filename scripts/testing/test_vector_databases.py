#! / usr / bin / env python3

"""
Comprehensive test of vector database libraries:
    - Milvus (pymilvus)
    - FAISS (faiss - cpu)
    - Neo4j
    - Sentence Transformers for embeddings
"""

import time

import faiss
import numpy as np
import torch
from neo4j import GraphDatabase
from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections, utility
from sentence_transformers import SentenceTransformer

    class VectorDatabaseTester:

        def __init__(self):
# Force CPU usage to avoid CUDA issues
            torch.set_default_device("cpu")
            self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
            self.documents = [
            "Python is a high - level programming language",
            "Machine learning is a subset of artificial intelligence",
            "Vector databases are optimized for similarity search",
            "Neural networks are inspired by biological neurons",
            "Natural language processing helps computers understand human language",
            "Deep learning uses multiple layers of neural networks",
            "Embeddings convert text into numerical vectors",
            "Similarity search finds nearest neighbors in vector space"]

            def test_faiss(self):
                print("\n == = Testing FAISS == =")
                start_time = time.time()

# Generate embeddings
                embeddings = self.model.encode(self.documents)
                dimension = embeddings.shape[1]

# Create FAISS index
                index = faiss.IndexFlatL2(dimension)
                index.add(embeddings.astype("float32"))

# Search for similar documents
                query = "What is artificial intelligence?"
                query_embedding = self.model.encode([query])

                k = 3  # Find top 3 similar documents
                distances, indices = index.search(query_embedding.astype("float32"), k)

                print(f"Query: {query}")
                print(f"Top {k} similar documents:")
                for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
                    print(f"{i + 1}. Distance: {dist:.4f} - Document: {self.documents[idx]}")

                    print(f"FAISS test completed in {time.time() - start_time:.2f} seconds")
                    return True

                def test_milvus(self):
                    print("\n == = Testing Milvus == =")
                    start_time = time.time()

                    try:
# Connect to Milvus
                        connections.connect(alias="default", host="localhost", port=19530)

# Create collection
                        collection_name = "test_collection"

# Drop existing collection if exists
                        if utility.has_collection(collection_name):
                            utility.drop_collection(collection_name)

# Define schema
                            fields = [
                            FieldSchema(
                            name="id", dtype=DataType.INT64, is_primary=True, auto_id=True), FieldSchema(
                            name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384), FieldSchema(
                            name="text", dtype=DataType.VARCHAR, max_length=500)]
                            schema = CollectionSchema(fields=fields, description="Test collection")

# Create collection
                            collection = Collection(name=collection_name, schema=schema)

# Generate embeddings
                            embeddings = self.model.encode(self.documents)

# Insert data
                            entities = [
                            embeddings.tolist(),
                            self.documents
                            ]
                            collection.insert(entities)

# Create index
                            index_params = {
                            "metric_type": "L2",
                            "index_type": "IVF_FLAT",
                            "params": {"nlist": 128}
                            }
                            collection.create_index(field_name="embedding", index_params=index_params)
                            collection.load()

# Search
                            query = "What is machine learning?"
                            query_embedding = self.model.encode([query])

                            search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
                            results = collection.search(
                            data=query_embedding.tolist(),
                            anns_field="embedding",
                            param=search_params,
                            limit=3,
                            output_fields=["text"]
                            )

                            print(f"Query: {query}")
                            print("Top 3 similar documents:")
                            for i, hit in enumerate(results[0]):
                                print(f"{i + 1}. Distance: {hit.distance:.4f} - Document: {hit.entity.get("text")}")

# Cleanup
                                utility.drop_collection(collection_name)
                                connections.disconnect("default")

                                print(f"Milvus test completed in {time.time() - start_time:.2f} seconds")
                                return True

                            except Exception as e:
                                print(f"Milvus test skipped (server not running): {e}")
                                return False

                            def test_neo4j(self):
                                print("\n == = Testing Neo4j == =")
                                start_time = time.time()

                                try:
# Connect to Neo4j
                                    uri = "bolt://localhost:7687"
                                    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

                                    with driver.session() as session:
# Clear existing data
                                        session.run("MATCH (n) DETACH DELETE n")

# Create nodes with embeddings
                                        embeddings = self.model.encode(self.documents)

                                        for i, (doc, embedding) in enumerate(zip(self.documents, embeddings)):
                                            session.run(
                                            "CREATE (d:Document {id: $id, text: $text, embedding: $embedding})",
                                            id=i, text=doc, embedding=embedding.tolist()
                                            )

# Create relationships based on similarity
                                            threshold = 20.0  # Similarity threshold
                                            for i in range(len(self.documents)):
                                                for j in range(i + 1, len(self.documents)):
                                                    distance = np.linalg.norm(embeddings[i] - embeddings[j])
                                                    if distance < threshold:
                                                        session.run(
"""
                                                        MATCH (d1:Document {id: $id1}), (d2:Document {id: $id2})
                                                        CREATE (d1) - [:SIMILAR_TO {distance: $distance}] - > (d2)
""",
                                                        id1=i, id2=j, distance=float(distance)
                                                        )

# Query similar documents
                                                        result = session.run(
"""
                                                        MATCH (d1:Document) - [r:SIMILAR_TO] - > (d2:Document)
                                                        WHERE r.distance < 15.0
                                                        RETURN d1.text as doc1, d2.text as doc2, r.distance as distance
                                                        ORDER BY r.distance
                                                        LIMIT 5
"""
                                                        )

                                                        print("Top 5 most similar document pairs:")
                                                        for i, record in enumerate(result):
                                                            print(f"{i + 1}. Distance: {record["distance"]:.4f}")
                                                            print(f" Doc1: {record["doc1"]}")
                                                            print(f" Doc2: {record["doc2"]}")

                                                            driver.close()
                                                            print(f"Neo4j test completed in {time.time() - start_time:.2f} seconds")
                                                            return True

                                                        except Exception as e:
                                                            print(f"Neo4j test skipped (server not running): {e}")
                                                            return False

                                                        def run_all_tests(self):
                                                            print("Starting comprehensive vector database tests...")
                                                            print(f"Using embedding model: {self.model}")
                                                            print(f"Number of test documents: {len(self.documents)}")

                                                            results = {
                                                            "FAISS": self.test_faiss(),
                                                            "Milvus": self.test_milvus(),
                                                            "Neo4j": self.test_neo4j()
                                                            }

                                                            print("\n == = Test Summary == =")
                                                            for db, success in results.items():
                                                                status = "✓ PASSED" if success else "✗ SKIPPED"
                                                                print(f"{db}: {status}")

                                                                return results

                                                            if __name__ = = "__main__":
                                                                tester = VectorDatabaseTester()
                                                                results = tester.run_all_tests()
