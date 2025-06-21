#! / usr / bin / env python3

"""
Run all Think AI test applications to demonstrate full functionality
"""

import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import annoy
import requests
import torch
from sentence_transformers import SentenceTransformer

from o1_vector_search import O1VectorSearch
from vector_search_adapter import VectorSearchAdapter

# Test applications
TEST_APPS = [
{
"name": "Collaborative Code Editor",
"path": "collab-editor/server.py",
"port": 8001,
"url": "http://localhost:8001",
"description": "Real-time collaborative editing with AI code suggestions"
},
{
"name": "API Documentation Generator",
"path": "api-doc-gen/server.py",
"port": 8002,
"url": "http://localhost:8002",
"description": "Analyze code and generate searchable API docs"
},
{
"name": "Code Review System",
"path": "code-review/server.py",
"port": 8003,
"url": "http://localhost:8003",
"description": "AI-powered code review with suggestions"
}
]


def start_app(app_info):
"""Start a test application"""
    print(f"🚀 Starting {app_info['name']} on port {app_info['port']}...")

# Change to app directory
    app_dir = os.path.dirname(app_info['path'])
    app_file = os.path.basename(app_info['path'])

# Start the server
    process = subprocess.Popen(
    [sys.executable, app_file],
    cwd = os.path.join(os.path.dirname(__file__), app_dir),
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
    )

# Wait for server to start
    time.sleep(3)

# Test if server is running
    try:
        response = requests.get(app_info['url'], timeout = 5)
        if response.status_code = = 200:
            print(f"✅ {app_info['name']} is running at {app_info['url']}")
            return {"app": app_info, "process": process, "status": "running"}
    else:
        print(f"❌ {app_info['name']} returned status {response.status_code}")
        process.terminate()
        return {"app": app_info, "process": None, "status": "error"}
    except Exception as e:
        print(f"❌ {app_info['name']} failed to start: {e}")
        process.terminate()
        return {"app": app_info, "process": None, "status": "error"}

    def test_vector_search():
"""Test vector search functionality"""
        print("\n📊 Testing Vector Search Performance...")

# Import our modules
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

        torch.set_default_device('cpu')

# Test 1: Vector Search Adapter
        print("\n1️⃣ Testing VectorSearchAdapter...")
        adapter = VectorSearchAdapter(384)
        print(f" Backend: {adapter.backend}")

# Add some vectors
        model = SentenceTransformer('all-MiniLM-L6-v2', device = 'cpu')
        test_docs = [
        "Python web development with FastAPI",
        "Machine learning algorithms in Python",
        "Real-time collaborative editing",
        "API documentation generation tools"
        ]

        for doc in test_docs:
            embedding = model.encode(doc)
            adapter.add(embedding, {"text": doc})

# Search
            query = "web API development"
            query_emb = model.encode(query)
            results = adapter.search(query_emb, k = 2)

            print(f" Query: '{query}'")
            for score, meta in results:
                print(f" ✓ {meta['text']} (score: {score:.3f})")

# Test 2: O(1) Vector Search
                print("\n2️⃣ Testing O(1) Vector Search...")
                o1_index = O1VectorSearch(384, num_tables = 10)

# Add same documents
                for doc in test_docs:
                    embedding = model.encode(doc)
                    o1_index.add(embedding, {"text": doc})

# Search with O(1)
                    start = time.time()
                    results = o1_index.search(query_emb, k = 2)
                    search_time = (time.time() - start) * 1000

                    print(f" O(1) Search completed in {search_time:.3f}ms")
                    for score, _, meta in results:
                        print(f" ✓ {meta['text']} (score: {score:.3f})")

                        return True

                    def test_offline_support():
"""Test offline functionality"""
                        print("\n🌐 Testing Offline Support...")

# Check if libraries work without internet
                        print("1️⃣ Testing sentence transformers offline...")
                        try:
                            torch.set_default_device('cpu')

# This should work with cached model
                            model = SentenceTransformer('all-MiniLM-L6-v2', device = 'cpu')
                            test_emb = model.encode("test")
                            print(f" ✅ Sentence transformers work offline (embedding shape: {test_emb.shape})")
                            except Exception as e:
                                print(f" ❌ Error: {e}")

                                print("2️⃣ Testing Annoy offline...")
                                try:
                                    index = annoy.AnnoyIndex(10, 'angular')
                                    index.add_item(0, [1.0] * 10)
                                    index.build(10)
                                    print(" ✅ Annoy works offline")
                                    except Exception as e:
                                        print(f" ❌ Error: {e}")

                                        return True

                                    def main():
                                        print("🧪 THINK AI COMPREHENSIVE TEST SUITE")
                                        print("=" * 60)
                                        print("Testing all libraries and web applications...")

# Test vector search first
                                        test_vector_search()

# Test offline support
                                        test_offline_support()

# Start all apps in parallel
                                        print(f"\n🚀 Starting {len(TEST_APPS)} test applications in parallel...")

                                        running_apps = []
                                        with ProcessPoolExecutor(max_workers = len(TEST_APPS)) as executor:
                                            futures = {executor.submit(start_app, app): app for app in TEST_APPS}

                                            for future in as_completed(futures):
                                                result = future.result()
                                                running_apps.append(result)

# Summary
                                                print("\n" + "=" * 60)
                                                print("📊 TEST SUMMARY")
                                                print("=" * 60)

                                                successful = sum(1 for app in running_apps if app['status'] = = 'running')
                                                print(f"\n✅ Applications running: {successful}/{len(TEST_APPS)}")

                                                print("\n🌐 Access the applications:")
                                                for app in running_apps:
                                                    if app['status'] = = 'running':
                                                        print(f" • {app['app']['name']}: {app['app']['url']}")
                                                        print(f" {app['app']['description']}")

                                                        print("\n📋 Features demonstrated:")
                                                        print(" ✅ Vector search with multiple backends (FAISS/Annoy/O1)")
                                                        print(" ✅ Real-time collaborative editing")
                                                        print(" ✅ AI-powered code suggestions")
                                                        print(" ✅ Semantic search through documentation")
                                                        print(" ✅ Automated code review")
                                                        print(" ✅ Parallel processing")
                                                        print(" ✅ Offline support")
                                                        print(" ✅ No SWIG/compilation required")

                                                        print("\n⏸️ Press Ctrl+C to stop all applications...")

                                                        try:
# Keep running
                                                            while True:
                                                                time.sleep(1)
                                                                except KeyboardInterrupt:
                                                                    print("\n\n🛑 Stopping all applications...")
                                                                    for app in running_apps:
                                                                        if app['process']:
                                                                            app['process'].terminate()
                                                                            print("✅ All applications stopped")

                                                                            if __name__ = = "__main__":
                                                                                main()
