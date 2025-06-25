"""Automatically load pre-trained knowledge for all Think AI users."""

import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from ..utils.logging import get_logger

logger = get_logger(__name__)


class KnowledgeLoader:
    """Load pre-trained knowledge automatically."""

    def __init__(self):
        self.knowledge_dir = Path(__file__).parent.parent / "data" / "knowledge"
        self.loaded_packages = set()
        self.qa_index = {}
        self.embeddings = None
        self.categories = {}

    def load_knowledge(self) -> bool:
        """Load all available knowledge packages."""
        if not self.knowledge_dir.exists():
            logger.info("No pre-trained knowledge found. Run train_massive_knowledge.py first.")
            return False

        # Load manifest
        manifest_path = self.knowledge_dir / "manifest.json"
        if not manifest_path.exists():
            logger.warning("Knowledge manifest not found")
            return False

        with open(manifest_path) as f:
            manifest = json.load(f)

        logger.info(f"Loading knowledge version {manifest['version']} with {manifest['total_pairs']:,} Q&A pairs")

        # Load embeddings
        self._load_embeddings()

        # Load categories
        self._load_categories()

        # Load packages on-demand
        self.manifest = manifest

        logger.info("Knowledge system ready!")
        return True

    def _load_embeddings(self):
        """Load embeddings index."""
        embeddings_path = self.knowledge_dir / "embeddings.npz"
        if embeddings_path.exists():
            data = np.load(embeddings_path)
            self.embeddings = data["embeddings"]
            logger.info(f"Loaded embeddings with shape {self.embeddings.shape}")

    def _load_categories(self):
        """Load category index."""
        categories_path = self.knowledge_dir / "categories.json.gz"
        if categories_path.exists():
            with gzip.open(categories_path, "rt") as f:
                self.categories = json.load(f)
            logger.info(f"Loaded {len(self.categories)} category indexes")

    def get_answer(self, question: str) -> Optional[str]:
        """Get answer for a question using loaded knowledge."""
        # First check persistent intelligence
        from .persistent_intelligence import persistent_intelligence

        # Search persistent knowledge first
        persistent_results = persistent_intelligence.get_knowledge(question, limit=1)
        if persistent_results:
            return persistent_results[0]["answer"]

        # Then try exact match from pre-trained
        question_hash = hashlib.md5(question.encode()).hexdigest()
        if question_hash in self.qa_index:
            return self.qa_index[question_hash]

        # Try semantic search if embeddings available
        if self.embeddings is not None:
            similar_idx = self._find_similar_question(question)
            if similar_idx is not None:
                return self._get_answer_by_index(similar_idx)

        # Try category-based search
        categories = self._detect_categories(question)
        for category in categories:
            if category in self.categories:
                # Load relevant package if needed
                for item in self.categories[category][:10]:  # Check top 10
                    answer = self._get_answer_by_index(item["index"])
                    if answer:
                        return answer

        return None

    def _find_similar_question(self, question: str) -> Optional[int]:
        """Find similar question using embeddings."""
        # Extract features
        features = self._extract_features(question)

        # Compute similarities
        similarities = np.dot(self.embeddings, features)

        # Get best match
        best_idx = np.argmax(similarities)
        if similarities[best_idx] > 0.7:  # Threshold
            return int(best_idx)

        return None

    def _extract_features(self, text: str, dim: int = 384) -> np.ndarray:
        """Extract features (same as packager)."""
        words = text.lower().split()
        features = np.zeros(dim, dtype=np.float32)

        for word in words:
            for i in range(3):
                idx = hash(word + str(i)) % dim
                features[idx] += 1.0

        norm = np.linalg.norm(features)
        if norm > 0:
            features /= norm

        return features

    def _get_answer_by_index(self, idx: int) -> Optional[str]:
        """Get answer by global index."""
        # Find which package contains this index
        for package_info in self.manifest["packages"]:
            if package_info["index_start"] <= idx < package_info["index_end"]:
                # Load package if not already loaded
                if package_info["id"] not in self.loaded_packages:
                    self._load_package(package_info)

                # Get answer from loaded data
                local_idx = idx - package_info["index_start"]
                package_data = self.package_cache.get(package_info["id"])
                if package_data and local_idx < len(package_data["qa_pairs"]):
                    return package_data["qa_pairs"][local_idx][1]

        return None

    def _load_package(self, package_info: Dict):
        """Load a specific knowledge package."""
        package_path = self.knowledge_dir / package_info["file"]

        with gzip.open(package_path, "rt") as f:
            package_data = json.load(f)

        # Cache the package
        if not hasattr(self, "package_cache"):
            self.package_cache = {}

        self.package_cache[package_info["id"]] = package_data
        self.loaded_packages.add(package_info["id"])

        # Index Q&A pairs for fast lookup
        for question, answer in package_data["qa_pairs"]:
            question_hash = hashlib.md5(question.encode()).hexdigest()
            self.qa_index[question_hash] = answer

    def _detect_categories(self, text: str) -> List[str]:
        """Detect categories from text."""
        categories = []
        text_lower = text.lower()

        category_keywords = {
            "programming": ["code", "function", "algorithm", "programming", "software"],
            "science": ["physics", "chemistry", "biology", "science", "experiment"],
            "mathematics": ["math", "equation", "calculate", "algebra", "calculus"],
            "technology": ["computer", "internet", "software", "hardware", "tech"],
            "ai": ["artificial intelligence", "machine learning", "neural", "ai", "ml"],
        }

        for category, keywords in category_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)

        return categories if categories else ["general"]

    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about loaded knowledge."""
        return {
            "total_pairs": self.manifest.get("total_pairs", 0) if hasattr(self, "manifest") else 0,
            "loaded_packages": len(self.loaded_packages),
            "cached_answers": len(self.qa_index),
            "categories": len(self.categories),
            "has_embeddings": self.embeddings is not None,
        }


# Global knowledge loader instance
knowledge_loader = KnowledgeLoader()
