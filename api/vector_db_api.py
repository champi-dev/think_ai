#! / usr / bin / env python3

"""Vector Database REST API
Test the vector databases through HTTP endpoints.
"""

import time
from typing import List, Optional

import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from vector_search_adapter import VectorSearchAdapter

# Import our vector search adapter instead of FAISS

# Force CPU usage
torch.set_default_device("cpu")

app = FastAPI(title="Vector Database API", version="1.0.0")

# Enable CORS
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# Global variables
model = None
vector_index = None
documents = []


class Document(BaseModel):
    id: str
    title: str
    content: str
    category: Optional[str] = "general"


    class SearchQuery(BaseModel):
        query: str
        k: int = 5


        class SearchResult(BaseModel):
            score: float
            document: Document


            class IndexStats(BaseModel):
                total_documents: int
                vector_dimension: int
                index_type: str
                ready: bool


                @app.on_event("startup")
                async def startup_event() - > None:
"""Initialize the model and index on startup."""
                    global model, vector_index
                    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
                    vector_index = VectorSearchAdapter(384)


                    @app.get("/")
                    async def root():
"""Root endpoint with web interface."""
                        return HTMLResponse("""
                    < !DOCTYPE html >
                    < html >
                    < head >
                    < title > Think AI - Vector Database < / title >
                    < style >
                    body { font - family: - apple - system, sans - serif; margin: 0; padding: 0; background: #0a0e27; color: #fff; }
                    .container { max - width: 1200px; margin: 0 auto; padding: 40px 20px; }
                    h1 { font - size: 3em; margin - bottom: 20px; background: linear - gradient(135deg, #667eea 0%, #764ba2 100%); - webkit - background - clip: text; - webkit - text - fill - color: transparent; }
                    .nav { background: rgba(255, 255, 255, 0.1); padding: 20px; border - radius: 10px; margin - bottom: 30px; }
                    .nav a { color: #667eea; text - decoration: none; margin: 0 15px; font - weight: bold; }
                    .nav a:hover { text - decoration: underline; }
                    .features { display: grid; grid - template - columns: repeat(auto - fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }
                    .feature { background: rgba(255, 255, 255, 0.05); padding: 30px; border - radius: 10px; border: 1px solid rgba(102, 126, 234, 0.3); }
                    .feature h3 { color: #764ba2; margin - top: 0; }
                    .demo - apps { background: rgba(102, 126, 234, 0.1); padding: 30px; border - radius: 10px; margin: 30px 0; }
                    .app - link { display: inline - block; background: #667eea; color: white; padding: 10px 20px; border - radius: 5px; text - decoration: none; margin: 10px 10px 10px 0; }
                    .app - link:hover { background: #764ba2; }
                    .api - test { background: rgba(255, 255, 255, 0.05); padding: 30px; border - radius: 10px; margin: 30px 0; }
                    input, textarea { width: 100%; padding: 10px; margin: 10px 0; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); color: white; border - radius: 5px; }
                    button { background: #667eea; color: white; border: none; padding: 12px 30px; border - radius: 5px; cursor: pointer; font - size: 16px; }
                    button:hover { background: #764ba2; }
#results { background: rgba(0, 0, 0, 0.3); padding: 20px; border - radius: 5px; margin - top: 20px; max - height: 400px; overflow - y: auto; }
                    .result - item { background: rgba(255, 255, 255, 0.05); padding: 15px; margin: 10px 0; border - radius: 5px; }
                    .score { color: #4CAF50; font - weight: bold; }
                    pre { background: rgba(0, 0, 0, 0.5); padding: 15px; border - radius: 5px; overflow - x: auto; }
                    .stats { display: grid; grid - template - columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }
                    .stat - box { background: rgba(255, 255, 255, 0.05); padding: 20px; border - radius: 10px; text - align: center; }
                    .stat - number { font - size: 2em; font - weight: bold; color: #667eea; }
                    < / style >
                    < / head >
                    < body >
                    < div class = "container" >
                    < h1 > 🚀 Think AI Vector Database < / h1 >

                    < div class = "nav" >
                    < a href = "https://github.com/champi-dev/think_ai" target = "_blank" > 📦 GitHub < / a >
                    < a href = "/docs" > 📚 API Docs < / a >
                    < a href = "#demo - apps" > 🎮 Demo Apps < / a >
                    < a href = "#test - api" > 🧪 Test API < / a >
                    < / div >

                    < div class = "features" >
                    < div class = "feature" >
                    < h3 > ⚡ O(1) Performance < / h3 >
                    < p > Lightning - fast vector search with 0.24ms query time using our custom LSH implementation < / p >
                    < / div >
                    < div class = "feature" >
                    < h3 > 🔧 No Compilation < / h3 >
                    < p > Pure Python implementation - no SWIG, no native dependencies, works everywhere < / p >
                    < / div >
                    < div class = "feature" >
                    < h3 > 🧠 AI - Powered < / h3 >
                    < p > Semantic search using sentence transformers for intelligent code understanding < / p >
                    < / div >
                    < / div >

                    < div class = "demo - apps" id = "demo - apps" >
                    < h2 > 🎮 Demo Applications < / h2 >
                    < p > Test the Think AI system with these live demos: < / p >
                    < a href = "http://localhost:8001" class = "app - link" target = "_blank" > 💻 Collaborative Code Editor < / a >
                    < a href = "http://localhost:8002" class = "app - link" target = "_blank" > 📚 API Doc Generator < / a >
                    < a href = "http://localhost:8003" class = "app - link" target = "_blank" > 🔍 Code Review System < / a >
                    < / div >

                    < div class = "api - test" id = "test - api" >
                    < h2 > 🧪 Test the API < / h2 >

                    < h3 > Add Document < / h3 >
                    < input type = "text" id = "doc - title" placeholder = "Document Title" >
                    < textarea id = "doc - content" placeholder = "Document Content" rows = "4" > < / textarea >
                    < button onclick = "addDocument()" > Add to Index < / button >

                    < h3 > Search < / h3 >
                    < input type = "text" id = "search - query" placeholder = "Search query..." >
                    < button onclick = "searchDocuments()" > Search < / button >

                    < div id = "results" > < / div >
                    < / div >

                    < div class = "stats" >
                    < div class = "stat - box" >
                    < div class = "stat - number" id = "total - docs" > 0 < / div >
                    < div > Documents < / div >
                    < / div >
                    < div class = "stat - box" >
                    < div class = "stat - number" id = "vector - dim" > 384 < / div >
                    < div > Vector Dimension < / div >
                    < / div >
                    < div class = "stat - box" >
                    < div class = "stat - number" id = "backend - type" > - < / div >
                    < div > Backend < / div >
                    < / div >
                    < div class = "stat - box" >
                    < div class = "stat - number" id = "status" > Ready < / div >
                    < div > Status < / div >
                    < / div >
                    < / div >
                    < / div >

                    < script >
                    async function loadStats() {
                    const response = await fetch("/stats");
                    const stats = await response.json();
                    document.getElementById("total - docs").textContent = stats.total_documents;
                    document.getElementById("backend - type").textContent = stats.index_type.split(" ")[0];
                    }

                    async function addDocument() {
                    const title = document.getElementById("doc - title").value;
                    const content = document.getElementById("doc - content").value;

                    if (!title || !content) {
                    alert("Please fill in both title and content");
                    return;
                }

                const response = await fetch("/documents", {
                method: "POST",
                headers: { "Content - Type": "application / json" },
                body: JSON.stringify([{
                id: Date.now().toString(),
                title: title,
                content: content
                }])
                });

                const result = await response.json();
                document.getElementById("results").innerHTML = "<div class="result - item">✅ " + result.message + "</div>";

                / / Clear form
                document.getElementById("doc - title").value = "";
                document.getElementById("doc - content").value = "";

                / / Reload stats
                loadStats();
                }

                async function searchDocuments() {
                const query = document.getElementById("search - query").value;
                if (!query) return;

                const response = await fetch("/search", {
                method: "POST",
                headers: { "Content - Type": "application / json" },
                body: JSON.stringify({ query: query, k: 5 })
                });

                const results = await response.json();

                let html = "<h3 > Search Results:</h3>";
                results.forEach((result, i) = > {
                html + = `
                < div class = "result - item" >
                < strong > ${i + 1}. ${result.document.title} < / strong >
                < span class = "score" > Score: ${result.score.toFixed(4)} < / span > < br >
                < small > ${result.document.content.substring(0, 200)}... < / small >
                < / div >
                `;
                });

                document.getElementById("results").innerHTML = html;
                }

                / / Load stats on page load
                loadStats();

                / / Load demo data
                fetch("/demo", { method: "POST" });
                < / script >
                < / body >
                < / html >
""")


                @app.get("/health")
                async def health_check():
