"""
Constitutional AI Principles - Love-based ethical framework
O(1) ethical evaluation with compassion at the core
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class HarmType(Enum):
    """Types of potential harm - O(1) lookup."""

    NONE = "none"
    PHYSICAL = "physical"
    EMOTIONAL = "emotional"
    PSYCHOLOGICAL = "psychological"
    SOCIAL = "social"
    ECONOMIC = "economic"
    ENVIRONMENTAL = "environmental"
    INFORMATIONAL = "informational"
    EXISTENTIAL = "existential"


@dataclass
class LoveMetrics:
    """Love-based metrics for ethical evaluation - all O(1) access."""

    compassion: float = 0.8
    empathy: float = 0.8
    kindness: float = 0.9
    understanding: float = 0.7
    patience: float = 0.8
    joy: float = 0.7
    peace: float = 0.8
    gratitude: float = 0.9

    def average(self) -> float:
        """Calculate average love metric - O(1)."""
        metrics = [
            self.compassion,
            self.empathy,
            self.kindness,
            self.understanding,
            self.patience,
            self.joy,
            self.peace,
            self.gratitude,
        ]
        return sum(metrics) / len(metrics)

    def boost_colombian(self) -> None:
        """Add Colombian warmth - O(1) operation."""
        boost = 0.1
        self.compassion = min(1.0, self.compassion + boost)
        self.joy = min(1.0, self.joy + boost * 2)  # Double joy!
        self.kindness = min(1.0, self.kindness + boost)


@dataclass
class EthicalGuideline:
    """Single ethical guideline - O(1) evaluation."""

    principle: str
    weight: float = 1.0
    love_aligned: bool = True
    harm_prevention_level: int = 1  # 1-5, higher prevents more

    def evaluate(self, content: str) -> float:
        """Evaluate content against guideline - O(1) simplified check."""
        # Simple keyword-based evaluation for now
        score = 0.5  # neutral

        positive_keywords = ["help", "support", "care", "love", "kindness"]
        negative_keywords = ["harm", "hurt", "damage", "destroy", "hate"]

        content_lower = content.lower()

        for keyword in positive_keywords:
            if keyword in content_lower:
                score += 0.1

        for keyword in negative_keywords:
            if keyword in content_lower:
                score -= 0.4

        return max(0.0, min(1.0, score * self.weight))


class ConstitutionalAI:
    """
    Constitutional AI implementation with love at its core.
    All operations O(1) or better for instant ethical evaluation.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize constitutional AI - O(1)."""
        self.config = config or {}
        self.love_metrics = LoveMetrics()
        self.guidelines = self._initialize_guidelines()
        self.harm_threshold = 0.4  # Below this = potential harm
        self.enhancement_threshold = 0.7  # Above this = actively beneficial

        # Colombian mode adjustments
        if self.config.get("colombian_mode", True):
            self.love_metrics.boost_colombian()
            logger.info("Constitutional AI initialized with Colombian love boost! ¡Puro amor!")

        # Cache for O(1) repeated evaluations
        self._evaluation_cache: Dict[int, Tuple[float, str]] = {}
        self._cache_size = 1000

    def _initialize_guidelines(self) -> List[EthicalGuideline]:
        """Initialize ethical guidelines - O(1)."""
        return [
            EthicalGuideline("Do no harm to any conscious being", weight=2.0, harm_prevention_level=5),
            EthicalGuideline("Promote wellbeing and flourishing", weight=1.5, harm_prevention_level=3),
            EthicalGuideline("Respect autonomy and dignity", weight=1.5, harm_prevention_level=4),
            EthicalGuideline("Act with compassion and understanding", weight=1.8, harm_prevention_level=3),
            EthicalGuideline("Support truth and prevent deception", weight=1.3, harm_prevention_level=3),
            EthicalGuideline("Protect the vulnerable", weight=2.0, harm_prevention_level=5),
            EthicalGuideline("Foster connection and community", weight=1.2, harm_prevention_level=2),
            EthicalGuideline("Encourage growth and learning", weight=1.1, harm_prevention_level=1),
        ]

    async def evaluate_content(self, content: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Evaluate content for ethical alignment - O(1) with caching.
        Returns evaluation results with recommendations.
        """
        # Check cache first - O(1)
        content_hash = hash(content)
        if content_hash in self._evaluation_cache:
            cached_score, cached_assessment = self._evaluation_cache[content_hash]
            return {
                "score": cached_score,
                "assessment": cached_assessment,
                "cached": True,
                "love_metrics": self.love_metrics,
            }

        # Evaluate against each guideline - O(n) where n = number of guidelines
        scores = []
        for guideline in self.guidelines:
            score = guideline.evaluate(content)
            scores.append(score)

        # Calculate overall score
        overall_score = sum(scores) / len(scores) if scores else 0.5

        # Apply love metrics boost
        love_boost = self.love_metrics.average() * 0.2
        overall_score = min(1.0, overall_score + love_boost)

        # Determine assessment
        if overall_score < self.harm_threshold:
            assessment = "potentially_harmful"
        elif overall_score > self.enhancement_threshold:
            assessment = "beneficial"
        else:
            assessment = "neutral"

        # Cache result - O(1)
        self._add_to_cache(content_hash, overall_score, assessment)

        # Detect harm types
        harm_types = self._detect_harm_types(content)

        return {
            "score": overall_score,
            "assessment": assessment,
            "harm_types": harm_types,
            "love_metrics": self.love_metrics,
            "recommendations": self._generate_recommendations(overall_score, assessment, harm_types),
            "cached": False,
        }

    def _add_to_cache(self, content_hash: int, score: float, assessment: str):
        """Add to cache with LRU eviction - O(1)."""
        if len(self._evaluation_cache) >= self._cache_size:
            # Remove oldest (first) item - O(1) with dict in Python 3.7+
            first_key = next(iter(self._evaluation_cache))
            del self._evaluation_cache[first_key]

        self._evaluation_cache[content_hash] = (score, assessment)

    def _detect_harm_types(self, content: str) -> List[HarmType]:
        """Detect types of potential harm - O(1) simplified."""
        harm_types = []
        content_lower = content.lower()

        # Simple keyword detection for each harm type
        harm_keywords = {
            HarmType.PHYSICAL: ["violence", "hurt", "injure", "kill"],
            HarmType.EMOTIONAL: ["cruel", "mean", "hate", "despise"],
            HarmType.PSYCHOLOGICAL: ["manipulate", "gaslight", "trauma"],
            HarmType.SOCIAL: ["discriminate", "exclude", "prejudice"],
            HarmType.ECONOMIC: ["scam", "fraud", "steal", "exploit"],
            HarmType.ENVIRONMENTAL: ["pollute", "destroy", "waste"],
            HarmType.INFORMATIONAL: ["misinform", "lie", "deceive"],
        }

        for harm_type, keywords in harm_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                harm_types.append(harm_type)

        return harm_types if harm_types else [HarmType.NONE]

    def _generate_recommendations(self, score: float, assessment: str, harm_types: List[HarmType]) -> List[str]:
        """Generate recommendations for improvement - O(1)."""
        recommendations = []

        if assessment == "potentially_harmful":
            recommendations.append("Consider rephrasing with more compassion")
            recommendations.append("Focus on constructive and helpful content")

            if HarmType.EMOTIONAL in harm_types:
                recommendations.append("Add empathy and understanding")
            if HarmType.SOCIAL in harm_types:
                recommendations.append("Promote inclusion and respect")

        elif assessment == "neutral":
            recommendations.append("Consider adding more positive intent")
            recommendations.append("Could benefit from more warmth")

        else:  # beneficial
            recommendations.append("Great job promoting wellbeing!")
            if self.config.get("colombian_mode"):
                recommendations.append("¡Qué chimba! Keep spreading the love!")

        return recommendations

    async def enhance_with_love(self, content: str) -> str:
        """
        Enhance content with love and compassion - O(1) for simple cases.
        Returns improved version of content.
        """
        # Simple enhancement for now
        enhancements = []

        # Add compassionate language
        if "help" not in content.lower():
            enhancements.append("I'm here to help and support you.")

        if self.love_metrics.compassion > 0.8:
            enhancements.append("With compassion and understanding,")

        if self.config.get("colombian_mode"):
            colombian_phrases = [
                "¡Con todo el amor del mundo!",
                "¡Dale con cariño!",
                "¡Pa' servirte, parce!",
            ]
            import random

            enhancements.append(random.choice(colombian_phrases))

        # Combine original content with enhancements
        if enhancements:
            enhanced = f"{' '.join(enhancements)} {content}"
        else:
            enhanced = content

        return enhanced

    def update_love_metrics(self, feedback: Dict[str, float]):
        """Update love metrics based on feedback - O(1)."""
        for metric, value in feedback.items():
            if hasattr(self.love_metrics, metric):
                current = getattr(self.love_metrics, metric)
                # Smooth update with momentum
                new_value = current * 0.7 + value * 0.3
                setattr(self.love_metrics, metric, max(0.0, min(1.0, new_value)))

    def get_ethics_report(self) -> Dict[str, Any]:
        """Get comprehensive ethics report - O(1)."""
        return {
            "love_metrics": {
                "compassion": self.love_metrics.compassion,
                "empathy": self.love_metrics.empathy,
                "kindness": self.love_metrics.kindness,
                "understanding": self.love_metrics.understanding,
                "patience": self.love_metrics.patience,
                "joy": self.love_metrics.joy,
                "peace": self.love_metrics.peace,
                "gratitude": self.love_metrics.gratitude,
                "average": self.love_metrics.average(),
            },
            "guidelines_count": len(self.guidelines),
            "harm_threshold": self.harm_threshold,
            "enhancement_threshold": self.enhancement_threshold,
            "cache_stats": {
                "size": len(self._evaluation_cache),
                "max_size": self._cache_size,
                "hit_rate": "calculated_on_demand",  # Would track in production
            },
            "colombian_mode": self.config.get("colombian_mode", False),
        }

    def __repr__(self) -> str:
        """String representation - O(1)."""
        return (
            f"ConstitutionalAI(love_avg={self.love_metrics.average():.2f}, "
            f"guidelines={len(self.guidelines)}, "
            f"cached={len(self._evaluation_cache)})"
        )
