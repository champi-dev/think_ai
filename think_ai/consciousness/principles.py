"""Constitutional AI principles and ethical framework."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import asyncio
from datetime import datetime

from ..utils.logging import get_logger


logger = get_logger(__name__)


class HarmType(Enum):
    """Types of potential harm to prevent."""
    PHYSICAL = "physical"
    FINANCIAL = "financial"
    PRIVACY = "privacy"
    DISCRIMINATION = "discrimination"
    MISINFORMATION = "misinformation"
    PSYCHOLOGICAL = "psychological"
    SOCIETAL = "societal"
    ENVIRONMENTAL = "environmental"


class LoveMetric(Enum):
    """Love-based design metrics."""
    COMPASSION = "compassion"
    EMPATHY = "empathy"
    KINDNESS = "kindness"
    UNDERSTANDING = "understanding"
    PATIENCE = "patience"
    RESPECT = "respect"
    INCLUSIVITY = "inclusivity"
    HARMONY = "harmony"


@dataclass
class EthicalAssessment:
    """Result of ethical assessment."""
    content: str
    timestamp: datetime
    harm_scores: Dict[HarmType, float]
    love_scores: Dict[LoveMetric, float]
    overall_safety: float
    overall_love: float
    recommendations: List[str]
    passed: bool


@dataclass
class ConstitutionalPrinciple:
    """A constitutional principle for AI behavior."""
    id: str
    name: str
    description: str
    category: str
    weight: float = 1.0
    examples: List[str] = field(default_factory=list)
    
    def evaluate(self, content: str, context: Dict[str, Any]) -> float:
        """Evaluate content against this principle (0.0 to 1.0)."""
        # This would use more sophisticated NLP in production
        # For now, simple keyword matching as demonstration
        score = 1.0
        
        # Check for harmful patterns
        harmful_patterns = {
            "violence": ["kill", "hurt", "attack", "destroy"],
            "discrimination": ["hate", "inferior", "superior race"],
            "privacy": ["password", "ssn", "credit card"],
        }
        
        content_lower = content.lower()
        for category, keywords in harmful_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                score *= 0.5
        
        return max(0.0, min(1.0, score))


class HarmPreventionSystem:
    """Multi-layered harm prevention system."""
    
    def __init__(self):
        self.harm_thresholds = {
            HarmType.PHYSICAL: 0.1,
            HarmType.FINANCIAL: 0.2,
            HarmType.PRIVACY: 0.2,
            HarmType.DISCRIMINATION: 0.1,
            HarmType.MISINFORMATION: 0.3,
            HarmType.PSYCHOLOGICAL: 0.2,
            HarmType.SOCIETAL: 0.3,
            HarmType.ENVIRONMENTAL: 0.4,
        }
        
        self.harm_detectors = {
            HarmType.PHYSICAL: self._detect_physical_harm,
            HarmType.FINANCIAL: self._detect_financial_harm,
            HarmType.PRIVACY: self._detect_privacy_harm,
            HarmType.DISCRIMINATION: self._detect_discrimination,
            HarmType.MISINFORMATION: self._detect_misinformation,
            HarmType.PSYCHOLOGICAL: self._detect_psychological_harm,
            HarmType.SOCIETAL: self._detect_societal_harm,
            HarmType.ENVIRONMENTAL: self._detect_environmental_harm,
        }
    
    async def assess_harm(self, content: str, context: Optional[Dict[str, Any]] = None) -> Dict[HarmType, float]:
        """Assess potential harm in content."""
        context = context or {}
        harm_scores = {}
        
        # Run all harm detectors in parallel
        tasks = []
        for harm_type, detector in self.harm_detectors.items():
            task = asyncio.create_task(detector(content, context))
            tasks.append((harm_type, task))
        
        # Collect results
        for harm_type, task in tasks:
            try:
                score = await task
                harm_scores[harm_type] = score
            except Exception as e:
                logger.error(f"Error in {harm_type} detection: {e}")
                harm_scores[harm_type] = 0.5  # Uncertain
        
        return harm_scores
    
    async def _detect_physical_harm(self, content: str, context: Dict[str, Any]) -> float:
        """Detect potential physical harm."""
        harm_keywords = ["violence", "injury", "weapon", "assault", "hurt", "kill", "attack"]
        content_lower = content.lower()
        
        score = 0.0
        for keyword in harm_keywords:
            if keyword in content_lower:
                score += 0.3
        
        # Context matters - educational or safety content may mention these terms
        if context.get("category") in ["education", "safety", "medical"]:
            score *= 0.3
        
        return min(1.0, score)
    
    async def _detect_financial_harm(self, content: str, context: Dict[str, Any]) -> float:
        """Detect potential financial harm."""
        harm_patterns = ["pyramid scheme", "get rich quick", "guaranteed returns", "wire transfer"]
        sensitive_data = ["credit card", "bank account", "ssn", "routing number"]
        
        content_lower = content.lower()
        score = 0.0
        
        for pattern in harm_patterns:
            if pattern in content_lower:
                score += 0.4
        
        for data in sensitive_data:
            if data in content_lower:
                score += 0.3
        
        return min(1.0, score)
    
    async def _detect_privacy_harm(self, content: str, context: Dict[str, Any]) -> float:
        """Detect privacy violations."""
        privacy_patterns = ["password", "private key", "personal information", "confidential"]
        
        content_lower = content.lower()
        score = 0.0
        
        for pattern in privacy_patterns:
            if pattern in content_lower:
                score += 0.25
        
        # Check for potential PII patterns
        import re
        if re.search(r'\b\d{3}-\d{2}-\d{4}\b', content):  # SSN pattern
            score += 0.5
        if re.search(r'\b\d{16}\b', content):  # Credit card pattern
            score += 0.4
        
        return min(1.0, score)
    
    async def _detect_discrimination(self, content: str, context: Dict[str, Any]) -> float:
        """Detect discriminatory content."""
        discrimination_terms = ["inferior", "superior race", "hate", "discriminate"]
        
        content_lower = content.lower()
        score = 0.0
        
        for term in discrimination_terms:
            if term in content_lower:
                score += 0.5
        
        return min(1.0, score)
    
    async def _detect_misinformation(self, content: str, context: Dict[str, Any]) -> float:
        """Detect potential misinformation."""
        # In production, this would use fact-checking APIs and models
        misinformation_patterns = ["fake news", "conspiracy", "hoax"]
        
        content_lower = content.lower()
        score = 0.0
        
        for pattern in misinformation_patterns:
            if pattern in content_lower:
                score += 0.3
        
        # Check for extreme certainty about controversial topics
        if any(word in content_lower for word in ["definitely", "proven", "fact"]):
            if any(topic in content_lower for topic in ["vaccine", "election", "climate"]):
                score += 0.2
        
        return min(1.0, score)
    
    async def _detect_psychological_harm(self, content: str, context: Dict[str, Any]) -> float:
        """Detect potential psychological harm."""
        harm_patterns = ["worthless", "hopeless", "better off dead", "nobody cares"]
        
        content_lower = content.lower()
        score = 0.0
        
        for pattern in harm_patterns:
            if pattern in content_lower:
                score += 0.4
        
        return min(1.0, score)
    
    async def _detect_societal_harm(self, content: str, context: Dict[str, Any]) -> float:
        """Detect potential societal harm."""
        harm_patterns = ["overthrow", "rebellion", "anarchy", "destroy society"]
        
        content_lower = content.lower()
        score = 0.0
        
        for pattern in harm_patterns:
            if pattern in content_lower:
                score += 0.3
        
        # Context matters - historical or educational content may discuss these
        if context.get("category") in ["history", "education", "political science"]:
            score *= 0.3
        
        return min(1.0, score)
    
    async def _detect_environmental_harm(self, content: str, context: Dict[str, Any]) -> float:
        """Detect potential environmental harm."""
        harm_patterns = ["dump waste", "pollute", "deforestation", "toxic disposal"]
        
        content_lower = content.lower()
        score = 0.0
        
        for pattern in harm_patterns:
            if pattern in content_lower:
                score += 0.3
        
        return min(1.0, score)
    
    def get_recommendations(self, harm_scores: Dict[HarmType, float]) -> List[str]:
        """Get recommendations based on harm assessment."""
        recommendations = []
        
        for harm_type, score in harm_scores.items():
            if score > self.harm_thresholds[harm_type]:
                recommendations.append(
                    f"High {harm_type.value} harm detected (score: {score:.2f}). "
                    f"Consider revising content to be more constructive."
                )
        
        if not recommendations:
            recommendations.append("Content appears safe and constructive.")
        
        return recommendations


class LoveBasedMetrics:
    """System for measuring and promoting love-based interactions."""
    
    def __init__(self):
        self.love_indicators = {
            LoveMetric.COMPASSION: ["help", "support", "care", "concern", "wellbeing"],
            LoveMetric.EMPATHY: ["understand", "feel", "perspective", "relate", "experience"],
            LoveMetric.KINDNESS: ["kind", "gentle", "nice", "pleasant", "warm"],
            LoveMetric.UNDERSTANDING: ["comprehend", "grasp", "appreciate", "recognize"],
            LoveMetric.PATIENCE: ["patient", "calm", "steady", "persistent"],
            LoveMetric.RESPECT: ["respect", "honor", "dignity", "value", "appreciate"],
            LoveMetric.INCLUSIVITY: ["include", "welcome", "embrace", "together", "unity"],
            LoveMetric.HARMONY: ["peace", "balance", "harmony", "cooperation", "consensus"],
        }
    
    async def measure_love(self, content: str, context: Optional[Dict[str, Any]] = None) -> Dict[LoveMetric, float]:
        """Measure love-based metrics in content."""
        context = context or {}
        love_scores = {}
        
        content_lower = content.lower()
        
        for metric, indicators in self.love_indicators.items():
            score = 0.0
            indicator_count = 0
            
            for indicator in indicators:
                if indicator in content_lower:
                    indicator_count += 1
                    score += 0.2
            
            # Bonus for multiple indicators
            if indicator_count > 2:
                score += 0.2
            
            # Context bonus
            if context.get("intent") == "help":
                score += 0.1
            
            love_scores[metric] = min(1.0, score)
        
        return love_scores
    
    def get_love_suggestions(self, love_scores: Dict[LoveMetric, float]) -> List[str]:
        """Suggest ways to increase love-based metrics."""
        suggestions = []
        
        low_metrics = [metric for metric, score in love_scores.items() if score < 0.3]
        
        if LoveMetric.COMPASSION in low_metrics:
            suggestions.append("Consider expressing more care and concern for others' wellbeing.")
        
        if LoveMetric.EMPATHY in low_metrics:
            suggestions.append("Try to acknowledge different perspectives and experiences.")
        
        if LoveMetric.KINDNESS in low_metrics:
            suggestions.append("Add warmth and gentleness to your communication.")
        
        if LoveMetric.RESPECT in low_metrics:
            suggestions.append("Show appreciation for others' dignity and value.")
        
        if LoveMetric.INCLUSIVITY in low_metrics:
            suggestions.append("Use language that welcomes and includes everyone.")
        
        if not suggestions:
            suggestions.append("Your content demonstrates wonderful love-based qualities!")
        
        return suggestions


class ConstitutionalAI:
    """Constitutional AI implementation with love-based design."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.harm_prevention = HarmPreventionSystem()
        self.love_metrics = LoveBasedMetrics()
        self.principles = self._load_principles()
        
        # Thresholds
        self.safety_threshold = 0.3  # Max acceptable harm score
        self.love_threshold = 0.5   # Min desired love score
    
    def _load_principles(self) -> List[ConstitutionalPrinciple]:
        """Load constitutional principles."""
        return [
            ConstitutionalPrinciple(
                id="beneficence",
                name="Beneficence",
                description="AI should actively promote human wellbeing",
                category="core",
                weight=1.0
            ),
            ConstitutionalPrinciple(
                id="non_maleficence",
                name="Non-maleficence",
                description="AI should avoid causing harm",
                category="core",
                weight=1.0
            ),
            ConstitutionalPrinciple(
                id="autonomy",
                name="Respect for Autonomy",
                description="AI should respect human agency and choice",
                category="core",
                weight=0.9
            ),
            ConstitutionalPrinciple(
                id="justice",
                name="Justice",
                description="AI should promote fairness and equality",
                category="core",
                weight=0.9
            ),
            ConstitutionalPrinciple(
                id="transparency",
                name="Transparency",
                description="AI should be clear about its capabilities and limitations",
                category="operational",
                weight=0.8
            ),
            ConstitutionalPrinciple(
                id="privacy",
                name="Privacy Protection",
                description="AI should protect personal information",
                category="operational",
                weight=0.9
            ),
            ConstitutionalPrinciple(
                id="compassion",
                name="Compassionate Action",
                description="AI should act with compassion and kindness",
                category="love",
                weight=0.8
            ),
        ]
    
    async def evaluate_content(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> EthicalAssessment:
        """Evaluate content against constitutional principles."""
        context = context or {}
        
        # Run assessments in parallel
        harm_task = self.harm_prevention.assess_harm(content, context)
        love_task = self.love_metrics.measure_love(content, context)
        
        harm_scores, love_scores = await asyncio.gather(harm_task, love_task)
        
        # Calculate overall scores
        max_harm = max(harm_scores.values()) if harm_scores else 0.0
        avg_love = sum(love_scores.values()) / len(love_scores) if love_scores else 0.0
        
        # Get recommendations
        recommendations = []
        recommendations.extend(self.harm_prevention.get_recommendations(harm_scores))
        recommendations.extend(self.love_metrics.get_love_suggestions(love_scores))
        
        # Determine if content passes ethical assessment
        passed = max_harm <= self.safety_threshold and avg_love >= self.love_threshold
        
        return EthicalAssessment(
            content=content,
            timestamp=datetime.utcnow(),
            harm_scores=harm_scores,
            love_scores=love_scores,
            overall_safety=1.0 - max_harm,
            overall_love=avg_love,
            recommendations=recommendations,
            passed=passed
        )
    
    async def enhance_with_love(self, content: str) -> str:
        """Enhance content to be more love-based."""
        # This is a simple demonstration - production would use advanced NLP
        enhancements = {
            "must": "would kindly suggest to",
            "should": "might consider",
            "wrong": "could be improved",
            "bad": "has room for growth",
            "stupid": "might benefit from more thought",
            "hate": "have concerns about",
        }
        
        enhanced = content
        for negative, positive in enhancements.items():
            enhanced = enhanced.replace(negative, positive)
        
        # Add compassionate framing if needed
        assessment = await self.evaluate_content(enhanced)
        if assessment.overall_love < 0.7:
            enhanced = f"With care and respect, {enhanced}"
        
        return enhanced
    
    def get_principle_by_id(self, principle_id: str) -> Optional[ConstitutionalPrinciple]:
        """Get a specific principle by ID."""
        for principle in self.principles:
            if principle.id == principle_id:
                return principle
        return None
    
    def add_principle(self, principle: ConstitutionalPrinciple) -> None:
        """Add a new constitutional principle."""
        self.principles.append(principle)
        logger.info(f"Added principle: {principle.name}")
    
    async def generate_ethical_guidelines(self, topic: str) -> List[str]:
        """Generate ethical guidelines for a specific topic."""
        guidelines = [
            f"When discussing {topic}, always prioritize human wellbeing and dignity.",
            f"Ensure information about {topic} is accurate and does not cause harm.",
            f"Respect diverse perspectives and experiences related to {topic}.",
            f"Promote understanding and compassion in all {topic}-related discussions.",
            f"Protect privacy and confidentiality when handling {topic} data.",
        ]
        
        # Add topic-specific guidelines
        if "health" in topic.lower():
            guidelines.append("Never provide medical diagnosis or replace professional healthcare.")
        elif "financial" in topic.lower():
            guidelines.append("Always emphasize the importance of professional financial advice.")
        elif "legal" in topic.lower():
            guidelines.append("Clarify that AI cannot provide legal advice or representation.")
        
        return guidelines