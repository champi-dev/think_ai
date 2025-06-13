"""Alternative core using Annoy for environments without FAISS."""

import json
import os
from typing import Dict, List, Optional, Tuple

import torch
from annoy import AnnoyIndex
from sentence_transformers import SentenceTransformer

# Force CPU usage
torch.set_default_device("cpu")


class ThinkAI:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        """Initialize ThinkAI with Annoy vector search."""
        self.model = SentenceTransformer(model_name, device="cpu")
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.code_snippets = []
        self.metadata = []
        self.knowledge_base_path = os.path.expanduser("~/.think-ai/knowledge.json")
        self.index_path = os.path.expanduser("~/.think-ai/index.ann")
        self._ensure_dirs()
        self._load_knowledge_base()

    def _ensure_dirs(self) -> None:
        """Ensure necessary directories exist."""
        os.makedirs(os.path.dirname(self.knowledge_base_path), exist_ok=True)

    def _load_knowledge_base(self) -> None:
        """Load existing knowledge base."""
        if os.path.exists(self.knowledge_base_path):
            with open(self.knowledge_base_path) as f:
                data = json.load(f)
                self.code_snippets = data.get("snippets", [])
                self.metadata = data.get("metadata", [])

        # Load Annoy index
        if os.path.exists(self.index_path) and self.code_snippets:
            self.index = AnnoyIndex(self.dimension, "angular")
            self.index.load(self.index_path)
        else:
            self._rebuild_index()

    def _save_knowledge_base(self) -> None:
        """Save knowledge base to disk."""
        data = {
            "snippets": self.code_snippets,
            "metadata": self.metadata,
        }
        with open(self.knowledge_base_path, "w") as f:
            json.dump(data, f, indent=2)

        # Save Annoy index
        if self.index and len(self.code_snippets) > 0:
            self.index.save(self.index_path)

    def _rebuild_index(self) -> None:
        """Rebuild Annoy index from snippets."""
        self.index = AnnoyIndex(self.dimension, "angular")

        if not self.code_snippets:
            return

        embeddings = self.model.encode(self.code_snippets)

        for i, embedding in enumerate(embeddings):
            self.index.add_item(i, embedding)

        # Build the index
        self.index.build(10)  # 10 trees

    def add_code(
        self,
        code: str,
        language: str,
        description: str,
        tags: Optional[List[str]] = None,
    ):
        """Add code snippet to knowledge base."""
        idx = len(self.code_snippets)
        self.code_snippets.append(code)
        self.metadata.append(
            {
                "language": language,
                "description": description,
                "tags": tags or [],
                "length": len(code),
            }
        )

        # Rebuild index (Annoy requires rebuild for new items)
        self._rebuild_index()

        self._save_knowledge_base()
        return idx

    def search(self, query: str, k: int = 5) -> List[Tuple[float, str, Dict]]:
        """Search for similar code snippets."""
        if not self.index or len(self.code_snippets) == 0:
            return []

        query_embedding = self.model.encode([query])[0]

        # Get nearest neighbors
        indices, distances = self.index.get_nns_by_vector(
            query_embedding,
            min(k, len(self.code_snippets)),
            include_distances=True,
        )

        results = []
        for idx, dist in zip(indices, distances):
            # Convert angular distance to similarity score
            score = 1 - (dist / 2)  # Angular distance to similarity
            results.append(
                (
                    score,
                    self.code_snippets[idx],
                    self.metadata[idx],
                )
            )

        return results

    def generate_code(self, prompt: str, language: str = "python") -> str:
        """Generate code based on prompt and similar examples."""
        # Search for similar code
        similar = self.search(prompt, k=3)

        # Build context from similar code
        context = []
        for score, code, meta in similar:
            if score > 0.5:  # Only use highly relevant examples
                context.append(f"# {meta['description']}\n{code}")

        # For now, return a template based on similar code
        if context:
            return f"""# Generated based on: {prompt}
# Similar examples found:

{chr(10).join(context[:2])}

# Your implementation here:
def implement_{language}_solution():
    # TODO: Implement based on the examples above
    pass
"""
        return f"""# Generated for: {prompt}
# Language: {language}

def implement_solution():
    # TODO: No similar examples found
    # Start with a basic implementation
    pass
"""

    def analyze_code(self, code: str) -> Dict:
        """Analyze code for patterns and suggestions."""
        # Find similar code
        similar = self.search(code, k=3)

        analysis = {
            "length": len(code),
            "lines": code.count("\n") + 1,
            "similar_patterns": [],
            "suggestions": [],
        }

        for score, _similar_code, meta in similar:
            if score > 0.7:
                analysis["similar_patterns"].append(
                    {
                        "description": meta["description"],
                        "similarity": f"{score*100:.1f}%",
                        "language": meta["language"],
                    }
                )

        # Basic suggestions
        if "TODO" in code or "FIXME" in code:
            analysis["suggestions"].append("Complete TODO/FIXME items")

        if not any(word in code.lower() for word in ["test", "assert", "expect"]):
            analysis["suggestions"].append("Consider adding tests")

        return analysis

    def get_stats(self) -> Dict:
        """Get knowledge base statistics."""
        if not self.metadata:
            return {"total_snippets": 0}

        languages = {}
        total_lines = 0

        for meta in self.metadata:
            lang = meta["language"]
            languages[lang] = languages.get(lang, 0) + 1
            total_lines += meta["length"]

        return {
            "total_snippets": len(self.code_snippets),
            "total_characters": total_lines,
            "languages": languages,
            "index_size": len(self.code_snippets),
        }