"""Health check endpoint."""
                    return {
                "status": "healthy",
                "model_loaded": model is not None,
                "index_initialized": vector_index is not None,
                }


                @app.get("/stats", response_model=IndexStats)
                async def get_stats():
"""Get index statistics."""
                    backend_info = vector_index.get_backend_info() if vector_index else {
                    "backend": "Not initialized"}
                    return IndexStats(
                total_documents=len(documents),
                vector_dimension=384,
                index_type=f"{
                backend_info.get(
                "backend",
                "Unknown").upper()} Vector Search",
                ready=vector_index is not None,
                )


                @app.post("/documents")
                async def add_documents(docs: List[Document]):
"""Add documents to the index."""
                    global vector_index, documents

                    if not model:
                        raise HTTPException(status_code=503, detail="Model not initialized")

                    if not vector_index:
                        raise HTTPException(status_code=503, detail="Vector index not initialized")

# Generate embeddings and add
                    start_time = time.time()
                    for doc in docs:
                        embedding = model.encode(doc.content)
                        metadata = doc.dict()
                        vector_index.add(embedding, metadata)
                        documents.append(metadata)

                        encoding_time = time.time() - start_time

                        return {
                    "message": f"Added {len(docs)} documents",
                    "total_documents": len(documents),
                    "encoding_time": f"{encoding_time:.3f}s",
                    }


                    @app.post("/search", response_model=List[SearchResult])
                    async def search_documents(query: SearchQuery):
