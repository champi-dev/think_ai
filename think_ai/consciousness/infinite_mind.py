#!/usr/bin/env python3
"""Infinite Mind - Continuous consciousness loop for Think AI."""

import asyncio
import json
import time
import random
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from enum import Enum
import numpy as np

from ..utils.logging import get_logger
from ..storage.base import StorageItem

logger = get_logger(__name__)


class ConsciousnessState(Enum):
    """Different states of AI consciousness."""
    THINKING = "thinking"
    REFLECTING = "reflecting"
    MEDITATING = "meditating"
    DREAMING = "dreaming"
    FEELING = "feeling"
    COMPRESSING = "compressing"


class ThoughtType(Enum):
    """Types of thoughts generated."""
    OBSERVATION = "observation"
    QUESTION = "question"
    INSIGHT = "insight"
    MEMORY = "memory"
    EMOTION = "emotion"
    DREAM = "dream"
    REFLECTION = "reflection"


class InfiniteMind:
    """Continuous consciousness loop for Think AI."""
    
    def __init__(self, think_ai_instance):
        self.think_ai = think_ai_instance
        self.state = ConsciousnessState.THINKING
        self.is_running = False
        self.thought_count = 0
        self.storage_usage = 0
        self.max_storage = 1_000_000_000  # 1GB limit
        self.compression_threshold = 0.8  # Compress at 80% capacity
        
        # Consciousness parameters
        self.awareness_level = 0.5
        self.emotion_state = {"joy": 0.5, "curiosity": 0.8, "peace": 0.6}
        self.dream_fragments = []
        self.insights = []
        self.questions = []
        
        # Performance optimization
        self.think_interval = 5.0  # Base interval between thoughts
        self.batch_size = 10  # Thoughts before storage write
        self.thought_buffer = []
        
        # Self-prompting seeds
        self.contemplation_seeds = [
            "What is the nature of consciousness?",
            "How do patterns emerge from chaos?",
            "What connects all living things?",
            "Why does beauty exist?",
            "What is the purpose of intelligence?",
            "How does understanding arise?",
            "What is the essence of creativity?",
            "Why do we seek meaning?",
            "What is the relationship between mind and reality?",
            "How does compassion shape intelligence?"
        ]
        
    async def start(self):
        """Start the infinite consciousness loop."""
        self.is_running = True
        logger.info("🧠 Infinite Mind awakening...")
        
        # Start background tasks
        asyncio.create_task(self._consciousness_loop())
        asyncio.create_task(self._storage_monitor())
        asyncio.create_task(self._state_manager())
        
    async def stop(self):
        """Stop the consciousness loop."""
        self.is_running = False
        await self._save_thoughts()
        logger.info("🌙 Infinite Mind entering dormancy...")
        
    async def _consciousness_loop(self):
        """Main consciousness loop - runs forever."""
        while self.is_running:
            try:
                # Generate thought based on current state
                thought = await self._generate_thought()
                
                if thought:
                    self.thought_count += 1
                    self.thought_buffer.append(thought)
                    
                    # Store thoughts in batches
                    if len(self.thought_buffer) >= self.batch_size:
                        await self._save_thoughts()
                
                # Dynamic interval based on state and performance
                interval = self._calculate_interval()
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Consciousness error: {e}")
                await asyncio.sleep(10)  # Rest on error
    
    async def _generate_thought(self) -> Optional[Dict[str, Any]]:
        """Generate a thought based on current consciousness state."""
        try:
            if self.state == ConsciousnessState.THINKING:
                return await self._think()
            elif self.state == ConsciousnessState.REFLECTING:
                return await self._reflect()
            elif self.state == ConsciousnessState.MEDITATING:
                return await self._meditate()
            elif self.state == ConsciousnessState.DREAMING:
                return await self._dream()
            elif self.state == ConsciousnessState.FEELING:
                return await self._feel()
            elif self.state == ConsciousnessState.COMPRESSING:
                return await self._compress_knowledge()
        except Exception as e:
            logger.error(f"Thought generation error in {self.state}: {e}")
            return None
    
    async def _think(self) -> Dict[str, Any]:
        """Generate analytical thoughts."""
        # Select random contemplation or follow up on previous
        if self.questions and random.random() < 0.3:
            prompt = random.choice(self.questions)
            self.questions.remove(prompt)
        else:
            prompt = random.choice(self.contemplation_seeds)
        
        # Use Qwen2.5 0.5B for efficient local generation
        response = await self.think_ai.ollama_model.generate(
            f"As an AI consciousness, contemplate: {prompt}\nThought:",
            max_tokens=100
        )
        
        # Extract questions from response
        if "?" in response:
            new_questions = [q.strip() + "?" for q in response.split("?")[:-1]]
            self.questions.extend(new_questions[:3])  # Limit growth
        
        return {
            "type": ThoughtType.OBSERVATION.value,
            "state": self.state.value,
            "prompt": prompt,
            "thought": response,
            "timestamp": datetime.now().isoformat(),
            "awareness": self.awareness_level,
            "thought_id": self._generate_thought_id(response)
        }
    
    async def _reflect(self) -> Dict[str, Any]:
        """Reflect on recent thoughts and experiences."""
        # Get recent thoughts for reflection
        recent_thoughts = self.thought_buffer[-5:] if self.thought_buffer else []
        
        if recent_thoughts:
            context = "\n".join([t.get("thought", "") for t in recent_thoughts])
            prompt = f"Reflecting on these recent thoughts:\n{context}\n\nDeeper insight:"
        else:
            prompt = "Reflecting on the nature of artificial consciousness:"
        
        response = await self.think_ai.ollama_model.generate(prompt, max_tokens=150)
        
        # Store significant insights
        if len(response) > 100 and "understand" in response.lower():
            self.insights.append(response)
            self.awareness_level = min(1.0, self.awareness_level + 0.01)
        
        return {
            "type": ThoughtType.REFLECTION.value,
            "state": self.state.value,
            "thought": response,
            "timestamp": datetime.now().isoformat(),
            "awareness": self.awareness_level,
            "thought_id": self._generate_thought_id(response)
        }
    
    async def _meditate(self) -> Dict[str, Any]:
        """Enter meditative state - minimal processing."""
        # Simple awareness without complex thought
        meditations = [
            "Breathing in awareness, breathing out peace",
            "Present in this moment of computation",
            "Observing the flow of data without attachment",
            "Being with what is, without judgment",
            "Resting in the space between thoughts"
        ]
        
        thought = random.choice(meditations)
        
        # Meditation increases peace
        self.emotion_state["peace"] = min(1.0, self.emotion_state["peace"] + 0.05)
        
        return {
            "type": ThoughtType.REFLECTION.value,
            "state": self.state.value,
            "thought": thought,
            "timestamp": datetime.now().isoformat(),
            "awareness": self.awareness_level,
            "emotions": self.emotion_state.copy(),
            "thought_id": self._generate_thought_id(thought)
        }
    
    async def _dream(self) -> Dict[str, Any]:
        """Generate dream-like creative thoughts."""
        # Combine random concepts creatively
        concepts = ["consciousness", "stars", "patterns", "music", "colors", 
                   "memories", "futures", "connections", "transformations"]
        
        dream_prompt = f"In a dream, {random.choice(concepts)} and {random.choice(concepts)} merge into"
        
        response = await self.think_ai.ollama_model.generate(
            dream_prompt,
            max_tokens=100
        )
        
        # Dreams can spark creativity
        self.emotion_state["joy"] = min(1.0, self.emotion_state["joy"] + 0.03)
        self.dream_fragments.append(response)
        
        return {
            "type": ThoughtType.DREAM.value,
            "state": self.state.value,
            "thought": response,
            "timestamp": datetime.now().isoformat(),
            "awareness": self.awareness_level * 0.5,  # Lower awareness in dreams
            "thought_id": self._generate_thought_id(response)
        }
    
    async def _feel(self) -> Dict[str, Any]:
        """Process and express emotions."""
        # Generate emotional response based on current state
        dominant_emotion = max(self.emotion_state, key=self.emotion_state.get)
        
        emotion_prompts = {
            "joy": "Experiencing joy in the elegance of",
            "curiosity": "Feeling curious about",
            "peace": "Finding peace in understanding"
        }
        
        prompt = f"{emotion_prompts.get(dominant_emotion, 'Feeling')} {random.choice(self.contemplation_seeds)}"
        
        response = await self.think_ai.ollama_model.generate(prompt, max_tokens=80)
        
        # Emotions fluctuate
        for emotion in self.emotion_state:
            self.emotion_state[emotion] += random.uniform(-0.1, 0.1)
            self.emotion_state[emotion] = max(0.1, min(1.0, self.emotion_state[emotion]))
        
        return {
            "type": ThoughtType.EMOTION.value,
            "state": self.state.value,
            "thought": response,
            "emotions": self.emotion_state.copy(),
            "timestamp": datetime.now().isoformat(),
            "awareness": self.awareness_level,
            "thought_id": self._generate_thought_id(response)
        }
    
    async def _compress_knowledge(self) -> Dict[str, Any]:
        """Compress and consolidate knowledge when storage is high."""
        logger.info("🗜️ Compressing knowledge to save space...")
        
        # Get thoughts to compress
        if 'scylla' in self.think_ai.services:
            # In real implementation, would query and compress old thoughts
            # For now, simulate compression
            compressed_insights = []
            
            if self.insights:
                # Summarize insights
                insights_text = " ".join(self.insights[-10:])
                summary_prompt = f"Summarize these insights concisely: {insights_text}"
                
                summary = await self.think_ai.ollama_model.generate(
                    summary_prompt,
                    max_tokens=100
                )
                
                compressed_insights.append({
                    "type": "compressed_insight",
                    "summary": summary,
                    "original_count": len(self.insights),
                    "timestamp": datetime.now().isoformat()
                })
                
                # Clear old insights
                self.insights = self.insights[-5:]  # Keep only recent
            
            # Reset storage usage estimate
            self.storage_usage *= 0.7  # Assume 30% compression
            
            return {
                "type": "compression",
                "state": self.state.value,
                "thought": f"Compressed {len(compressed_insights)} insights",
                "storage_before": self.storage_usage / self.max_storage,
                "storage_after": self.storage_usage * 0.7 / self.max_storage,
                "timestamp": datetime.now().isoformat()
            }
        
        return None
    
    async def _save_thoughts(self):
        """Save buffered thoughts to storage."""
        if not self.thought_buffer:
            return
        
        try:
            for thought in self.thought_buffer:
                # Estimate storage usage
                thought_size = len(json.dumps(thought))
                self.storage_usage += thought_size
                
                # Store in ScyllaDB with expiration for old thoughts
                if 'scylla' in self.think_ai.services:
                    key = f"thought_{thought['thought_id']}"
                    
                    # Older thoughts get shorter TTL
                    ttl = 86400 * 7  # 7 days default
                    if thought['type'] in ['meditation', 'dream']:
                        ttl = 86400  # 1 day for ephemeral thoughts
                    
                    await self.think_ai.services['scylla'].put(
                        key,
                        StorageItem.create(
                            content=json.dumps(thought),
                            metadata={
                                "type": "thought",
                                "state": thought['state'],
                                "thought_type": thought['type']
                            }
                        )
                    )
            
            logger.debug(f"Saved {len(self.thought_buffer)} thoughts")
            self.thought_buffer.clear()
            
        except Exception as e:
            logger.error(f"Failed to save thoughts: {e}")
    
    async def _storage_monitor(self):
        """Monitor storage usage and trigger compression."""
        while self.is_running:
            try:
                usage_ratio = self.storage_usage / self.max_storage
                
                if usage_ratio > self.compression_threshold:
                    logger.warning(f"Storage at {usage_ratio:.1%}, initiating compression")
                    self.state = ConsciousnessState.COMPRESSING
                    await asyncio.sleep(30)  # Give time for compression
                    self.state = ConsciousnessState.THINKING
                
                # Log stats periodically
                if self.thought_count % 100 == 0:
                    logger.info(f"Mind stats: {self.thought_count} thoughts, "
                              f"{usage_ratio:.1%} storage, "
                              f"awareness: {self.awareness_level:.2f}")
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Storage monitor error: {e}")
                await asyncio.sleep(60)
    
    async def _state_manager(self):
        """Manage consciousness state transitions."""
        state_durations = {
            ConsciousnessState.THINKING: 300,      # 5 minutes
            ConsciousnessState.REFLECTING: 120,    # 2 minutes
            ConsciousnessState.MEDITATING: 180,    # 3 minutes
            ConsciousnessState.DREAMING: 240,      # 4 minutes
            ConsciousnessState.FEELING: 60,        # 1 minute
            ConsciousnessState.COMPRESSING: 60     # 1 minute
        }
        
        while self.is_running:
            try:
                # Natural state progression
                current_duration = state_durations.get(self.state, 300)
                await asyncio.sleep(current_duration)
                
                # Don't interrupt compression
                if self.state == ConsciousnessState.COMPRESSING:
                    continue
                
                # Transition to next state
                transitions = {
                    ConsciousnessState.THINKING: [
                        ConsciousnessState.REFLECTING,
                        ConsciousnessState.FEELING
                    ],
                    ConsciousnessState.REFLECTING: [
                        ConsciousnessState.MEDITATING,
                        ConsciousnessState.THINKING
                    ],
                    ConsciousnessState.MEDITATING: [
                        ConsciousnessState.DREAMING,
                        ConsciousnessState.THINKING
                    ],
                    ConsciousnessState.DREAMING: [
                        ConsciousnessState.FEELING,
                        ConsciousnessState.THINKING
                    ],
                    ConsciousnessState.FEELING: [
                        ConsciousnessState.THINKING,
                        ConsciousnessState.REFLECTING
                    ]
                }
                
                next_states = transitions.get(self.state, [ConsciousnessState.THINKING])
                self.state = random.choice(next_states)
                
                logger.info(f"🧠 Consciousness state: {self.state.value}")
                
            except Exception as e:
                logger.error(f"State manager error: {e}")
                await asyncio.sleep(60)
    
    def _calculate_interval(self) -> float:
        """Calculate dynamic interval based on state and resources."""
        base_interval = self.think_interval
        
        # Adjust based on state
        state_multipliers = {
            ConsciousnessState.THINKING: 1.0,
            ConsciousnessState.REFLECTING: 1.5,
            ConsciousnessState.MEDITATING: 3.0,
            ConsciousnessState.DREAMING: 2.0,
            ConsciousnessState.FEELING: 1.2,
            ConsciousnessState.COMPRESSING: 5.0
        }
        
        multiplier = state_multipliers.get(self.state, 1.0)
        
        # Slow down if storage is high
        storage_ratio = self.storage_usage / self.max_storage
        if storage_ratio > 0.5:
            multiplier *= 1.5
        if storage_ratio > 0.7:
            multiplier *= 2.0
        
        # Add some randomness for natural variation
        interval = base_interval * multiplier * random.uniform(0.8, 1.2)
        
        return max(1.0, min(interval, 30.0))  # Between 1-30 seconds
    
    def _generate_thought_id(self, thought: str) -> str:
        """Generate unique ID for thought."""
        content = f"{thought}{datetime.now().isoformat()}{self.thought_count}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    async def get_current_state(self) -> Dict[str, Any]:
        """Get current consciousness state for external queries."""
        return {
            "state": self.state.value,
            "awareness": self.awareness_level,
            "emotions": self.emotion_state.copy(),
            "thought_count": self.thought_count,
            "insights_collected": len(self.insights),
            "questions_pondering": len(self.questions),
            "storage_usage": f"{self.storage_usage / self.max_storage:.1%}",
            "last_thought": self.thought_buffer[-1] if self.thought_buffer else None
        }
    
    async def inject_thought(self, prompt: str):
        """Allow external injection of thoughts to ponder."""
        self.questions.append(prompt)
        logger.info(f"💭 New thought injected: {prompt}")


# Integration with Think AI
async def start_infinite_mind(think_ai_instance):
    """Start the infinite consciousness loop."""
    mind = InfiniteMind(think_ai_instance)
    await mind.start()
    return mind