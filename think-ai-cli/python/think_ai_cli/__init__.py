"""
Think AI CLI - AI-powered coding assistant
"""

try:
    from .core import ThinkAI as _ThinkAI
except ImportError:
    # Fallback to Annoy if FAISS not available
    from .core_annoy import ThinkAI as _ThinkAI

from .cli import main


class ThinkAI(_ThinkAI):
    """Wrapper to provide test-compatible interface."""

    def add(self, text: str, metadata: dict = None):
        """Add text with metadata - test compatible interface."""
        # Extract metadata or use defaults
        if metadata is None:
            metadata = {}

        language = metadata.get("language", "python")
        description = metadata.get("source", "Added via API")
        tags = metadata.get("tags", [])

        # Call the underlying add_code method
        idx = self.add_code(text, language, description, tags)

        # Return test-expected format
        return {"status": "added", "index": idx}

    def search(self, query: str, k: int = 5):
        """Search with test-compatible return format."""
        # Call parent search method
        results = super().search(query, k)

        # Transform results to test-expected format
        formatted_results = []
        for score, code, meta in results:
            formatted_results.append({"score": score, "text": code, "metadata": meta})

        return formatted_results

    def analyze(self, code: str):
        """Analyze code with test-compatible return format."""
        # Call parent analyze_code method
        analysis = self.analyze_code(code)

        # Add structure key for test compatibility
        analysis["structure"] = {
            "lines": analysis["lines"],
            "length": analysis["length"],
            "patterns": len(analysis.get("similar_patterns", [])),
        }

        return analysis

    def generate(self, prompt: str, language: str = "python"):
        """Generate code with test-compatible interface."""
        return self.generate_code(prompt, language)


__version__ = "0.2.0"
__author__ = "Think AI"

__all__ = ["ThinkAI", "main"]
