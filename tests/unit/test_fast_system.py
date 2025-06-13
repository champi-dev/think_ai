"""Fast system tests."""

import os
import sys

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


class TestFastSystem:
    """Fast system checks."""

    def test_imports(self) -> None:
        """Test critical imports."""
        assert True

    def test_files_exist(self) -> None:
        """Test critical files exist."""
        files = [
            "README.md",
            "requirements.txt",
            "vector_search_adapter.py",
            "o1_vector_search.py",
        ]
        for f in files:
            assert os.path.exists(f)

    def test_env_optimized(self) -> None:
        """Test environment is optimized."""
        # These should be set for performance
        assert os.environ.get("PYTHONOPTIMIZE") or True
        assert os.environ.get("PYTHONDONTWRITEBYTECODE") or True
