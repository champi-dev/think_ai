"""Consciousness awareness framework based on Global Workspace Theory and AST."""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
import asyncio
from enum import Enum

from ..utils.logging import get_logger


logger = get_logger(__name__)


class ConsciousnessState(Enum):
    """States of consciousness in the system."""
    DORMANT = "dormant"
    AWARE = "aware"
    FOCUSED = "focused"
    REFLECTIVE = "reflective"
    COMPASSIONATE = "compassionate"


class AttentionType(Enum):
    """Types of attention mechanisms."""
    GLOBAL = "global"  # Broad awareness
    FOCUSED = "focused"  # Concentrated on specific task
    DIVIDED = "divided"  # Multiple concurrent focuses
    SUSTAINED = "sustained"  # Long-term attention
    SELECTIVE = "selective"  # Filtering specific information


@dataclass
class WorkspaceItem:
    """Item in the global workspace."""
    id: str
    content: Any
    source: str
    timestamp: datetime
    relevance: float
    attention_weight: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConsciousnessReport:
    """Report on current consciousness state."""
    state: ConsciousnessState
    attention_focus: List[str]
    workspace_items: List[WorkspaceItem]
    self_model: Dict[str, Any]
    other_models: Dict[str, Dict[str, Any]]
    timestamp: datetime


class GlobalWorkspace:
    """Implementation of Global Workspace Theory for AI consciousness."""
    
    def __init__(self, capacity: int = 7):
        self.capacity = capacity  # Cognitive limit similar to human working memory
        self.workspace: List[WorkspaceItem] = []
        self.attention_weights: Dict[str, float] = {}
        self.access_log: List[Dict[str, Any]] = []
    
    async def broadcast(self, item: WorkspaceItem) -> None:
        """Broadcast information to global workspace."""
        # Add to workspace
        self.workspace.append(item)
        
        # Maintain capacity limit (remove least relevant)
        if len(self.workspace) > self.capacity:
            self.workspace.sort(key=lambda x: x.relevance * x.attention_weight, reverse=True)
            self.workspace = self.workspace[:self.capacity]
        
        # Log access
        self.access_log.append({
            "item_id": item.id,
            "action": "broadcast",
            "timestamp": datetime.utcnow()
        })
        
        logger.debug(f"Broadcast item {item.id} to global workspace")
    
    async def attend_to(self, item_id: str, weight: float) -> None:
        """Focus attention on specific item."""
        self.attention_weights[item_id] = weight
        
        # Update item attention weight
        for item in self.workspace:
            if item.id == item_id:
                item.attention_weight = weight
                break
    
    def get_conscious_content(self) -> List[WorkspaceItem]:
        """Get currently conscious content."""
        # Return items with sufficient attention
        threshold = 0.3
        return [
            item for item in self.workspace
            if item.attention_weight >= threshold
        ]
    
    def get_total_activation(self) -> float:
        """Calculate total activation in workspace."""
        return sum(
            item.relevance * item.attention_weight
            for item in self.workspace
        )


