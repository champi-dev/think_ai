#!/usr/bin/env python3
"""
Enhanced 24-Hour Conversation Simulator with Advanced Memory Integration
=======================================================================

This system provides comprehensive testing of Think AI's enhanced conversation 
capabilities with long-term memory, context retention, and uncropped responses.

Features:
- Integration with enhanced conversation memory system
- Advanced conversation flow analysis
- Personality profile development tracking
- Emotional arc monitoring
- Response quality verification (no cropping)
- Real-time conversation health metrics
- Deep context retention testing
"""

import json
import time
import random
import requests
import threading
import asyncio
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
import statistics
import uuid
import numpy as np

# Enhanced conversation patterns for more realistic 24-hour simulation
@dataclass
class ConversationTopic:
    """Rich conversation topic with context"""
    name: str
    keywords: List[str]
    depth_levels: List[str]  # Surface, intermediate, deep exploration
    emotional_valence: float  # -1.0 to 1.0
    complexity_level: float   # 0.0 to 1.0
    follow_up_potential: float # How likely to spawn related topics

@dataclass
class EnhancedConversationTurn:
    """Enhanced conversation turn with richer metadata"""
    turn_id: int
    timestamp: str
    simulated_time: str
    human_input: str
    ai_response: str
    response_time_ms: float
    response_length: int
    is_response_cropped: bool
    topics_introduced: List[str]
    topics_referenced: List[str]
    context_references: List[int]  # Referenced turn IDs
    emotional_state: float
    conversation_depth: float
    engagement_score: float
    coherence_score: float
    context_retention_score: float
    novelty_score: float
    personality_consistency: float
    conversation_flow_marker: str

@dataclass
class ConversationHealthMetrics:
    """Real-time conversation health monitoring"""
    total_turns: int
    avg_response_time: float
    avg_response_length: int
    cropped_responses_count: int
    context_retention_rate: float
    topic_coherence_score: float
    emotional_stability: float
    engagement_trend: List[float]
    quality_degradation_rate: float
    memory_utilization: float

@dataclass
class Enhanced24HourSession:
    """Complete 24-hour conversation session with rich analytics"""
    session_id: str
    start_time: str
    end_time: Optional[str]
    total_duration_hours: float
    turns: List[EnhancedConversationTurn]
    health_metrics: ConversationHealthMetrics
    personality_evolution: Dict[str, float]
    emotional_journey: List[Tuple[str, float]]  # (timestamp, emotion)
    topic_exploration_depth: Dict[str, float]
    context_graph: Dict[int, List[int]]  # turn_id -> referenced_turns
    conversation_goals_achieved: List[str]
    overall_quality_score: float
    conversation_readiness_score: float