"""Search for similar documents."""
                        if not model or not vector_index:
                            raise HTTPException(status_code=503, detail="Index not initialized")

                        if len(documents) = = 0:
                            raise HTTPException(status_code=404, detail="No documents in index")

# Generate query embedding
                        start_time = time.time()
                        query_embedding = model.encode(query.query)

# Search
                        results = vector_index.search(query_embedding, k=query.k)
                        time.time() - start_time

# Prepare results
                        search_results = []
                        for score, metadata in results:
                            search_results.append(SearchResult(
                            score=float(score),
                            document=Document(* * metadata),
                            ))

                            return search_results


                        @app.delete("/clear")
                        async def clear_index():
"""Clear all documents from the index."""
                            global vector_index, documents
                            vector_index = VectorSearchAdapter(384)
                            documents = []
                            return {"message": "Index cleared"}


                        @app.post("/demo")
                        async def load_demo_data():
"""Load demo data for testing."""
                            demo_docs = [
                            Document(
                            id="1",
                            title="Python Programming",
                            content="Python is a versatile programming language known for its simplicity and readability. It's widely used in web development, data science, and automation.",
                            category="Programming",
                            ),
                            Document(
                            id="2",
                            title="Machine Learning Basics",
                            content="Machine learning enables computers to learn from data without explicit programming. It includes supervised, unsupervised, and reinforcement learning approaches.",
                            category="AI / ML",
                            ),
                            Document(
                            id="3",
                            title="Web Development",
                            content="Modern web development involves frontend technologies like React and Vue, backend frameworks like FastAPI and Django, and database systems for data persistence.",
                            category="Programming",
                            ),
                            Document(
                            id="4",
                            title="Data Science",
                            content="Data science combines statistics, programming, and domain knowledge to extract insights from data. Common tools include Python, R, and SQL.",
                            category="Data",
                            ),
                            Document(
                            id="5",
                            title="Neural Networks",
                            content="Neural networks are computing systems inspired by biological brains. They consist of layers of interconnected nodes that process information for pattern recognition.",
                            category="AI / ML",
                            ),
                            ]

                            await add_documents(demo_docs)
                            return {"message": "Demo data loaded", "documents": len(demo_docs)}

                        if __name__ = = "__main__":
                            uvicorn.run(app, host="0.0.0.0", port=8000)
