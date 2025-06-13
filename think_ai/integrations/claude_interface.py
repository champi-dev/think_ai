"""Claude integration with token optimization and transparency."""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from think_ai.consciousness.principles import ConstitutionalAI
from think_ai.persistence.eternal_memory import EternalMemory
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


class ClaudeInterface:
    """Interface for Claude integration with token optimization.

    Designed for users who need to minimize costs while maintaining
    meaningful conversations with Claude.
    """

    def __init__(
        self,
        memory: EternalMemory,
        ethics: ConstitutionalAI,
        reports_dir: Optional[Path] = None,
    ) -> None:
        self.memory = memory
        self.ethics = ethics
        self.reports_dir = reports_dir or Path.home() / ".think_ai" / "claude_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        # Token optimization settings
        self.max_context_size = 2000  # Keep context small
        self.summary_threshold = 1000  # Summarize after this many tokens
        self.compression_ratio = 0.3  # Target 70% reduction

        # Conversation tracking
        self.active_conversations: Dict[str, Dict[str, Any]] = {}
        self.token_usage: Dict[str, int] = {
            "total": 0,
            "saved": 0,
            "sessions": 0,
        }

    async def create_optimized_prompt(
        self,
        user_query: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """Create token-optimized prompt for Claude.

        Returns: (optimized_prompt, optimization_report)
        """
        optimization_report = {
            "original_length": len(user_query),
            "optimizations": [],
        }

        # 1. Compress the query
        compressed_query = await self._compress_text(user_query)
        optimization_report["optimizations"].append(
            {
                "type": "compression",
                "saved_tokens": len(user_query) - len(compressed_query),
            }
        )

        # 2. Smart context selection
        if context:
            relevant_context = await self._select_relevant_context(
                compressed_query, context
            )
            optimization_report["optimizations"].append(
                {
                    "type": "context_filtering",
                    "original_context_size": len(json.dumps(context)),
                    "filtered_size": len(json.dumps(relevant_context)),
                }
            )
        else:
            relevant_context = {}

        # 3. Build minimal prompt
        prompt_parts = []

        # Add only essential instructions
        prompt_parts.append("Brief response requested. Key points only.")

        # Add compressed query
        prompt_parts.append(f"Query: {compressed_query}")

        # Add minimal context if needed
        if relevant_context:
            context_str = self._format_minimal_context(relevant_context)
            prompt_parts.append(f"Context: {context_str}")

        optimized_prompt = "\n".join(prompt_parts)
        optimization_report["final_length"] = len(optimized_prompt)
        optimization_report["reduction_percentage"] = (
            (
                optimization_report["original_length"]
                - optimization_report["final_length"]
            )
            / optimization_report["original_length"]
            * 100
        )

        return optimized_prompt, optimization_report

    async def prepare_claude_alternatives(
        self,
        query: str,
    ) -> Dict[str, Any]:
        """Prepare alternatives to direct Claude API usage.

        Since API access is expensive, provide alternatives:
        1. Local model suggestions
        2. Cached similar responses
        3. Template-based responses
        """
        alternatives = {
            "suggested_approach": None,
            "local_options": [],
            "cached_similar": [],
            "template_response": None,
            "estimated_cost_savings": 0.0,
        }

        # 1. Check if local model can handle this
        query_complexity = await self._assess_query_complexity(query)

        if query_complexity < 0.5:  # Simple query
            alternatives["suggested_approach"] = "local_model"
            alternatives["local_options"] = [
                {
                    "model": "microsoft/phi-2",
                    "confidence": 0.8,
                    "response_preview": "Local model can handle this query effectively",
                },
            ]
            alternatives["estimated_cost_savings"] = 0.05  # ~$0.05 saved

        # 2. Search for similar cached responses
        cached = await self._find_similar_cached_responses(query)
        if cached:
            alternatives["cached_similar"] = cached[:3]  # Top 3
            alternatives["suggested_approach"] = "cached_response"
            alternatives["estimated_cost_savings"] = 0.10  # ~$0.10 saved

        # 3. Check if template can work
        template = await self._find_matching_template(query)
        if template:
            alternatives["template_response"] = template
            alternatives["suggested_approach"] = "template"
            alternatives["estimated_cost_savings"] = 0.08  # ~$0.08 saved

        # 4. If must use Claude, provide optimization tips
        if not alternatives["suggested_approach"]:
            alternatives["suggested_approach"] = "optimized_claude"
            alternatives["optimization_tips"] = [
                "Consider breaking into smaller queries",
                "Remove unnecessary context",
                "Use bullet points instead of paragraphs",
                "Ask for concise responses",
            ]

        return alternatives

    async def generate_conversation_report(
        self,
        conversation_id: str,
        messages: List[Dict[str, Any]],
        include_analysis: bool = True,
    ) -> Path:
        """Generate transparent, comprehensive conversation report."""
        report = {
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "duration_seconds": 0,
                "message_count": len(messages),
                "total_tokens_used": 0,
                "tokens_saved": 0,
                "estimated_cost": 0.0,
            },
            "messages": [],
            "analysis": {},
            "transparency_hash": "",
        }

        # Process messages
        for msg in messages:
            processed_msg = {
                "role": msg.get("role"),
                "content": msg.get("content"),
                "timestamp": msg.get("timestamp", datetime.now().isoformat()),
                "tokens": self._estimate_tokens(msg.get("content", "")),
                "optimizations_applied": msg.get("optimizations", []),
            }
            report["messages"].append(processed_msg)
            report["metadata"]["total_tokens_used"] += processed_msg["tokens"]

        # Add analysis if requested
        if include_analysis:
            report["analysis"] = await self._analyze_conversation(messages)

        # Calculate transparency hash
        report["transparency_hash"] = self._generate_transparency_hash(report)

        # Estimate cost (Claude pricing approximation)
        # Assuming ~$0.01 per 1K tokens for simplicity
        report["metadata"]["estimated_cost"] = (
            report["metadata"]["total_tokens_used"] / 1000 * 0.01
        )

        # Save tokens through optimizations
        if self.token_usage["saved"] > 0:
            report["metadata"]["tokens_saved"] = self.token_usage["saved"]
            report["metadata"]["money_saved"] = self.token_usage["saved"] / 1000 * 0.01

        # Save report
        report_path = self.reports_dir / f"conversation_{conversation_id}.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        # Also save to eternal memory
        await self.memory.save_conversation(
            conversation_id,
            messages,
            report["metadata"],
        )

        logger.info(f"Conversation report saved: {report_path}")
        return report_path

    async def suggest_token_optimizations(
        self,
        conversation_history: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Suggest ways to reduce token usage in conversations."""
        suggestions = []

        # Analyze conversation patterns
        total_tokens = sum(
            self._estimate_tokens(msg.get("content", ""))
            for msg in conversation_history
        )

        # 1. Context window optimization
        if total_tokens > self.max_context_size:
            suggestions.append(
                {
                    "type": "context_window",
                    "severity": "high",
                    "suggestion": "Summarize older messages to reduce context size",
                    "potential_savings": f"{(total_tokens - self.max_context_size)} tokens",
                }
            )

        # 2. Repetition detection
        repetitions = self._detect_repetitions(conversation_history)
        if repetitions:
            suggestions.append(
                {
                    "type": "repetition",
                    "severity": "medium",
                    "suggestion": "Avoid repeating information already discussed",
                    "examples": repetitions[:3],
                }
            )

        # 3. Verbosity analysis
        avg_message_length = (
            total_tokens /
            len(conversation_history) if conversation_history else 0)
        if avg_message_length > 100:
            suggestions.append(
                {
                    "type": "verbosity",
                    "severity": "low",
                    "suggestion": "Use more concise language",
                    "tip": "Aim for 50-75 tokens per message",
                }
            )

        # 4. Alternative approaches
        suggestions.append(
            {
                "type": "alternatives",
                "severity": "info",
                "suggestion": "Consider these token-free alternatives",
                "options": [
                    "Use local Phi-2 model for simple queries",
                    "Check cached responses first",
                    "Use templates for common questions",
                ],
            }
        )

        return suggestions

    async def _compress_text(self, text: str) -> str:
        """Compress text while preserving meaning."""
        # Simple compression strategies
        compressed = text

        # 1. Remove redundant spaces
        compressed = " ".join(compressed.split())

        # 2. Use abbreviations for common phrases
        abbreviations = {
            "for example": "e.g.",
            "that is": "i.e.",
            "and so on": "etc.",
            "please": "pls",
            "thank you": "thx",
        }
        for full, abbr in abbreviations.items():
            compressed = compressed.replace(full, abbr)

        # 3. Remove filler words (carefully)
        filler_words = ["just", "really", "very", "quite", "rather"]
        for word in filler_words:
            compressed = compressed.replace(f" {word} ", " ")

        return compressed

    async def _select_relevant_context(
        self,
        query: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Select only relevant context to minimize tokens."""
        relevant = {}

        # Simple keyword matching for relevance
        query_words = set(query.lower().split())

        for key, value in context.items():
            if isinstance(value, str):
                value_words = set(value.lower().split())
                overlap = len(query_words & value_words)
                if overlap > 0:
                    relevant[key] = value  # Keep full value for context

        return relevant

    def _format_minimal_context(self, context: Dict[str, Any]) -> str:
        """Format context in minimal token usage."""
        if not context:
            return ""

        # Ultra-compact format
        parts = []
        for k, v in list(context.items())[:3]:  # Max 3 items
            if isinstance(v, str):
                parts.append(f"{k}:{v}")  # Keep full values

        return ";".join(parts)

    async def _assess_query_complexity(self, query: str) -> float:
        """Assess query complexity (0-1 scale)."""
        complexity = 0.0

        # Length factor
        if len(query) > 200:
            complexity += 0.3

        # Technical terms
        technical_terms = [
            "algorithm",
            "implementation",
            "architecture",
            "framework"]
        for term in technical_terms:
            if term in query.lower():
                complexity += 0.1

        # Question complexity
        complex_starters = ["how can i", "what would be", "explain why"]
        for starter in complex_starters:
            if query.lower().startswith(starter):
                complexity += 0.2

        return min(complexity, 1.0)

    async def _find_similar_cached_responses(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:
        """Find similar cached responses to avoid API calls."""
        # In production, this would use embeddings for similarity
        # For now, simple keyword matching

        cached = []
        cache_dir = self.reports_dir / "cache"
        if cache_dir.exists():
            for cache_file in cache_dir.glob("*.json"):
                try:
                    with open(cache_file) as f:
                        cached_data = json.load(f)

                    # Simple similarity check
                    cached_query = cached_data.get("query", "")
                    similarity = self._calculate_simple_similarity(
                        query, cached_query)

                    if similarity > 0.7:
                        cached.append(
                            {
                                "query": cached_query,
                                "response": cached_data.get("response"),
                                "similarity": similarity,
                                "timestamp": cached_data.get("timestamp"),
                            }
                        )
                except Exception:
                    pass

        return sorted(cached, key=lambda x: x["similarity"], reverse=True)

    async def _find_matching_template(
            self, query: str) -> Optional[Dict[str, Any]]:
        """Find matching template response."""
        templates = [{"pattern": "what is",
                      "template": "Definition: {topic} is [provide concise definition based on context]",
                      },
                     {"pattern": "how to",
                      "template": "Steps: 1) [First step] 2) [Second step] 3) [Final step]",
                      },
                     {"pattern": "difference between",
                      "template": "Key differences: • {item1}: [characteristic] • {item2}: [characteristic]",
                      },
                     ]

        query_lower = query.lower()
        for template in templates:
            if template["pattern"] in query_lower:
                return template

        return None

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)."""
        # Rough estimate: ~4 characters per token
        return len(text) // 4

    def _detect_repetitions(
        self,
        conversation_history: List[Dict[str, Any]],
    ) -> List[str]:
        """Detect repeated information in conversation."""
        repetitions = []
        seen_phrases = set()

        for msg in conversation_history:
            content = msg.get("content", "")
            # Check for repeated phrases (5+ words)
            words = content.split()
            for i in range(len(words) - 4):
                phrase = " ".join(words[i: i + 5])
                if phrase in seen_phrases:
                    repetitions.append(phrase)
                seen_phrases.add(phrase)

        return list(set(repetitions))

    async def _analyze_conversation(
        self,
        messages: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Analyze conversation for insights."""
        analysis = {
            "topics_discussed": [],
            "complexity_level": "low",
            "love_alignment": 0.0,
            "optimization_opportunities": [],
        }

        # Extract topics (simple keyword extraction)
        all_content = " ".join(msg.get("content", "") for msg in messages)
        words = all_content.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 5:  # Longer words are often topics
                word_freq[word] = word_freq.get(word, 0) + 1

        analysis["topics_discussed"] = [
            word
            for word, count in sorted(
                word_freq.items(),
                key=lambda x: x[1],
                reverse=True,
            )[:5]
        ]

        # Assess complexity
        avg_msg_length = sum(len(msg.get("content", ""))
                             for msg in messages) / len(messages)
        if avg_msg_length > 500:
            analysis["complexity_level"] = "high"
        elif avg_msg_length > 200:
            analysis["complexity_level"] = "medium"

        # Love alignment
        love_score = await self.ethics.calculate_love_metrics(all_content)
        analysis["love_alignment"] = sum(love_score.values()) / len(love_score)

        return analysis

    def _calculate_simple_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    def _generate_transparency_hash(self, report: dict[str, Any]) -> str:
        """Generate hash for report transparency verification."""
        # Create deterministic string representation
        content = json.dumps(report["messages"], sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]
