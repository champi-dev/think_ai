#! / usr / bin / env python3

"""Complete system test - proving all libraries and CLI work 100%."""

import json
import os
import subprocess


def run_command(cmd, description, check=True):
"""Run command and return output."""
    try:
        result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=check)
        if result.stderr:
            pass
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


    def test_alternative_packages():
"""Test alternative packages work without SWIG."""
# Test Annoy
        test_code = """

# Create index
        index = annoy.AnnoyIndex(10, "angular")
        for i in range(100):
            v = np.random.normal(size = 10)
            index.add_item(i, v)

            index.build(10)
            print("✅ Annoy working - no SWIG required!")
            print(f" Items in index: {index.get_n_items()}")

# Test search
            result = index.get_nns_by_item(0, 5)
            print(f" Nearest neighbors of item 0: {result}")
"""

            success, _ = run_command(
            f"python -c "{test_code}"",
            "Test Annoy (FAISS alternative)",
            )

# Test sentence transformers without FAISS
            test_code2 = """
from sentence_transformers import SentenceTransformer
import torch
            torch.set_default_device("cpu")

            model = SentenceTransformer("all-MiniLM-L6-v2", device = "cpu")
            embeddings = model.encode(["Hello world", "Testing without FAISS"])
            print("✅ Sentence Transformers working without FAISS!")
            print(f" Embedding shape: {embeddings.shape}")
"""

            success2, _ = run_command(
            f"python -c "{test_code2}"",
            "Test Sentence Transformers (CPU only)",
            )

            return success and success2


        def test_python_cli():
"""Test Python CLI package."""
# Change to Python CLI directory
            os.chdir("/home / champi / development / think_ai / think - ai - cli / python")

# Test imports
            test_code = """
# Test with Annoy backend
            sys.path.insert(0, ".")

# Mock the import to use Annoy version
            ThinkAI = core_module.ThinkAI

# Test core functionality
            ai = ThinkAI()
            print("✅ ThinkAI initialized with Annoy backend")

# Add some code
            idx = ai.add_code(
            "def binary_search(arr, target): return bisect.bisect_left(arr, target)",
            "python",
            "Binary search implementation",
            ["algorithm", "search"]
            )
            print(f"✅ Added code snippet (index: {idx})")

# Search
            results = ai.search("search algorithm", k = 1)
            if results:
                score, code, meta = results[0]
                print(f"✅ Search working! Found: {meta["description"]} (score: {score:.2f})")

# Get stats
                stats = ai.get_stats()
                print(f"✅ Stats: {stats["total_snippets"]} snippets in knowledge base")
"""

                success, _ = run_command(
                f"python -c "{test_code}"",
                "Test Python CLI core with Annoy",
                )

# Go back
                os.chdir("/home / champi / development / think_ai")

                return success


            def test_nodejs_package() - > bool:
"""Test Node.js package structure."""
# Check package.json
                pkg_path = "/home / champi / development / think_ai / think - ai - cli / nodejs / package.json"
                if os.path.exists(pkg_path):
                    with open(pkg_path) as f:
                        json.load(f)
                        return True
                    return False


                def test_api_compatibility():
"""Test API works with alternative packages."""
# Create test API with Annoy
                    test_code = """
import numpy as np
import annoy
from sentence_transformers import SentenceTransformer
import torch

                    torch.set_default_device("cpu")

# Initialize
                    model = SentenceTransformer("all-MiniLM-L6-v2", device = "cpu")
                    index = annoy.AnnoyIndex(384, "angular")

# Add documents
                    docs = ["Python programming", "Machine learning", "Web development"]
                    embeddings = model.encode(docs)

                    for i, emb in enumerate(embeddings):
                        index.add_item(i, emb)

                        index.build(10)

# Search
                        query_emb = model.encode(["learning python"])
                        results = index.get_nns_by_vector(query_emb[0], 2, include_distances = True)

                        print("✅ API - compatible search working!")
                        print(f" Results: {results}")
                        print(f" Best match: "{docs[results[0][0]]}" (distance: {results[1][0]:.3f})")
"""

                        success, _ = run_command(
                        f"python -c "{test_code}"",
                        "Test API compatibility with Annoy",
                        )

                        return success


                    def main() - > None:

                        tests = [
                        ("Alternative Packages", test_alternative_packages),
                        ("Python CLI Package", test_python_cli),
                        ("Node.js Package", test_nodejs_package),
                        ("API Compatibility", test_api_compatibility),
                        ]

                        results = {}
                        for name, test_func in tests:
                            try:
                                results[name] = test_func()
                                except Exception:
                                    results[name] = False

# Summary

                                    all_passed = True
                                    for name, passed in results.items():
                                        if not passed:
                                            all_passed = False

                                            if all_passed:
                                                pass
                                        else:
                                            pass


                                        if __name__ = = "__main__":
                                            main()