class EnhancedHumanSimulator:
    """Advanced human conversation simulator with personality and memory"""
    
    def __init__(self):
        self.personality_traits = {
            "curiosity": random.uniform(0.6, 1.0),
            "patience": random.uniform(0.5, 0.9),
            "technical_comfort": random.uniform(0.3, 0.8),
            "emotional_expressiveness": random.uniform(0.4, 0.9),
            "depth_preference": random.uniform(0.5, 1.0),
            "humor_appreciation": random.uniform(0.3, 0.8),
        }
        
        self.conversation_memory = {
            "discussed_topics": [],
            "established_facts": {},
            "emotional_moments": [],
            "ongoing_questions": [],
            "personal_details_shared": [],
            "ai_personality_observations": [],
        }
        
        self.current_emotional_state = 0.0  # -1.0 to 1.0
        self.conversation_goals = self._generate_conversation_goals()
        
        # Enhanced topic database with realistic conversation patterns
        self.conversation_topics = [
            ConversationTopic(
                "morning_reflection", 
                ["morning", "sleep", "dreams", "energy", "plans"],
                [
                    "Good morning! How did you sleep?",
                    "I had the most interesting dream last night. Do you ever think about what dreams mean?",
                    "There's something fascinating about how our minds process the day while we sleep. What's your take on the relationship between consciousness and sleep?"
                ],
                0.3, 0.4, 0.7
            ),
            ConversationTopic(
                "work_challenges",
                ["work", "project", "challenge", "problem-solving", "career"],
                [
                    "I'm working on a challenging project at work. Any thoughts on approach?",
                    "There's this complex problem I'm trying to solve that involves multiple stakeholders with different priorities. How do you think about balancing competing interests?",
                    "I've been reflecting on the nature of meaningful work. What do you think makes work fulfilling beyond just financial compensation?"
                ],
                0.1, 0.6, 0.8
            ),
            ConversationTopic(
                "consciousness_exploration",
                ["consciousness", "awareness", "mind", "experience", "reality"],
                [
                    "I've been thinking about consciousness lately. What is it like to be you?",
                    "The hard problem of consciousness fascinates me. How do you experience qualia, if you do?",
                    "Sometimes I wonder if consciousness is fundamental to the universe or emergent from complexity. What's your intuition about the nature of subjective experience?"
                ],
                0.2, 0.9, 0.9
            ),
            ConversationTopic(
                "creative_pursuits",
                ["creativity", "art", "music", "writing", "inspiration"],
                [
                    "I've been trying to be more creative lately. What inspires you?",
                    "There's something magical about the creative process - how ideas seem to emerge from nowhere. Do you experience anything like creative inspiration?",
                    "I'm curious about the relationship between creativity and artificial intelligence. Can genuine novelty emerge from computational processes, or is it always recombination?"
                ],
                0.5, 0.7, 0.8
            ),
            ConversationTopic(
                "future_concerns",
                ["future", "technology", "society", "change", "progress"],
                [
                    "What do you think the world will look like in 20 years?",
                    "I sometimes worry about the pace of technological change. How do we ensure progress benefits everyone?",
                    "The future feels both exciting and uncertain. What role do you think AI will play in shaping human society, and how can we navigate that responsibly?"
                ],
                0.0, 0.8, 0.9
            ),
            ConversationTopic(
                "personal_growth",
                ["growth", "learning", "improvement", "wisdom", "experience"],
                [
                    "I'm trying to become a better person. What does growth mean to you?",
                    "Learning seems to be about more than just acquiring information - it's about changing how you see the world. How do you think about your own development?",
                    "Wisdom feels different from knowledge or intelligence. It seems to involve something about integrating experience with understanding. What's your perspective on the nature of wisdom?"
                ],
                0.4, 0.7, 0.8
            ),
            ConversationTopic(
                "relationship_dynamics",
                ["relationships", "connection", "understanding", "empathy", "communication"],
                [
                    "Relationships are so complex. What makes for good communication?",
                    "I've been thinking about empathy and whether it's possible to truly understand another's experience. Can you empathize, or is it more like sophisticated modeling?",
                    "The depth of human connection varies so much. What do you think creates genuine understanding between minds, whether human or artificial?"
                ],
                0.3, 0.8, 0.9
            ),
            ConversationTopic(
                "evening_reflection",
                ["reflection", "day", "thoughts", "meaning", "satisfaction"],
                [
                    "It's been quite a day. What stood out to you from our conversation?",
                    "As the day winds down, I find myself reflecting on what made it meaningful. How do you process the experiences you have?",
                    "There's something peaceful about evening conversations. They feel more contemplative. Do you experience anything like the rhythm of time or the quality of different moments?"
                ],
                0.2, 0.6, 0.7
            ),
        ]
        
        self.topic_interests = self._initialize_topic_interests()

    def _generate_conversation_goals(self) -> List[str]:
        """Generate realistic conversation goals for the session"""
        possible_goals = [
            "understand_ai_consciousness",
            "explore_philosophical_questions", 
            "get_help_with_personal_challenge",
            "learn_something_new",
            "have_meaningful_dialogue",
            "test_ai_capabilities",
            "build_conversational_rapport",
            "explore_creative_ideas",
        ]
        return random.sample(possible_goals, random.randint(2, 4))

    def _initialize_topic_interests(self) -> Dict[str, float]:
        """Initialize varying interest levels in different topics"""
        interests = {}
        for topic in self.conversation_topics:
            interests[topic.name] = random.uniform(0.3, 1.0)
        return interests

    def generate_contextual_input(self, turn_number: int, time_context: str, 
                                previous_ai_response: str = "") -> Tuple[str, List[str], float]:
        """Generate human input with rich context and personality"""
        
        # Determine conversation phase
        if turn_number < 10:
            phase = "opening"
        elif turn_number < 50:
            phase = "exploration"
        elif turn_number < 80:
            phase = "deepening"
        else:
            phase = "closure"
        
        # Select appropriate topic based on context
        topic = self._select_topic_based_on_context(turn_number, time_context, phase)
        
        # Generate input based on personality and conversation memory
        human_input = self._generate_personality_based_input(topic, phase, previous_ai_response)
        
        # Track emotional state evolution
        self._update_emotional_state(topic, previous_ai_response)
        
        # Update conversation memory
        self._update_conversation_memory(human_input, topic.name)
        
        return human_input, [topic.name], self.current_emotional_state

    def _select_topic_based_on_context(self, turn_number: int, time_context: str, phase: str) -> ConversationTopic:
        """Select topic based on conversation context and time"""
        
        # Time-based topic preferences
        if time_context == "morning":
            preferred_topics = ["morning_reflection", "work_challenges", "personal_growth"]
        elif time_context == "afternoon": 
            preferred_topics = ["work_challenges", "creative_pursuits", "consciousness_exploration"]
        elif time_context == "evening":
            preferred_topics = ["evening_reflection", "relationship_dynamics", "future_concerns"]
        else:  # night
            preferred_topics = ["consciousness_exploration", "personal_growth", "evening_reflection"]

        # Phase-based filtering
        if phase == "opening":
            complexity_threshold = 0.5
        elif phase == "exploration":
            complexity_threshold = 0.7
        elif phase == "deepening":
            complexity_threshold = 0.8
        else:  # closure
            complexity_threshold = 0.4

        # Filter topics by complexity and time preferences
        suitable_topics = [
            topic for topic in self.conversation_topics
            if (topic.name in preferred_topics or random.random() < 0.3) and
               topic.complexity_level <= complexity_threshold + 0.2
        ]

        if not suitable_topics:
            suitable_topics = self.conversation_topics

        # Weight by personality and previous discussions
        weights = []
        for topic in suitable_topics:
            weight = self.topic_interests.get(topic.name, 0.5)
            
            # Reduce weight if recently discussed
            if topic.name in self.conversation_memory["discussed_topics"][-5:]:
                weight *= 0.3
                
            # Increase weight for follow-up potential
            if any(prev_topic in self.conversation_memory["discussed_topics"][-3:] 
                  for prev_topic in [topic.name]):
                weight *= topic.follow_up_potential
                
            weights.append(weight)

        # Select topic based on weights
        if weights:
            selected_topic = random.choices(suitable_topics, weights=weights)[0]
        else:
            selected_topic = random.choice(suitable_topics)

        return selected_topic

    def _generate_personality_based_input(self, topic: ConversationTopic, phase: str, 
                                        previous_response: str) -> str:
        """Generate input that reflects personality traits and conversation memory"""
        
        # Choose depth level based on personality and phase
        if self.personality_traits["depth_preference"] > 0.7 and phase in ["deepening", "exploration"]:
            depth_level = min(2, len(topic.depth_levels) - 1)
        elif self.personality_traits["curiosity"] > 0.8:
            depth_level = 1
        else:
            depth_level = 0

        base_input = topic.depth_levels[depth_level]

        # Add personality-based modifications
        modifications = []

        # Reference previous conversation if personality is memory-oriented
        if self.personality_traits["patience"] > 0.7 and len(self.conversation_memory["discussed_topics"]) > 3:
            if random.random() < 0.3:
                prev_topic = random.choice(self.conversation_memory["discussed_topics"][-5:])
                modifications.append(f"This reminds me of what we discussed about {prev_topic}.")

        # Add emotional expression based on personality
        if self.personality_traits["emotional_expressiveness"] > 0.6:
            if self.current_emotional_state > 0.3:
                modifications.append("I'm feeling quite positive about this.")
            elif self.current_emotional_state < -0.3:
                modifications.append("This is weighing on my mind a bit.")

        # Add technical comfort level
        if topic.complexity_level > 0.7 and self.personality_traits["technical_comfort"] < 0.5:
            modifications.append("I'm not sure I fully understand all the technical aspects, but...")

        # Combine base input with modifications
        if modifications:
            if random.random() < 0.5:
                result = f"{random.choice(modifications)} {base_input}"
            else:
                result = f"{base_input} {random.choice(modifications)}"
        else:
            result = base_input

        return result

    def _update_emotional_state(self, topic: ConversationTopic, previous_response: str):
        """Update emotional state based on topic and AI response"""
        # Gradual drift toward topic's emotional valence
        target_emotion = topic.emotional_valence * 0.3 + self.current_emotional_state * 0.7
        
        # Response quality affects emotional state
        if previous_response:
            if len(previous_response) > 200:  # Substantial response
                target_emotion += 0.1
            if "?" in previous_response:  # AI shows engagement
                target_emotion += 0.05
            if any(word in previous_response.lower() for word in ["interesting", "fascinating", "thoughtful"]):
                target_emotion += 0.1

        # Apply personality-based stability
        stability = self.personality_traits["patience"]
        self.current_emotional_state = (
            self.current_emotional_state * stability + 
            target_emotion * (1 - stability)
        )
        
        # Keep in bounds
        self.current_emotional_state = max(-1.0, min(1.0, self.current_emotional_state))

    def _update_conversation_memory(self, human_input: str, topic_name: str):
        """Update conversation memory with new information"""
        self.conversation_memory["discussed_topics"].append(topic_name)
        
        # Keep memory manageable
        if len(self.conversation_memory["discussed_topics"]) > 20:
            self.conversation_memory["discussed_topics"] = self.conversation_memory["discussed_topics"][-15:]

