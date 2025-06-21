"""Test dependency installation with graceful handling of optional dependencies."""

import sys


def test_core_imports():
    """Test that core dependencies can be imported."""
    print("Testing core imports...")

    # Test core required dependencies
    core_deps = [
        ("numpy", "numpy"),
        ("torch", "torch"),
        ("transformers", "transformers"),
        ("fastapi", "fastapi"),
    ]

    for name, module in core_deps:
        try:
            __import__(module)
            print(f"✓ {name} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {name}: {e}")
            return False

    # Test optional dependencies with graceful fallback
    optional_deps = [
        ("faiss", "faiss"),
        ("chromadb", "chromadb"),
        ("aiosqlite", "aiosqlite"),
    ]

    for name, module in optional_deps:
        try:
            __import__(module)
            print(f"✓ {name} available (optional)")
        except ImportError:
            print(f"ℹ {name} not available (using fallback)")

    return True


def test_think_ai_imports():
    """Test Think AI core module imports."""
    print("\nTesting Think AI imports...")

    # Test core Think AI modules
    try:
        from think_ai.storage.fast_vector_db import FastVectorDB

        print("✓ FastVectorDB imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import FastVectorDB: {e}")
        return False

    try:
        from think_ai.intelligence_optimizer import intelligence_optimizer

        print("✓ Intelligence optimizer imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import intelligence_optimizer: {e}")
        return False

    try:
        from think_ai.core.engine import ThinkAIEngine

        print("✓ ThinkAIEngine imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ThinkAIEngine: {e}")
        return False

    return True


def test_vector_db():
    """Test vector database functionality."""
    print("\nTesting vector database...")

    try:
        import numpy as np

        from think_ai.storage.fast_vector_db import FastVectorDB

        # Create a vector DB instance
        db = FastVectorDB(dimension=128)

        # Add some test vectors
        vectors = np.random.randn(10, 128).astype(np.float32)
        ids = [f"test_{i}" for i in range(10)]
        metadata = [{"index": i} for i in range(10)]

        db.add_vectors(vectors, ids, metadata)
        print("✓ Added vectors successfully")

        # Search for similar vectors
        query = np.random.randn(128).astype(np.float32)
        results = db.search(query, top_k=5)
        print(f"✓ Search returned {len(results)} results")

        return True

    except Exception as e:
        print(f"✗ Vector database test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing Think AI dependency installation...\n")

    # Test core imports
    if not test_core_imports():
        print("\n❌ Core import tests failed!")
        sys.exit(1)

    # Test Think AI imports
    if not test_think_ai_imports():
        print("\n❌ Think AI import tests failed!")
        sys.exit(1)

    # Test vector DB
    if not test_vector_db():
        print("\n❌ Vector database tests failed!")
        sys.exit(1)

    print("\n✅ All tests passed! Dependencies are working correctly.")
    return True


if __name__ == "__main__":
    main()
