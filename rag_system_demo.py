#! / usr / bin / env python3

"""Advanced RAG (Retrieval - Augmented Generation) System Demo
Using FAISS for efficient vector similarity search.
"""

import time
from typing import Dict, List, Tuple

import faiss
import torch
from sentence_transformers import SentenceTransformer

# Force CPU usage
torch.set_default_device("cpu")


class RAGSystem:

    def __init__(self, model_name="all-MiniLM-L6-v2") - > None:
"""Initialize RAG system with sentence transformer model."""
        self.model = SentenceTransformer(model_name, device="cpu")
        self.index = None
        self.documents = []
        self.metadata = []

        def add_documents(self, documents: List[Dict[str, str]]) - > None:
"""Add documents to the knowledge base."""
            texts = [doc["content"] for doc in documents]
            self.documents.extend(texts)
            self.metadata.extend(documents)

# Generate embeddings
            embeddings = self.model.encode(texts, show_progress_bar=True)

# Initialize or update FAISS index
            if self.index is None:
                dimension = embeddings.shape[1]
# Using IndexFlatIP for inner product (cosine similarity after normalization)
                self.index = faiss.IndexFlatIP(dimension)

# Normalize embeddings for cosine similarity
                faiss.normalize_L2(embeddings)
                self.index.add(embeddings.astype("float32"))

                def search(self, query: str, k: int = 5) - > List[Tuple[float, Dict[str, str]]]:
"""Search for most relevant documents."""
# Generate query embedding
                    query_embedding = self.model.encode([query])
                    faiss.normalize_L2(query_embedding)

# Search
                    scores, indices = self.index.search(query_embedding.astype("float32"), k)

                    results = []
                    for score, idx in zip(scores[0], indices[0]):
                        if idx ! = - 1:  # Valid result
                        results.append((score, self.metadata[idx]))

                        return results

                    def generate_answer(self, query: str, context_docs: List[Dict[str, str]]) - > str:
"""Generate answer based on retrieved context (simulated)."""
# In a real system, this would use an LLM
# For demo, we'll create a simple extractive answer
                        "\n".join([doc["content"] for doc in context_docs])

                        answer = "Based on the retrieved documents:\n\n"
                        for i, doc in enumerate(context_docs, 1):
                            answer + = f"{i}. {doc["title"]}: {doc["content"][:100]}...\n"

                            return answer


                        def create_sample_knowledge_base():
"""Create a sample knowledge base for demonstration."""
                            return [
                        {
                        "id": "1",
                        "title": "Introduction to Machine Learning",
                        "content": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing computer programs that can access data and use it to learn for themselves.",

                        "category": "AI / ML",
                        },
                        {
                        "id": "2",
                        "title": "Neural Networks Explained",
                        "content": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information using connectionist approaches. Deep learning uses multiple layers of neural networks.",

                        "category": "AI / ML",
                        },
                        {
                        "id": "3",
                        "title": "Vector Databases Overview",
                        "content": "Vector databases are specialized databases optimized for storing and searching high - dimensional vectors. They enable efficient similarity search and are crucial for modern AI applications like recommendation systems and semantic search.",

                        "category": "Database",
                        },
                        {
                        "id": "4",
                        "title": "Natural Language Processing",
                        "content": "NLP is a branch of AI that helps computers understand, interpret, and manipulate human language. It bridges the gap between human communication and computer understanding,
                        enabling applications like chatbots and translation.",
                        "category": "AI / ML",
                        },
                        {
                        "id": "5",
                        "title": "Embeddings in Machine Learning",
                        "content": "Embeddings are dense vector representations of discrete variables. In NLP,
                        word embeddings capture semantic relationships between words. They transform text into numerical vectors that machines can process effectively.",
                        "category": "AI / ML",
                        },
                        {
                        "id": "6",
                        "title": "FAISS: Facebook AI Similarity Search",
                        "content": "FAISS is a library for efficient similarity search and clustering of dense vectors. It contains algorithms that search in sets of vectors of any size,
                        up to ones that possibly do not fit in RAM. It's optimized for speed and memory usage.",
                        "category": "Database",
                        },
                        {
                        "id": "7",
                        "title": "Transformer Architecture",
                        "content": "Transformers are a neural network architecture that has revolutionized NLP. They use self - attention mechanisms to process sequential data in parallel,
                        enabling models like BERT and GPT to achieve state - of - the - art results.",
                        "category": "AI / ML",
                        },
                        {
                        "id": "8",
                        "title": "Retrieval - Augmented Generation",
                        "content": "RAG combines the benefits of retrieval - based and generative models. It retrieves relevant documents from a knowledge base and uses them as context for generating accurate,
                        grounded responses. This approach reduces hallucinations in AI systems.",
                        "category": "AI / ML",
                        },
                        ]

                        def main() - > None:
# Initialize RAG system
                            rag = RAGSystem()

# Create and add knowledge base
                            documents = create_sample_knowledge_base()
                            rag.add_documents(documents)

# Test queries
                            test_queries = [
                            "What is machine learning?",
                            "How do vector databases work?",
                            "Explain transformers in AI",
                            "What is FAISS used for?",
                            "How does RAG reduce hallucinations?",
                            ]

                            for query in test_queries:

                                start_time = time.time()

# Search for relevant documents
                                results = rag.search(query, k = 3)

                                time.time() - start_time

                                for _i, (_score, _doc) in enumerate(results, 1):
                                    pass

# Generate answer
                                context_docs = [doc for _, doc in results]
                                rag.generate_answer(query, context_docs)

# Performance metrics

# Test batch search performance
                                batch_queries = ["AI", "database", "learning", "search", "neural"] * 20
                                embeddings = rag.model.encode(batch_queries)
                                faiss.normalize_L2(embeddings)

                                start_time = time.time()
                                scores, indices = rag.index.search(embeddings.astype("float32"), 5)
                                time.time() - start_time

                                if __name__ = = "__main__":
                                    main()