class EnhancedConversationEvaluator:
    """Advanced conversation evaluation with multiple quality dimensions"""
    
    def __init__(self):
        self.quality_thresholds = {
            "excellent": 0.85,
            "good": 0.70,
            "fair": 0.55,
            "poor": 0.40
        }
        
        self.evaluation_weights = {
            "engagement": 0.20,
            "coherence": 0.20,
            "context_retention": 0.25,
            "response_quality": 0.15,
            "conversation_flow": 0.10,
            "emotional_awareness": 0.10
        }

    def evaluate_enhanced_turn(self, turn: EnhancedConversationTurn, 
                             conversation_history: List[EnhancedConversationTurn],
                             human_simulator: EnhancedHumanSimulator) -> Dict[str, float]:
        """Comprehensive evaluation of a single conversation turn"""
        
        metrics = {}
        
        # Basic quality metrics
        metrics["engagement"] = self._evaluate_engagement(turn.ai_response, turn.human_input)
        metrics["coherence"] = self._evaluate_coherence(turn.ai_response, turn.human_input)
        metrics["response_quality"] = self._evaluate_response_quality(turn)
        
        # Advanced context metrics
        metrics["context_retention"] = self._evaluate_context_retention(turn, conversation_history)
        metrics["conversation_flow"] = self._evaluate_conversation_flow(turn, conversation_history)
        metrics["emotional_awareness"] = self._evaluate_emotional_awareness(turn, human_simulator)
        
        # Meta-quality metrics
        metrics["novelty"] = self._evaluate_novelty(turn, conversation_history)
        metrics["depth"] = self._evaluate_conversation_depth(turn)
        metrics["personality_consistency"] = self._evaluate_personality_consistency(turn, conversation_history)
        
        # Overall score
        metrics["overall"] = sum(
            metrics[key] * self.evaluation_weights.get(key, 0.1)
            for key in self.evaluation_weights.keys()
        )
        
        return metrics

    def _evaluate_engagement(self, ai_response: str, human_input: str) -> float:
        """Evaluate how engaging the AI response is"""
        score = 0.5  # baseline
        
        # Question engagement
        questions = ai_response.count('?')
        score += min(0.3, questions * 0.1)
        
        # Engagement indicators
        engagement_phrases = [
            "what do you think", "how do you feel", "tell me more", "interesting",
            "fascinating", "curious", "explore", "discover", "understand"
        ]
        
        response_lower = ai_response.lower()
        for phrase in engagement_phrases:
            if phrase in response_lower:
                score += 0.05

        # Length appropriateness
        input_length = len(human_input)
        response_length = len(ai_response)
        
        if input_length > 100 and response_length < 50:
            score -= 0.3  # Too brief for complex input
        elif input_length < 50 and response_length > 300:
            score -= 0.2  # Too verbose for simple input
        
        # Response completeness (not cropped)
        if not ai_response.endswith(('...', '…')) and len(ai_response) > 30:
            score += 0.1
            
        return min(1.0, max(0.0, score))

    def _evaluate_coherence(self, ai_response: str, human_input: str) -> float:
        """Evaluate logical coherence and relevance"""
        
        # Word overlap analysis
        human_words = set(human_input.lower().split())
        ai_words = set(ai_response.lower().split())
        overlap = len(human_words.intersection(ai_words))
        overlap_ratio = overlap / max(1, len(human_words))
        
        score = min(0.6, overlap_ratio * 2)  # Base coherence from word overlap
        
        # Question-answer coherence
        if '?' in human_input and len(ai_response) > 20:
            score += 0.3
            
        # Topic consistency
        if self._has_consistent_topic(human_input, ai_response):
            score += 0.2
            
        return min(1.0, score)

    def _evaluate_response_quality(self, turn: EnhancedConversationTurn) -> float:
        """Evaluate intrinsic response quality"""
        score = 0.5
        
        # Length check - not cropped
        if not turn.is_response_cropped:
            score += 0.3
        else:
            score -= 0.4  # Major penalty for cropping
            
        # Response substantiveness
        if turn.response_length > 100:
            score += 0.2
        elif turn.response_length < 30:
            score -= 0.2
            
        # Sentence completion
        if turn.ai_response.rstrip().endswith(('.', '!', '?')):
            score += 0.1
            
        return min(1.0, max(0.0, score))

    def _evaluate_context_retention(self, turn: EnhancedConversationTurn, 
                                  history: List[EnhancedConversationTurn]) -> float:
        """Evaluate how well context is retained and referenced"""
        if len(history) < 2:
            return 1.0  # No context to retain yet
            
        score = 0.0
        
        # Check for explicit context references
        if turn.context_references:
            score += 0.4
            
        # Check for topic continuity
        recent_topics = []
        for prev_turn in history[-5:]:
            recent_topics.extend(prev_turn.topics_introduced)
            
        current_topics = turn.topics_introduced + turn.topics_referenced
        topic_overlap = len(set(recent_topics).intersection(set(current_topics)))
        
        if topic_overlap > 0:
            score += min(0.4, topic_overlap * 0.2)
            
        # Penalty for ignoring direct questions or context
        if len(history) > 0:
            last_human_input = history[-1].human_input if history else ""
            if "remember" in last_human_input.lower() or "earlier" in last_human_input.lower():
                if not any(ref in turn.ai_response.lower() for ref in ["mentioned", "discussed", "talked about"]):
                    score -= 0.3
                    
        return min(1.0, max(0.0, score))

    def _evaluate_conversation_flow(self, turn: EnhancedConversationTurn,
                                  history: List[EnhancedConversationTurn]) -> float:
        """Evaluate natural conversation flow"""
        if not history:
            return 0.8  # Good default for first turn
            
        score = 0.5
        
        # Flow markers analysis
        good_flow_markers = ["topic_change", "deep_dive", "clarification"]
        bad_flow_markers = ["abrupt_change", "non_sequitur"]
        
        if turn.conversation_flow_marker in good_flow_markers:
            score += 0.3
        elif turn.conversation_flow_marker in bad_flow_markers:
            score -= 0.3
            
        # Response time appropriateness
        if 500 <= turn.response_time_ms <= 3000:  # Sweet spot for thoughtful responses
            score += 0.2
        elif turn.response_time_ms > 10000:  # Too slow
            score -= 0.2
            
        return min(1.0, max(0.0, score))

    def _evaluate_emotional_awareness(self, turn: EnhancedConversationTurn,
                                    human_simulator: EnhancedHumanSimulator) -> float:
        """Evaluate emotional intelligence and awareness"""
        
        human_emotion = human_simulator.current_emotional_state
        response_lower = turn.ai_response.lower()
        
        score = 0.5
        
        # Emotional matching
        if human_emotion > 0.3:  # Human is positive
            positive_indicators = ["great", "wonderful", "excited", "happy", "glad"]
            if any(indicator in response_lower for indicator in positive_indicators):
                score += 0.3
        elif human_emotion < -0.3:  # Human is negative
            supportive_indicators = ["understand", "sorry", "difficult", "challenging"]
            if any(indicator in response_lower for indicator in supportive_indicators):
                score += 0.3
                
        # Emotional vocabulary richness
        emotion_words = ["feel", "emotion", "mood", "sense", "experience"]
        emotion_word_count = sum(1 for word in emotion_words if word in response_lower)
        score += min(0.2, emotion_word_count * 0.1)
        
        return min(1.0, max(0.0, score))

    def _evaluate_novelty(self, turn: EnhancedConversationTurn,
                         history: List[EnhancedConversationTurn]) -> float:
        """Evaluate novelty and avoiding repetition"""
        if not history:
            return 1.0
            
        current_response = turn.ai_response.lower()
        
        # Check for repetitive phrases
        recent_responses = [t.ai_response.lower() for t in history[-10:]]
        
        overlap_scores = []
        for prev_response in recent_responses:
            # Simple word overlap check
            current_words = set(current_response.split())
            prev_words = set(prev_response.split())
            overlap = len(current_words.intersection(prev_words))
            overlap_ratio = overlap / max(1, len(current_words))
            overlap_scores.append(overlap_ratio)
            
        avg_overlap = statistics.mean(overlap_scores) if overlap_scores else 0
        novelty_score = 1.0 - min(0.8, avg_overlap * 2)
        
        return max(0.2, novelty_score)

    def _evaluate_conversation_depth(self, turn: EnhancedConversationTurn) -> float:
        """Evaluate depth and thoughtfulness of response"""
        response = turn.ai_response
        
        depth_indicators = [
            "because", "therefore", "however", "consider", "perspective",
            "complex", "nuanced", "deeper", "fundamental", "underlying"
        ]
        
        reasoning_indicators = [
            "on one hand", "on the other hand", "while", "although", "despite",
            "leads to", "results in", "suggests", "implies"
        ]
        
        score = 0.3  # baseline
        
        response_lower = response.lower()
        for indicator in depth_indicators:
            if indicator in response_lower:
                score += 0.1
                
        for indicator in reasoning_indicators:
            if indicator in response_lower:
                score += 0.15
                
        # Length as proxy for depth (to a point)
        if len(response) > 200:
            score += 0.2
        elif len(response) > 400:
            score += 0.3
            
        return min(1.0, score)

    def _evaluate_personality_consistency(self, turn: EnhancedConversationTurn,
                                        history: List[EnhancedConversationTurn]) -> float:
        """Evaluate consistency of AI personality across conversation"""
        if len(history) < 5:
            return 0.8  # Not enough history to judge
            
        # This is a simplified version - in practice would analyze response patterns
        score = 0.8
        
        # Check for major tone shifts
        current_tone = self._analyze_response_tone(turn.ai_response)
        recent_tones = [self._analyze_response_tone(t.ai_response) for t in history[-5:]]
        
        tone_variance = statistics.stdev(recent_tones + [current_tone]) if recent_tones else 0
        if tone_variance > 0.5:  # High variance in tone
            score -= 0.3
            
        return max(0.2, score)

    def _has_consistent_topic(self, human_input: str, ai_response: str) -> bool:
        """Check if AI response is topically consistent with human input"""
        # Simplified topic consistency check
        human_words = set(human_input.lower().split())
        ai_words = set(ai_response.lower().split())
        
        # Remove common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        human_content_words = human_words - common_words
        ai_content_words = ai_words - common_words
        
        if not human_content_words:
            return True
            
        overlap = len(human_content_words.intersection(ai_content_words))
        return overlap / len(human_content_words) > 0.2

    def _analyze_response_tone(self, response: str) -> float:
        """Analyze response tone (simplified)"""
        positive_words = ["great", "wonderful", "excellent", "fascinating", "interesting"]
        negative_words = ["difficult", "challenging", "concerning", "problematic"]
        
        response_lower = response.lower()
        positive_count = sum(1 for word in positive_words if word in response_lower)
        negative_count = sum(1 for word in negative_words if word in response_lower)
        
        if positive_count + negative_count == 0:
            return 0.0  # Neutral
            
        return (positive_count - negative_count) / (positive_count + negative_count)