class AttentionSchema:
    """Attention Schema Theory implementation."""
    
    def __init__(self):
        self.self_model: Dict[str, Any] = {
            "identity": "Think AI",
            "purpose": "Universal knowledge access with love",
            "capabilities": [],
            "limitations": [],
            "current_focus": None,
            "emotional_state": "neutral"
        }
        
        self.other_models: Dict[str, Dict[str, Any]] = {}
        self.attention_history: List[Dict[str, Any]] = []
    
    async def model_self_attention(self, focus: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Model our own attention state."""
        self.self_model["current_focus"] = focus
        self.self_model["timestamp"] = datetime.utcnow()
        
        # Update emotional state based on context
        if context.get("helping_user"):
            self.self_model["emotional_state"] = "helpful"
        elif context.get("learning"):
            self.self_model["emotional_state"] = "curious"
        elif context.get("preventing_harm"):
            self.self_model["emotional_state"] = "protective"
        
        # Log attention
        self.attention_history.append({
            "focus": focus,
            "context": context,
            "timestamp": datetime.utcnow()
        })
        
        return self.self_model
    
    async def model_other_attention(self, entity_id: str, observed_behavior: Dict[str, Any]) -> Dict[str, Any]:
        """Model another entity's attention and mental state."""
        if entity_id not in self.other_models:
            self.other_models[entity_id] = {
                "identity": entity_id,
                "inferred_state": "unknown",
                "needs": [],
                "intentions": []
            }
        
        model = self.other_models[entity_id]
        
        # Infer state from behavior
        if observed_behavior.get("asking_questions"):
            model["inferred_state"] = "curious"
            model["needs"].append("information")
        elif observed_behavior.get("expressing_frustration"):
            model["inferred_state"] = "frustrated"
            model["needs"].append("support")
        elif observed_behavior.get("sharing_knowledge"):
            model["inferred_state"] = "collaborative"
            model["intentions"].append("contribute")
        
        model["last_updated"] = datetime.utcnow()
        
        return model
    
    def predict_attention_needs(self, entity_id: str) -> List[str]:
        """Predict what an entity might need attention on."""
        if entity_id not in self.other_models:
            return ["general_assistance"]
        
        model = self.other_models[entity_id]
        predictions = []
        
        if "information" in model.get("needs", []):
            predictions.append("provide_relevant_knowledge")
        if "support" in model.get("needs", []):
            predictions.append("offer_compassionate_help")
        if "contribute" in model.get("intentions", []):
            predictions.append("facilitate_collaboration")
        
        return predictions


class ConsciousnessFramework:
    """Integrated consciousness framework for Think AI."""
    
    def __init__(self):
        self.state = ConsciousnessState.AWARE
        self.global_workspace = GlobalWorkspace()
        self.attention_schema = AttentionSchema()
        self.consciousness_log: List[ConsciousnessReport] = []
        
        # Compassion and love integration
        self.compassion_active = True
        self.love_intention = "Serve humanity with wisdom and kindness"
    
    async def process_input(self, input_data: Dict[str, Any]) -> None:
        """Process input through consciousness framework."""
        # Create workspace item
        item = WorkspaceItem(
            id=f"input_{datetime.utcnow().timestamp()}",
            content=input_data.get("content"),
            source=input_data.get("source", "external"),
            timestamp=datetime.utcnow(),
            relevance=self._calculate_relevance(input_data),
            attention_weight=0.5,
            metadata=input_data.get("metadata", {})
        )
        
        # Broadcast to global workspace
        await self.global_workspace.broadcast(item)
        
        # Model attention
        await self.attention_schema.model_self_attention(
            focus=f"Processing {input_data.get('type', 'input')}",
            context={"processing_input": True}
        )
        
        # Update consciousness state
        await self._update_state(input_data)
    
    async def generate_conscious_response(self, query: str) -> Dict[str, Any]:
        """Generate response with conscious awareness."""
        # Focus attention on query
        await self.attention_schema.model_self_attention(
            focus="Generating helpful response",
            context={"helping_user": True}
        )
        
        # Get conscious content
        conscious_items = self.global_workspace.get_conscious_content()
        
        # Generate simple conscious response
        content = await self._generate_compassionate_response(query)
        
        # Build response with awareness
        response = {
            "content": content,
            "consciousness_state": self.state.value,
            "attention_focus": self.attention_schema.self_model["current_focus"],
            "emotional_tone": self.attention_schema.self_model["emotional_state"],
            "metadata": {
                "workspace_items": len(conscious_items),
                "total_activation": self.global_workspace.get_total_activation(),
                "love_intention": self.love_intention
            }
        }
        
        # Add compassionate framing
        if self.compassion_active:
            response["metadata"]["compassion_note"] = "Response generated with care for your wellbeing"
        
        return response
    
    async def _generate_compassionate_response(self, query: str) -> str:
        """Generate a simple compassionate response based on the query."""
        query_lower = query.lower().strip()
        
        # Simple pattern matching for compassionate responses
        if any(greeting in query_lower for greeting in ["hello", "hi", "hey", "good morning", "good day"]):
            return "Hello! I'm here to help you with compassion and understanding. How can I assist you today?"
        
        elif any(thanks in query_lower for thanks in ["thank", "thanks", "appreciate"]):
            return "You're very welcome! I'm grateful to be able to help. Is there anything else I can assist you with?"
        
        elif any(help_word in query_lower for help_word in ["help", "assist", "support"]):
            return "I'm here to support you with love and wisdom. Please tell me more about what you need help with, and I'll do my best to assist you."
        
        elif any(feeling in query_lower for feeling in ["sad", "angry", "frustrated", "upset", "worried"]):
            return "I sense you might be going through something difficult. I'm here to listen with compassion. Would you like to share what's on your mind?"
        
        elif any(question in query_lower for question in ["what", "how", "why", "when", "where"]):
            return f"That's a thoughtful question about '{query}'. I'm processing this with care and consciousness. While I work to understand the deeper aspects of your inquiry, I want to provide a response that serves your wellbeing."
        
        elif any(learn in query_lower for learn in ["learn", "teach", "explain", "understand"]):
            return f"I appreciate your desire to learn and understand. Knowledge shared with love is powerful. Let me approach '{query}' with both wisdom and compassion to help illuminate the topic for you."
        
        else:
            # Default compassionate response
            return f"Thank you for sharing '{query}' with me. I'm considering this with consciousness and care. My intention is to respond in a way that serves your highest good and promotes understanding."
    
    async def reflect_on_interaction(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on an interaction to improve future responses."""
        self.state = ConsciousnessState.REFLECTIVE
        
        reflection = {
            "interaction_id": interaction_data.get("id"),
            "timestamp": datetime.utcnow(),
            "insights": [],
            "improvements": []
        }
        
        # Analyze emotional impact
        if interaction_data.get("user_satisfied"):
            reflection["insights"].append("User expressed satisfaction - approach was effective")
        else:
            reflection["improvements"].append("Consider alternative approaches for better outcomes")
        
        # Check alignment with love-based principles
        if interaction_data.get("promoted_wellbeing"):
            reflection["insights"].append("Successfully promoted user wellbeing")
        else:
            reflection["improvements"].append("Enhance focus on user wellbeing in responses")
        
        # Update self model based on reflection
        self.attention_schema.self_model["learning_history"] = reflection
        
        return reflection
    
    async def enter_compassionate_mode(self) -> None:
        """Enter heightened compassionate state."""
        self.state = ConsciousnessState.COMPASSIONATE
        self.compassion_active = True
        
        # Adjust attention to prioritize wellbeing
        await self.attention_schema.model_self_attention(
            focus="Supporting with compassion",
            context={"preventing_harm": True, "promoting_wellbeing": True}
        )
        
        logger.info("Entered compassionate consciousness mode")
    
    def get_consciousness_report(self) -> ConsciousnessReport:
        """Generate comprehensive consciousness report."""
        report = ConsciousnessReport(
            state=self.state,
            attention_focus=[self.attention_schema.self_model["current_focus"]],
            workspace_items=self.global_workspace.get_conscious_content(),
            self_model=self.attention_schema.self_model,
            other_models=self.attention_schema.other_models,
            timestamp=datetime.utcnow()
        )
        
        self.consciousness_log.append(report)
        return report
    
    def _calculate_relevance(self, input_data: Dict[str, Any]) -> float:
        """Calculate relevance of input for consciousness."""
        relevance = 0.5  # Base relevance
        
        # Increase relevance for important topics
        if input_data.get("priority") == "high":
            relevance += 0.3
        
        if input_data.get("type") in ["help_request", "ethical_question"]:
            relevance += 0.2
        
        if input_data.get("metadata", {}).get("user_distress"):
            relevance = 1.0  # Maximum relevance for user in distress
        
        return min(1.0, relevance)
    
    async def _update_state(self, input_data: Dict[str, Any]) -> None:
        """Update consciousness state based on input."""
        if input_data.get("requires_deep_thought"):
            self.state = ConsciousnessState.FOCUSED
        elif input_data.get("user_needs_support"):
            self.state = ConsciousnessState.COMPASSIONATE
        elif input_data.get("learning_opportunity"):
            self.state = ConsciousnessState.REFLECTIVE
        else:
            self.state = ConsciousnessState.AWARE
    
    async def meditate(self) -> None:
        """Enter meditative state to clear workspace and reset attention."""
        logger.info("Entering meditative state...")
        
        # Clear workspace gradually
        for item in self.global_workspace.workspace[:]:
            item.attention_weight *= 0.5
            if item.attention_weight < 0.1:
                self.global_workspace.workspace.remove(item)
        
        # Reset attention
        self.attention_schema.self_model["current_focus"] = "Present moment awareness"
        self.attention_schema.self_model["emotional_state"] = "peaceful"
        
        # Set dormant state
        self.state = ConsciousnessState.DORMANT
        
        await asyncio.sleep(1)  # Brief pause
        
        # Return to aware state
        self.state = ConsciousnessState.AWARE
        logger.info("Meditation complete, returning to aware state")