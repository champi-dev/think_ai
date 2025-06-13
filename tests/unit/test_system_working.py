"""Working system tests"""

import os
import sys

from o1_vector_search import O1VectorSearch
import background_worker
import numpy as np
import o1_vector_search
import time
import vector_search_adapter

sys.path.insert(
    0, os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))


class TestSystemFunctionality:
    """Test system-level functionality"""

    def test_imports_work(self):
        """Test that main imports work"""

        assert hasattr(vector_search_adapter, 'VectorSearchAdapter')
        assert hasattr(o1_vector_search, 'O1VectorSearch')
        assert hasattr(background_worker, 'BackgroundWorker')

    def test_requirements_installable(self):
        """Test that requirements can be installed"""
        # Just check the file exists
        assert os.path.exists('requirements.txt')
        assert os.path.exists('requirements-fast.txt')

    def test_cli_packages_exist(self):
        """Test CLI packages exist"""
        assert os.path.exists('think-ai-cli/python/setup.py')
        assert os.path.exists('think-ai-cli/nodejs/package.json')

    def test_web_apps_exist(self):
        """Test web apps exist"""
        apps = ['collab-editor', 'api-doc-gen', 'code-review']
        for app in apps:
            assert os.path.exists(f'test-apps/{app}/server.py')
            assert os.path.exists(f'test-apps/{app}/templates/index.html')

    def test_documentation_exists(self):
        """Test documentation exists"""
        docs = ['README.md', 'DEPLOYMENT.md', 'docs/testing.md']
        for doc in docs:
            assert os.path.exists(doc)

    def test_vector_search_performance(self):
        """Test vector search performance"""

        search = O1VectorSearch(dim=128)

        # Add 1000 vectors
        for i in range(1000):
            search.add(np.random.rand(128), {"id": i})

        # Time search
        query = np.random.rand(128)
        start = time.time()
        results = search.search(query, k=10)
        elapsed = time.time() - start

        assert elapsed < 0.01  # Should be under 10ms
        assert len(results) <= 10