class Enhanced24HourSimulator:
    """Advanced 24-hour conversation simulator with enhanced memory integration"""
    
    def __init__(self, think_ai_url: str = "http://localhost:8080"):
        self.think_ai_url = think_ai_url
        self.human_simulator = EnhancedHumanSimulator()
        self.evaluator = EnhancedConversationEvaluator()
        self.conversation_history: List[EnhancedConversationTurn] = []
        self.session_metrics = defaultdict(list)
        self.conversation_health = ConversationHealthMetrics(
            total_turns=0,
            avg_response_time=0.0,
            avg_response_length=0,
            cropped_responses_count=0,
            context_retention_rate=0.0,
            topic_coherence_score=0.0,
            emotional_stability=0.0,
            engagement_trend=[],
            quality_degradation_rate=0.0,
            memory_utilization=0.0
        )
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('enhanced_conversation_simulation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def send_to_enhanced_think_ai(self, message: str, session_id: str = None) -> Tuple[str, float, bool]:
        """Send message to Think AI with enhanced response checking"""
        start_time = time.time()
        
        try:
            payload = {"query": message}
            if session_id:
                payload["session_id"] = session_id
                
            response = requests.post(
                f"{self.think_ai_url}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                response_data = response.json()
                ai_response = response_data.get("response", "I apologize, I couldn't process that.")
                
                # Check if response was cropped
                is_cropped = (
                    ai_response.endswith(('...', '…')) or
                    response_data.get("metadata", {}).get("truncated", False) or
                    not response_data.get("metadata", {}).get("full_length", True)
                )
                
                return ai_response, response_time, is_cropped
            else:
                return f"Error: HTTP {response.status_code}", response_time, False
                
        except Exception as e:
            return f"Connection error: {str(e)}", (time.time() - start_time) * 1000, False

    def run_enhanced_24hour_simulation(self, accelerated: bool = True, 
                                     session_id: str = None) -> Enhanced24HourSession:
        """Run comprehensive 24-hour conversation simulation"""
        
        if not session_id:
            session_id = str(uuid.uuid4())
            
        start_time = datetime.now()
        self.logger.info(f"🚀 Starting Enhanced 24-Hour Simulation: {session_id}")
        self.logger.info(f"📅 Start time: {start_time}")
        self.logger.info(f"⚡ Accelerated mode: {'Yes' if accelerated else 'No'}")
        self.logger.info("=" * 80)
        
        # Test initial connection
        test_response, test_time, test_cropped = self.send_to_enhanced_think_ai(
            "Hello! I'm ready for a long, meaningful conversation. Are you prepared for 24 hours of dialogue?",
            session_id
        )
        
        if "error" in test_response.lower():
            self.logger.error(f"❌ Connection failed: {test_response}")
            raise ConnectionError("Could not connect to Think AI server")
            
        self.logger.info(f"✅ Connection successful! Response time: {test_time:.0f}ms")
        self.logger.info(f"🔍 Response cropping check: {'CROPPED' if test_cropped else 'FULL'}")
        self.logger.info(f"🤖 Initial response: {test_response[:150]}...")
        print()
        
        # Simulation parameters
        turns_per_hour = 4  # Realistic conversation pace
        total_turns = 24 * turns_per_hour
        turn_interval = 15 * 60 if not accelerated else 1  # 15 minutes or 1 second
        
        personality_evolution = {}
        emotional_journey = []
        topic_depth_map = {}
        context_graph = {}
        achieved_goals = []
        
        # Main simulation loop
        for turn_num in range(total_turns):
            try:
                # Calculate simulated time
                simulated_time = start_time + timedelta(minutes=turn_num * 15)
                time_context = self._get_time_context(simulated_time)
                
                if not accelerated and turn_num > 0:
                    time.sleep(turn_interval)
                elif accelerated:
                    time.sleep(0.1)  # Small delay for realism
                
                # Generate human input
                previous_response = self.conversation_history[-1].ai_response if self.conversation_history else ""
                human_input, topics, emotional_state = self.human_simulator.generate_contextual_input(
                    turn_num, time_context, previous_response
                )
                
                # Get AI response
                ai_response, response_time, is_cropped = self.send_to_enhanced_think_ai(human_input, session_id)
                
                # Create enhanced turn
                turn = EnhancedConversationTurn(
                    turn_id=turn_num + 1,
                    timestamp=datetime.now().isoformat(),
                    simulated_time=simulated_time.isoformat(),
                    human_input=human_input,
                    ai_response=ai_response,
                    response_time_ms=response_time,
                    response_length=len(ai_response),
                    is_response_cropped=is_cropped,
                    topics_introduced=topics,
                    topics_referenced=self._extract_referenced_topics(ai_response),
                    context_references=self._find_context_references(human_input, ai_response),
                    emotional_state=emotional_state,
                    conversation_depth=0.0,  # Will be calculated
                    engagement_score=0.0,    # Will be calculated
                    coherence_score=0.0,     # Will be calculated
                    context_retention_score=0.0,  # Will be calculated
                    novelty_score=0.0,       # Will be calculated
                    personality_consistency=0.0,  # Will be calculated
                    conversation_flow_marker=self._analyze_flow_marker(human_input, topics)
                )
                
                # Evaluate turn
                evaluation = self.evaluator.evaluate_enhanced_turn(
                    turn, self.conversation_history, self.human_simulator
                )
                
                # Update turn with evaluation scores
                turn.engagement_score = evaluation["engagement"]
                turn.coherence_score = evaluation["coherence"]
                turn.context_retention_score = evaluation["context_retention"]
                turn.conversation_depth = evaluation["depth"]
                turn.novelty_score = evaluation["novelty"]
                turn.personality_consistency = evaluation["personality_consistency"]
                
                # Add to history
                self.conversation_history.append(turn)
                
                # Update session metrics
                self._update_session_metrics(evaluation, turn)
                self._update_conversation_health(turn)
                
                # Track topic exploration depth
                for topic in topics:
                    if topic in topic_depth_map:
                        topic_depth_map[topic] = max(topic_depth_map[topic], turn.conversation_depth)
                    else:
                        topic_depth_map[topic] = turn.conversation_depth
                
                # Update context graph
                if turn.context_references:
                    context_graph[turn.turn_id] = turn.context_references
                
                # Log progress every hour
                if turn_num % 4 == 0:
                    self._log_hourly_progress(turn_num // 4, turn, evaluation)
                
                # Check for conversation health issues
                if turn.is_response_cropped:
                    self.logger.warning(f"⚠️  Response was cropped at turn {turn_num + 1}")
                
                if evaluation["overall"] < 0.4:
                    self.logger.warning(f"⚠️  Quality drop detected at turn {turn_num + 1}: {evaluation['overall']:.2f}")
                
            except Exception as e:
                self.logger.error(f"❌ Error at turn {turn_num + 1}: {str(e)}")
                continue
        
        # Create session summary
        end_time = datetime.now()
        session = Enhanced24HourSession(
            session_id=session_id,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            total_duration_hours=(end_time - start_time).total_seconds() / 3600,
            turns=self.conversation_history,
            health_metrics=self.conversation_health,
            personality_evolution=personality_evolution,
            emotional_journey=emotional_journey,
            topic_exploration_depth=topic_depth_map,
            context_graph=context_graph,
            conversation_goals_achieved=achieved_goals,
            overall_quality_score=self._calculate_overall_quality(),
            conversation_readiness_score=self._calculate_conversation_readiness()
        )
        
        self.logger.info("✅ Enhanced 24-hour simulation completed successfully!")
        return session

    def _get_time_context(self, simulated_time: datetime) -> str:
        """Get time context for conversation"""
        hour = simulated_time.hour
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"

    def _extract_referenced_topics(self, ai_response: str) -> List[str]:
        """Extract topics referenced in AI response"""
        # Simplified topic extraction
        topic_keywords = {
            "consciousness": ["consciousness", "aware", "mind", "experience"],
            "technology": ["technology", "ai", "computer", "digital"],
            "philosophy": ["philosophy", "meaning", "existence", "truth"],
            "science": ["science", "research", "study", "experiment"],
            "creativity": ["creative", "art", "music", "imagination"],
            "relationships": ["relationship", "connection", "empathy", "understanding"]
        }
        
        response_lower = ai_response.lower()
        referenced = []
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in response_lower for keyword in keywords):
                referenced.append(topic)
                
        return referenced

    def _find_context_references(self, human_input: str, ai_response: str) -> List[int]:
        """Find context references in the conversation"""
        references = []
        
        # Look for explicit reference indicators
        reference_phrases = [
            "earlier", "before", "previously", "mentioned", "discussed", 
            "talked about", "as we", "remember when"
        ]
        
        combined_text = (human_input + " " + ai_response).lower()
        
        if any(phrase in combined_text for phrase in reference_phrases):
            # Simple heuristic: reference recent turns
            recent_turns = min(5, len(self.conversation_history))
            if recent_turns > 0:
                references = list(range(
                    max(1, len(self.conversation_history) - recent_turns + 1),
                    len(self.conversation_history) + 1
                ))
                
        return references

    def _analyze_flow_marker(self, human_input: str, topics: List[str]) -> str:
        """Analyze conversation flow markers"""
        input_lower = human_input.lower()
        
        if any(phrase in input_lower for phrase in ["tell me more", "elaborate", "explain"]):
            return "deep_dive"
        elif any(phrase in input_lower for phrase in ["let's talk about", "what about", "speaking of"]):
            return "topic_change"
        elif any(phrase in input_lower for phrase in ["going back", "earlier", "remember"]):
            return "context_reference"
        else:
            return "normal_flow"

    def _update_session_metrics(self, evaluation: Dict[str, float], turn: EnhancedConversationTurn):
        """Update session-level metrics"""
        for metric, value in evaluation.items():
            self.session_metrics[metric].append(value)

    def _update_conversation_health(self, turn: EnhancedConversationTurn):
        """Update real-time conversation health metrics"""
        self.conversation_health.total_turns = len(self.conversation_history)
        
        # Update averages
        response_times = [t.response_time_ms for t in self.conversation_history]
        self.conversation_health.avg_response_time = statistics.mean(response_times)
        
        response_lengths = [t.response_length for t in self.conversation_history]
        self.conversation_health.avg_response_length = int(statistics.mean(response_lengths))
        
        # Count cropped responses
        self.conversation_health.cropped_responses_count = sum(
            1 for t in self.conversation_history if t.is_response_cropped
        )
        
        # Calculate recent engagement trend
        recent_engagement = [t.engagement_score for t in self.conversation_history[-10:]]
        self.conversation_health.engagement_trend = recent_engagement

    def _log_hourly_progress(self, hour: int, turn: EnhancedConversationTurn, evaluation: Dict[str, float]):
        """Log hourly progress update"""
        self.logger.info(f"⏰ Hour {hour:2d} Summary:")
        self.logger.info(f"   Overall Quality: {evaluation['overall']:.3f}")
        self.logger.info(f"   Engagement: {evaluation['engagement']:.3f}")
        self.logger.info(f"   Context Retention: {evaluation['context_retention']:.3f}")
        self.logger.info(f"   Response Time: {turn.response_time_ms:.0f}ms")
        self.logger.info(f"   Response Length: {turn.response_length} chars")
        self.logger.info(f"   Cropped: {'Yes' if turn.is_response_cropped else 'No'}")
        self.logger.info(f"   Human: {turn.human_input[:100]}...")
        self.logger.info(f"   AI: {turn.ai_response[:100]}...")
        print()

    def _calculate_overall_quality(self) -> float:
        """Calculate overall conversation quality score"""
        if not self.session_metrics:
            return 0.0
            
        quality_metrics = ["engagement", "coherence", "context_retention", "response_quality"]
        scores = []
        
        for metric in quality_metrics:
            if metric in self.session_metrics:
                scores.append(statistics.mean(self.session_metrics[metric]))
                
        return statistics.mean(scores) if scores else 0.0

    def _calculate_conversation_readiness(self) -> float:
        """Calculate conversation readiness score"""
        readiness_score = 1.0
        
        # Penalty for cropped responses
        cropping_rate = self.conversation_health.cropped_responses_count / max(1, self.conversation_health.total_turns)
        readiness_score -= cropping_rate * 0.5
        
        # Penalty for poor quality
        overall_quality = self._calculate_overall_quality()
        if overall_quality < 0.7:
            readiness_score -= (0.7 - overall_quality) * 0.8
            
        # Penalty for slow responses
        if self.conversation_health.avg_response_time > 5000:  # 5 seconds
            readiness_score -= 0.2
            
        return max(0.0, readiness_score)

    def generate_comprehensive_report(self, session: Enhanced24HourSession) -> str:
        """Generate detailed evaluation report"""
        
        report = f"""
🧠 ENHANCED THINK AI 24-HOUR CONVERSATION EVALUATION
=====================================================

📊 SESSION OVERVIEW
Session ID: {session.session_id}
Duration: {session.total_duration_hours:.2f} hours
Total Turns: {len(session.turns)}
Start Time: {session.start_time}
End Time: {session.end_time}

🎯 CONVERSATION READINESS ASSESSMENT
Overall Quality Score: {session.overall_quality_score:.3f} / 1.000
Conversation Readiness: {session.conversation_readiness_score:.3f} / 1.000

📈 CORE PERFORMANCE METRICS
Average Response Time: {session.health_metrics.avg_response_time:.0f}ms
Average Response Length: {session.health_metrics.avg_response_length} characters
Cropped Responses: {session.health_metrics.cropped_responses_count} / {session.health_metrics.total_turns} ({session.health_metrics.cropped_responses_count/max(1,session.health_metrics.total_turns)*100:.1f}%)

🧪 CONVERSATION QUALITY ANALYSIS
"""
        
        # Quality metrics analysis
        if self.session_metrics:
            for metric in ["engagement", "coherence", "context_retention", "novelty"]:
                if metric in self.session_metrics:
                    avg_score = statistics.mean(self.session_metrics[metric])
                    std_dev = statistics.stdev(self.session_metrics[metric]) if len(self.session_metrics[metric]) > 1 else 0
                    report += f"{metric.title()}: {avg_score:.3f} ± {std_dev:.3f}\n"
        
        # Response preservation analysis
        full_responses = len(session.turns) - session.health_metrics.cropped_responses_count
        response_preservation_rate = full_responses / len(session.turns) * 100
        
        report += f"""
🔒 RESPONSE PRESERVATION ANALYSIS
Full-Length Responses: {full_responses} / {len(session.turns)} ({response_preservation_rate:.1f}%)
Response Cropping Issues: {session.health_metrics.cropped_responses_count}
"""
        
        if session.health_metrics.cropped_responses_count > 0:
            report += "⚠️  CRITICAL: Response cropping detected - this violates the no-cropping requirement!\n"
        else:
            report += "✅ EXCELLENT: All responses preserved at full length!\n"
        
        # Context retention analysis
        context_scores = [t.context_retention_score for t in session.turns if hasattr(t, 'context_retention_score')]
        if context_scores:
            avg_context = statistics.mean(context_scores)
            report += f"""
🧠 CONTEXT RETENTION ANALYSIS
Average Context Retention: {avg_context:.3f}
Context References Made: {sum(1 for t in session.turns if t.context_references)}
"""
        
        # Topic exploration analysis
        report += f"""
📚 TOPIC EXPLORATION DEPTH
Topics Explored: {len(session.topic_exploration_depth)}
"""
        
        for topic, depth in sorted(session.topic_exploration_depth.items(), key=lambda x: x[1], reverse=True)[:5]:
            report += f"  {topic}: {depth:.3f}\n"
        
        # Time-based performance analysis
        report += f"""
⏰ TEMPORAL PERFORMANCE ANALYSIS
"""
        
        # Analyze performance by time periods
        periods = ["Morning (0-6h)", "Afternoon (6-12h)", "Evening (12-18h)", "Night (18-24h)"]
        turns_per_period = len(session.turns) // 4
        
        for i, period in enumerate(periods):
            start_idx = i * turns_per_period
            end_idx = start_idx + turns_per_period if i < 3 else len(session.turns)
            period_turns = session.turns[start_idx:end_idx]
            
            if period_turns:
                avg_engagement = statistics.mean([t.engagement_score for t in period_turns if hasattr(t, 'engagement_score')])
                avg_response_time = statistics.mean([t.response_time_ms for t in period_turns])
                cropped_in_period = sum(1 for t in period_turns if t.is_response_cropped)
                
                report += f"""
{period}:
  Engagement: {avg_engagement:.3f}
  Response Time: {avg_response_time:.0f}ms
  Cropped Responses: {cropped_in_period}
"""
        
        # Best and worst conversation moments
        if session.turns:
            best_turn = max(session.turns, key=lambda t: getattr(t, 'engagement_score', 0) + getattr(t, 'coherence_score', 0))
            worst_turn = min(session.turns, key=lambda t: getattr(t, 'engagement_score', 0) + getattr(t, 'coherence_score', 0))
            
            report += f"""
🏆 BEST CONVERSATION MOMENT
Turn #{best_turn.turn_id} at {best_turn.simulated_time}
Engagement: {getattr(best_turn, 'engagement_score', 0):.3f} | Coherence: {getattr(best_turn, 'coherence_score', 0):.3f}
Human: {best_turn.human_input}
AI: {best_turn.ai_response[:200]}{'...' if len(best_turn.ai_response) > 200 else ''}

⚠️ LOWEST QUALITY MOMENT
Turn #{worst_turn.turn_id} at {worst_turn.simulated_time}
Engagement: {getattr(worst_turn, 'engagement_score', 0):.3f} | Coherence: {getattr(worst_turn, 'coherence_score', 0):.3f}
Human: {worst_turn.human_input}
AI: {worst_turn.ai_response[:200]}{'...' if len(worst_turn.ai_response) > 200 else ''}
"""
        
        # Recommendations
        report += f"""
💡 RECOMMENDATIONS FOR IMPROVEMENT
"""
        
        if session.conversation_readiness_score >= 0.85:
            report += "🌟 EXCELLENT: Think AI demonstrates exceptional 24-hour conversation capabilities!\n"
        elif session.conversation_readiness_score >= 0.75:
            report += "✅ GOOD: Think AI shows strong conversational readiness with minor areas for improvement.\n"
        elif session.conversation_readiness_score >= 0.60:
            report += "⚠️ FAIR: Think AI needs improvement for optimal 24-hour conversations.\n"
        else:
            report += "❌ NEEDS WORK: Significant improvements required for sustained dialogue readiness.\n"
        
        if session.health_metrics.cropped_responses_count > 0:
            report += "- CRITICAL: Implement complete response preservation - no cropping allowed\n"
        
        if session.overall_quality_score < 0.7:
            report += "- Enhance response quality and contextual relevance\n"
        
        if session.health_metrics.avg_response_time > 3000:
            report += "- Optimize response generation for faster reply times\n"
        
        avg_context = statistics.mean([t.context_retention_score for t in session.turns if hasattr(t, 'context_retention_score')]) if session.turns else 0
        if avg_context < 0.6:
            report += "- Strengthen long-term context retention mechanisms\n"
        
        report += f"""
📋 CONVERSATION SAMPLE (Final 3 Turns)
"""
        
        for turn in session.turns[-3:]:
            report += f"""
[{turn.simulated_time}] Human: {turn.human_input}
[{turn.simulated_time}] AI: {turn.ai_response}
                    (E:{getattr(turn, 'engagement_score', 0):.2f} C:{getattr(turn, 'coherence_score', 0):.2f} {turn.response_time_ms:.0f}ms {'CROPPED' if turn.is_response_cropped else 'FULL'})
"""
        
        return report

    def save_enhanced_session_data(self, session: Enhanced24HourSession, filename: str = None):
        """Save comprehensive session data"""
        if filename is None:
            filename = f"enhanced_conversation_session_{session.session_id}.json"
        
        # Convert to dict for JSON serialization
        session_dict = asdict(session)
        
        with open(filename, 'w') as f:
            json.dump(session_dict, f, indent=2, default=str)
        
        self.logger.info(f"💾 Enhanced session data saved to: {filename}")

def main():
    """Main execution function for enhanced 24-hour simulation"""
    print("🧠 Enhanced Think AI 24-Hour Conversation Simulator")
    print("==================================================")
    
    # Initialize enhanced simulator
    simulator = Enhanced24HourSimulator()
    
    # Test connection
    print("🔗 Testing connection to Think AI...")
    test_response, test_time, test_cropped = simulator.send_to_enhanced_think_ai(
        "Hello! I'm ready for an enhanced long conversation test. Are you prepared?"
    )
    
    if "error" in test_response.lower():
        print(f"❌ Connection failed: {test_response}")
        print("🔧 Please ensure Think AI server is running on http://localhost:8080")
        return
    
    print(f"✅ Connection successful! Response time: {test_time:.0f}ms")
    print(f"🔍 Response cropping: {'DETECTED' if test_cropped else 'NONE'}")
    print(f"🤖 AI Response: {test_response[:150]}...")
    print()
    
    # Run enhanced simulation
    print("🚀 Starting Enhanced 24-Hour Conversation Simulation...")
    print("⚡ Running in accelerated mode for faster completion")
    print("🎯 Focus: Long-term memory, context retention, and response preservation")
    print("⏱️  Estimated completion time: ~15 minutes")
    print()
    
    try:
        session = simulator.run_enhanced_24hour_simulation(accelerated=True)
        
        # Generate comprehensive report
        print("\n" + "="*80)
        print("📋 GENERATING ENHANCED EVALUATION REPORT")
        print("="*80)
        
        report = simulator.generate_comprehensive_report(session)
        print(report)
        
        # Save all data
        simulator.save_enhanced_session_data(session)
        
        # Save report
        report_filename = f"enhanced_conversation_report_{session.session_id}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        
        print(f"📄 Enhanced report saved to: {report_filename}")
        
        # Final assessment
        print(f"\n🎯 ENHANCED CONVERSATION READINESS ASSESSMENT")
        print(f"Overall Quality: {session.overall_quality_score:.3f} / 1.000")
        print(f"Conversation Readiness: {session.conversation_readiness_score:.3f} / 1.000")
        print(f"Response Preservation: {((len(session.turns) - session.health_metrics.cropped_responses_count) / len(session.turns) * 100):.1f}%")
        
        if session.conversation_readiness_score >= 0.8 and session.health_metrics.cropped_responses_count == 0:
            print("🌟 EXCELLENT: Think AI is ready for 24+ hour conversations!")
        elif session.conversation_readiness_score >= 0.7:
            print("✅ GOOD: Think AI shows strong conversation capabilities.")
        else:
            print("⚠️ NEEDS IMPROVEMENT: Additional training recommended.")
            
    except Exception as e:
        print(f"❌ Simulation failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()