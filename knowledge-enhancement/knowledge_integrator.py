#!/usr/bin/env python3
"""
Think AI - Knowledge Integrator

Integrates harvested knowledge into Think AI's knowledge base
with O(1) performance optimization.
"""

import json
import asyncio
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Set
from dataclasses import dataclass
import time
import re

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.table import Table

console = Console()


@dataclass
class ProcessedKnowledge:
    """Processed knowledge item for Think AI"""

    id: str
    title: str
    content: str
    summary: str
    keywords: List[str]
    source: str
    category: str
    confidence: float
    vector_hash: str
    metadata: Dict[str, Any]


class ThinkAIKnowledgeIntegrator:
    """Integrates harvested knowledge into Think AI system"""

    def __init__(
        self,
        harvest_dir: str = "./knowledge_harvest",
        output_dir: str = "./integrated_knowledge",
    ):
        self.harvest_dir = Path(harvest_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.processed_items: List[ProcessedKnowledge] = []
        self.knowledge_graph: Dict[str, Set[str]] = {}
        self.keyword_index: Dict[str, Set[str]] = {}

        # O(1) lookup structures
        self.title_hash_map: Dict[str, str] = {}
        self.content_hash_map: Dict[str, str] = {}

    def load_harvested_knowledge(self) -> List[Dict[str, Any]]:
        """Load all harvested knowledge from JSON files"""
        console.print("📂 Loading harvested knowledge...")

        knowledge_items = []

        # Load main knowledge base
        main_file = self.harvest_dir / "knowledge_base.json"
        if main_file.exists():
            with open(main_file, "r", encoding="utf-8") as f:
                knowledge_items.extend(json.load(f))

        # Load category files
        for json_file in self.harvest_dir.glob("*.json"):
            if json_file.name not in ["knowledge_base.json", "harvest_summary.json"]:
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        category_items = json.load(f)
                        # Add category to metadata if not present
                        category_name = json_file.stem.replace("_", " ").title()
                        for item in category_items:
                            if "category" not in item:
                                item["category"] = category_name
                        knowledge_items.extend(category_items)
                except Exception as e:
                    console.print(f"⚠️ Failed to load {json_file}: {e}")

        console.print(f"✅ Loaded {len(knowledge_items)} knowledge items")
        return knowledge_items

    def process_knowledge_items(self, raw_items: List[Dict[str, Any]]):
        """Process raw knowledge items for Think AI integration"""
        console.print(Panel("🔄 Processing Knowledge Items", style="blue"))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            console=console,
        ) as progress:

            task = progress.add_task("Processing items...", total=len(raw_items))

            for item in raw_items:
                try:
                    processed = self._process_single_item(item)
                    if processed:
                        self.processed_items.append(processed)
                        self._update_indexes(processed)

                    progress.advance(task)

                except Exception as e:
                    console.print(f"⚠️ Failed to process item: {e}")

        console.print(f"✅ Processed {len(self.processed_items)} items")

    def _process_single_item(self, item: Dict[str, Any]) -> ProcessedKnowledge:
        """Process a single knowledge item"""
        title = item.get("title", "").strip()
        content = item.get("content", "").strip()

        if not title or not content or len(content) < 50:
            return None

        # Generate unique ID
        item_id = self._generate_id(title, content)

        # Check for duplicates using O(1) hash lookup
        content_hash = self._hash_content(content)
        title_hash = self._hash_content(title)

        if content_hash in self.content_hash_map or title_hash in self.title_hash_map:
            return None  # Skip duplicate

        # Extract keywords
        keywords = self._extract_keywords(title, content)

        # Generate summary
        summary = self._generate_summary(content)

        # Calculate confidence based on source and content quality
        confidence = self._calculate_confidence(item)

        # Create vector hash for similarity matching
        vector_hash = self._create_vector_hash(content, keywords)

        processed = ProcessedKnowledge(
            id=item_id,
            title=title,
            content=content,
            summary=summary,
            keywords=keywords,
            source=item.get("source", "Unknown"),
            category=item.get("category", "General"),
            confidence=confidence,
            vector_hash=vector_hash,
            metadata=item.get("metadata", {}),
        )

        # Update hash maps for O(1) duplicate detection
        self.content_hash_map[content_hash] = item_id
        self.title_hash_map[title_hash] = item_id

        return processed

    def _generate_id(self, title: str, content: str) -> str:
        """Generate unique ID for knowledge item"""
        combined = f"{title}:{content[:100]}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def _hash_content(self, content: str) -> str:
        """Generate hash for content deduplication"""
        # Normalize content for better duplicate detection
        normalized = re.sub(r"\s+", " ", content.lower().strip())
        return hashlib.md5(normalized.encode()).hexdigest()

    def _extract_keywords(self, title: str, content: str) -> List[str]:
        """Extract keywords from title and content"""
        # Simple keyword extraction (can be enhanced with NLP)
        text = f"{title} {content}".lower()

        # Remove common words
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "from",
            "up",
            "about",
            "into",
            "over",
            "after",
            "beneath",
            "under",
            "above",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "can",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "it",
            "we",
            "they",
            "me",
            "him",
            "her",
            "us",
            "them",
            "my",
            "your",
            "his",
            "her",
            "its",
            "our",
            "their",
        }

        # Extract words (alphanumeric, 3+ characters)
        words = re.findall(r"\b[a-zA-Z0-9]{3,}\b", text)

        # Filter and score
        keyword_freq = {}
        for word in words:
            if word not in stop_words:
                keyword_freq[word] = keyword_freq.get(word, 0) + 1

        # Return top keywords
        sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_keywords[:20] if freq > 1]

    def _generate_summary(self, content: str) -> str:
        """Generate summary of content"""
        # Simple extractive summary (first sentences + key sentences)
        sentences = re.split(r"[.!?]+", content)

        if len(sentences) <= 3:
            return content[:500]

        # Take first 2 sentences + middle sentence + last sentence
        summary_sentences = []
        summary_sentences.append(sentences[0])

        if len(sentences) > 1:
            summary_sentences.append(sentences[1])

        if len(sentences) > 4:
            mid_idx = len(sentences) // 2
            summary_sentences.append(sentences[mid_idx])

        if len(sentences) > 2:
            summary_sentences.append(sentences[-2])

        summary = ". ".join(s.strip() for s in summary_sentences if s.strip())
        return summary[:500] + "..." if len(summary) > 500 else summary

    def _calculate_confidence(self, item: Dict[str, Any]) -> float:
        """Calculate confidence score for knowledge item"""
        confidence = 0.5  # Base confidence

        source = item.get("source", "").lower()

        # Source-based confidence
        if "wikipedia" in source:
            confidence += 0.3
        elif "arxiv" in source:
            confidence += 0.4
        elif "gutenberg" in source:
            confidence += 0.2
        elif "government" in source:
            confidence += 0.35

        # Content quality indicators
        content = item.get("content", "")
        if len(content) > 1000:
            confidence += 0.1
        if len(content) > 5000:
            confidence += 0.1

        # Metadata quality
        metadata = item.get("metadata", {})
        if metadata.get("pageviews", 0) > 1000:
            confidence += 0.05
        if metadata.get("downloads", 0) > 100:
            confidence += 0.05
        if len(metadata.get("authors", [])) > 0:
            confidence += 0.05

        return min(confidence, 1.0)

    def _create_vector_hash(self, content: str, keywords: List[str]) -> str:
        """Create vector hash for similarity matching"""
        # Simple vector representation using keywords
        keyword_str = " ".join(sorted(keywords))
        content_sample = content[:200]
        combined = f"{keyword_str}:{content_sample}"
        return hashlib.sha256(combined.encode()).hexdigest()[:32]

    def _update_indexes(self, item: ProcessedKnowledge):
        """Update O(1) lookup indexes"""
        # Keyword index
        for keyword in item.keywords:
            if keyword not in self.keyword_index:
                self.keyword_index[keyword] = set()
            self.keyword_index[keyword].add(item.id)

        # Knowledge graph (category connections)
        if item.category not in self.knowledge_graph:
            self.knowledge_graph[item.category] = set()

        # Connect related items by shared keywords
        for keyword in item.keywords:
            if keyword in self.keyword_index:
                for related_id in self.keyword_index[keyword]:
                    if related_id != item.id:
                        self.knowledge_graph[item.category].add(related_id)

    def build_knowledge_structures(self):
        """Build optimized knowledge structures for Think AI"""
        console.print(Panel("🏗️ Building Knowledge Structures", style="green"))

        # Build category statistics
        category_stats = {}
        for item in self.processed_items:
            cat = item.category
            if cat not in category_stats:
                category_stats[cat] = {
                    "count": 0,
                    "avg_confidence": 0.0,
                    "total_confidence": 0.0,
                    "sources": set(),
                    "top_keywords": {},
                }

            stats = category_stats[cat]
            stats["count"] += 1
            stats["total_confidence"] += item.confidence
            stats["sources"].add(item.source)

            # Count keywords
            for keyword in item.keywords:
                stats["top_keywords"][keyword] = (
                    stats["top_keywords"].get(keyword, 0) + 1
                )

        # Calculate averages
        for cat_stats in category_stats.values():
            cat_stats["avg_confidence"] = (
                cat_stats["total_confidence"] / cat_stats["count"]
            )
            cat_stats["sources"] = list(cat_stats["sources"])
            # Get top 10 keywords
            sorted_keywords = sorted(
                cat_stats["top_keywords"].items(), key=lambda x: x[1], reverse=True
            )
            cat_stats["top_keywords"] = dict(sorted_keywords[:10])

        # Save structures
        self._save_knowledge_structures(category_stats)

        console.print("✅ Knowledge structures built successfully")

    def _save_knowledge_structures(self, category_stats: Dict):
        """Save all knowledge structures to files"""
        # Main knowledge database
        knowledge_db = {
            "items": [
                {
                    "id": item.id,
                    "title": item.title,
                    "content": item.content,
                    "summary": item.summary,
                    "keywords": item.keywords,
                    "source": item.source,
                    "category": item.category,
                    "confidence": item.confidence,
                    "vector_hash": item.vector_hash,
                    "metadata": item.metadata,
                }
                for item in self.processed_items
            ],
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_items": len(self.processed_items),
        }

        with open(
            self.output_dir / "knowledge_database.json", "w", encoding="utf-8"
        ) as f:
            json.dump(knowledge_db, f, indent=2, ensure_ascii=False)

        # O(1) lookup indexes
        indexes = {
            "keyword_index": {k: list(v) for k, v in self.keyword_index.items()},
            "title_hash_map": self.title_hash_map,
            "content_hash_map": self.content_hash_map,
            "knowledge_graph": {k: list(v) for k, v in self.knowledge_graph.items()},
        }

        with open(
            self.output_dir / "knowledge_indexes.json", "w", encoding="utf-8"
        ) as f:
            json.dump(indexes, f, indent=2)

        # Category statistics
        with open(
            self.output_dir / "category_statistics.json", "w", encoding="utf-8"
        ) as f:
            json.dump(category_stats, f, indent=2, ensure_ascii=False)

        # Quick lookup tables
        quick_lookup = {
            "by_confidence": sorted(
                [
                    {"id": item.id, "title": item.title, "confidence": item.confidence}
                    for item in self.processed_items
                ],
                key=lambda x: x["confidence"],
                reverse=True,
            ),
            "by_category": {},
            "by_source": {},
        }

        # Group by category and source
        for item in self.processed_items:
            # By category
            if item.category not in quick_lookup["by_category"]:
                quick_lookup["by_category"][item.category] = []
            quick_lookup["by_category"][item.category].append(
                {"id": item.id, "title": item.title, "confidence": item.confidence}
            )

            # By source
            if item.source not in quick_lookup["by_source"]:
                quick_lookup["by_source"][item.source] = []
            quick_lookup["by_source"][item.source].append(
                {"id": item.id, "title": item.title, "confidence": item.confidence}
            )

        with open(self.output_dir / "quick_lookup.json", "w", encoding="utf-8") as f:
            json.dump(quick_lookup, f, indent=2, ensure_ascii=False)

    def generate_integration_report(self):
        """Generate comprehensive integration report"""
        console.print(Panel("📊 Generating Integration Report", style="cyan"))

        # Statistics
        total_items = len(self.processed_items)
        categories = set(item.category for item in self.processed_items)
        sources = set(item.source for item in self.processed_items)
        avg_confidence = (
            sum(item.confidence for item in self.processed_items) / total_items
            if total_items > 0
            else 0
        )

        # Top keywords
        all_keywords = {}
        for item in self.processed_items:
            for keyword in item.keywords:
                all_keywords[keyword] = all_keywords.get(keyword, 0) + 1

        top_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[
            :20
        ]

        # Create tables
        overview_table = Table(title="Integration Overview", show_header=True)
        overview_table.add_column("Metric", style="cyan")
        overview_table.add_column("Value", style="green", justify="right")

        overview_table.add_row("Total Knowledge Items", str(total_items))
        overview_table.add_row("Unique Categories", str(len(categories)))
        overview_table.add_row("Data Sources", str(len(sources)))
        overview_table.add_row("Average Confidence", f"{avg_confidence:.3f}")
        overview_table.add_row("Total Keywords", str(len(all_keywords)))

        console.print(overview_table)

        # Categories table
        category_table = Table(title="Knowledge by Category", show_header=True)
        category_table.add_column("Category", style="cyan")
        category_table.add_column("Items", style="green", justify="right")

        category_counts = {}
        for item in self.processed_items:
            category_counts[item.category] = category_counts.get(item.category, 0) + 1

        for category, count in sorted(
            category_counts.items(), key=lambda x: x[1], reverse=True
        ):
            category_table.add_row(category, str(count))

        console.print(category_table)

        # Sources table
        source_table = Table(title="Knowledge by Source", show_header=True)
        source_table.add_column("Source", style="cyan")
        source_table.add_column("Items", style="green", justify="right")

        source_counts = {}
        for item in self.processed_items:
            source_counts[item.source] = source_counts.get(item.source, 0) + 1

        for source, count in sorted(
            source_counts.items(), key=lambda x: x[1], reverse=True
        ):
            source_table.add_row(source, str(count))

        console.print(source_table)

        # Save report
        report = {
            "integration_summary": {
                "total_items": total_items,
                "categories": len(categories),
                "sources": len(sources),
                "average_confidence": avg_confidence,
                "integration_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "category_distribution": category_counts,
            "source_distribution": source_counts,
            "top_keywords": dict(top_keywords),
            "categories_list": list(categories),
            "sources_list": list(sources),
        }

        with open(
            self.output_dir / "integration_report.json", "w", encoding="utf-8"
        ) as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        console.print(
            Panel(
                f"✅ Integration completed successfully!\n"
                f"📁 Output directory: {self.output_dir}\n"
                f"📊 Processed {total_items} knowledge items\n"
                f"🎯 Average confidence: {avg_confidence:.3f}\n"
                f"📚 Categories: {len(categories)}\n"
                f"🔗 Sources: {len(sources)}",
                title="Integration Complete",
                style="bold green",
            )
        )


async def main():
    """Main integration function"""
    console.print(
        Panel(
            "🧠 Think AI - Knowledge Integration System\n"
            "Integrating harvested knowledge into Think AI...",
            title="Knowledge Integration",
            style="bold blue",
        )
    )

    integrator = ThinkAIKnowledgeIntegrator()

    try:
        # Load harvested knowledge
        raw_items = integrator.load_harvested_knowledge()

        if not raw_items:
            console.print("❌ No harvested knowledge found. Run the harvester first.")
            return

        # Process items
        integrator.process_knowledge_items(raw_items)

        # Build knowledge structures
        integrator.build_knowledge_structures()

        # Generate report
        integrator.generate_integration_report()

    except Exception as e:
        console.print(
            Panel(f"❌ Integration failed: {str(e)}", title="Error", style="bold red")
        )
        raise


if __name__ == "__main__":
    asyncio.run(main())
