"""Package and distribute Think AI's trained knowledge for all users."""

import gzip
import hashlib
import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from ..utils.logging import get_logger

logger = get_logger(__name__)


class KnowledgePackager:
    """Package trained knowledge for distribution."""

    def __init__(self):
        self.knowledge_dir = Path(__file__).parent.parent / "data" / "knowledge"
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)

    def create_knowledge_packages(self, qa_pairs: List[tuple], chunk_size: int = 10000):
        """Create distributable knowledge packages."""
        logger.info(f"Creating knowledge packages from {len(qa_pairs):,} Q&A pairs...")

        # Create manifest
        manifest = {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "total_pairs": len(qa_pairs),
            "packages": [],
        }

        # Split into chunks for efficient loading
        for i in range(0, len(qa_pairs), chunk_size):
            chunk = qa_pairs[i : i + chunk_size]
            package_id = f"knowledge_pack_{i // chunk_size:04d}"

            # Create package
            package_data = {
                "id": package_id,
                "qa_pairs": chunk,
                "index_start": i,
                "index_end": i + len(chunk),
                "checksum": self._calculate_checksum(chunk),
            }

            # Compress and save
            package_path = self.knowledge_dir / f"{package_id}.json.gz"
            with gzip.open(package_path, "wt", encoding="utf-8") as f:
                json.dump(package_data, f)

            manifest["packages"].append(
                {
                    "id": package_id,
                    "file": f"{package_id}.json.gz",
                    "size": package_path.stat().st_size,
                    "pairs": len(chunk),
                    "checksum": package_data["checksum"],
                }
            )

            if (i + chunk_size) % 100000 == 0:
                logger.info(f"Packaged {i + chunk_size:,} Q&A pairs...")

        # Save manifest
        manifest_path = self.knowledge_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        logger.info(f"Created {len(manifest['packages'])} knowledge packages")
        return manifest

    def _calculate_checksum(self, data: List[tuple]) -> str:
        """Calculate checksum for data integrity."""
        content = json.dumps(data, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def create_embeddings_index(self, qa_pairs: List[tuple]):
        """Create searchable embeddings index."""
        logger.info("Creating embeddings index...")

        # Create lightweight embeddings using hash-based approach
        embeddings = []
        for question, answer in qa_pairs:
            # Create feature vector from text
            features = self._extract_features(question + " " + answer)
            embeddings.append(features)

        # Save as numpy array for fast loading
        embeddings_array = np.array(embeddings, dtype=np.float32)
        np.savez_compressed(
            self.knowledge_dir / "embeddings.npz", embeddings=embeddings_array, shape=embeddings_array.shape
        )

        logger.info(f"Created embeddings index with shape {embeddings_array.shape}")

    def _extract_features(self, text: str, dim: int = 384) -> np.ndarray:
        """Extract features using lightweight method."""
        # Simple but effective feature extraction
        words = text.lower().split()
        features = np.zeros(dim, dtype=np.float32)

        for word in words:
            # Hash word to multiple positions
            for i in range(3):
                idx = hash(word + str(i)) % dim
                features[idx] += 1.0

        # Normalize
        norm = np.linalg.norm(features)
        if norm > 0:
            features /= norm

        return features

    def create_category_index(self, qa_pairs: List[tuple]):
        """Create category-based index for fast lookup."""
        logger.info("Creating category index...")

        categories_index = {}

        for i, (question, answer) in enumerate(qa_pairs):
            # Detect categories
            detected_categories = self._detect_categories(question)

            for category in detected_categories:
                if category not in categories_index:
                    categories_index[category] = []

                categories_index[category].append(
                    {
                        "index": i,
                        "question": question[:100],  # Store preview
                        "type": self._detect_question_type(question),
                    }
                )

        # Save category index
        with gzip.open(self.knowledge_dir / "categories.json.gz", "wt") as f:
            json.dump(categories_index, f)

        logger.info(f"Indexed {len(categories_index)} categories")

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

    def _detect_question_type(self, question: str) -> str:
        """Detect question type."""
        q_lower = question.lower()
        if q_lower.startswith(("what is", "define")):
            return "definition"
        elif q_lower.startswith("how"):
            return "how_to"
        elif q_lower.startswith("why"):
            return "explanation"
        elif "code" in q_lower:
            return "coding"
        return "general"
