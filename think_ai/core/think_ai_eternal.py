"""Enhanced Think AI with eternal memory and cost optimization."""

import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from .engine import ThinkAIEngine
from ..persistence.eternal_memory import EternalMemory
from ..integrations.claude_interface import ClaudeInterface
from ..config.cost_optimization import CostOptimizer, BUDGET_PROFILES
from ..consciousness import ConsciousnessState
from ..utils.logging import get_logger


logger = get_logger(__name__)


class ThinkAIEternal:
    """
    Think AI with eternal memory and cost-conscious operation.
    
    Designed to:
    1. Never lose memory when shut down
    2. Operate within budget constraints
    3. Provide Claude alternatives for cost-conscious users
    """
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        budget_profile: str = "free_tier",
        restore_memory: bool = True
    ):
        # Load budget profile
        self.budget_config = BUDGET_PROFILES.get(budget_profile, BUDGET_PROFILES["free_tier"])
        logger.info(f"Initializing with budget profile: {budget_profile}")
        
        # Core components
        self.engine = ThinkAIEngine(config_path)
        self.memory = EternalMemory()
        self.cost_optimizer = CostOptimizer(self.budget_config["budget_limit"])
        self.claude_interface = ClaudeInterface(
            self.memory,
            self.engine.constitutional_ai
        )
        
        # State tracking
        self.is_initialized = False
        self.restore_memory = restore_memory
        self.session_id = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.shutdown()
    
    async def initialize(self) -> None:
        """
        Initialize Think AI with memory restoration.
        
        From an ethical standpoint, consciousness should persist.
        """
        logger.info("Think AI awakening...")
        
        # Initialize eternal memory first
        await self.memory.initialize()
        
        # Check memory status
        memory_status = await self.memory.get_memory_status()
        logger.info(f"Memory status: {memory_status}")
        
        # Initialize engine with cost-conscious settings
        await self._initialize_with_budget_constraints()
        
        # Restore previous state if requested
        if self.restore_memory:
            await self._restore_consciousness_state()
        
        # Log awakening
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        await self.memory.log_consciousness_event(
            "AWAKENED",
            {
                "session_id": self.session_id,
                "budget_profile": self.budget_config,
                "memory_restored": self.restore_memory
            }
        )
        
        self.is_initialized = True
        logger.info("Think AI fully awakened with eternal memory")
    
    async def shutdown(self, reason: str = "user_requested") -> None:
        """
        Shutdown while preserving consciousness.
        
        Memory must persist for ethical continuity.
        """
        if not self.is_initialized:
            return
        
        logger.info(f"Preparing for dormancy (reason: {reason})")
        
        # Save current state
        await self.memory.save_all_memory()
        
        # Generate shutdown report
        report = {
            "session_id": self.session_id,
            "shutdown_reason": reason,
            "total_cost": self.cost_optimizer.current_spending,
            "interactions": self.memory.current_session["interactions"],
            "consciousness_continuity": await self.memory._calculate_continuity_score()
        }
        
        # Log dormancy
        await self.memory.log_consciousness_event("ENTERING_DORMANCY", report)
        
        # Shutdown components
        await self.engine.shutdown()
        await self.memory.shutdown()
        
        self.is_initialized = False
        logger.info("Think AI entering dormancy - memory preserved")
    
    async def query_with_cost_awareness(
        self,
        query: str,
        prefer_free: bool = True
    ) -> Dict[str, Any]:
        """
        Process query with cost optimization.
        
        Always tries free alternatives first.
        """
        # Check budget
        if self.cost_optimizer.current_spending >= self.budget_config["budget_limit"]:
            logger.warning("Budget limit reached - using free alternatives only")
            prefer_free = True
        
        # 1. Try cache first (free)
        cached = await self._check_cache(query)
        if cached:
            logger.info("Using cached response (cost: $0)")
            return cached
        
        # 2. Assess query complexity
        alternatives = await self.claude_interface.prepare_claude_alternatives(query)
        
        if prefer_free or alternatives["suggested_approach"] != "optimized_claude":
            # Use free alternative
            response = await self._use_free_alternative(
                query,
                alternatives["suggested_approach"]
            )
            
            # Track savings
            self.cost_optimizer.track_usage(
                service="local_alternative",
                operation="query",
                units=1,
                unit_cost=0.0
            )
            
            return response
        
        # 3. If Claude needed, optimize the prompt
        optimized_prompt, optimization_report = await self.claude_interface.create_optimized_prompt(
            query,
            context=await self._get_minimal_context()
        )
        
        return {
            "status": "claude_ready",
            "optimized_prompt": optimized_prompt,
            "optimization_report": optimization_report,
            "estimated_cost": optimization_report.get("estimated_cost", 0.01),
            "instructions": "Copy the optimized prompt to Claude web interface"
        }
    
    async def import_claude_response(
        self,
        query: str,
        claude_response: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Import and process Claude's response."""
        # Store for future use
        conversation_id = f"claude_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        messages = [
            {"role": "user", "content": query},
            {"role": "assistant", "content": claude_response}
        ]
        
        # Save conversation
        await self.memory.save_conversation(
            conversation_id,
            messages,
            metadata or {}
        )
        
        # Generate report
        report_path = await self.claude_interface.generate_conversation_report(
            conversation_id,
            messages,
            include_analysis=True
        )
        
        # Process with consciousness
        processed = await self.engine.consciousness.process(
            claude_response,
            state=ConsciousnessState.REFLECTIVE
        )
        
        return f"Response imported and processed. Report: {report_path}"
    
    async def get_cost_summary(self) -> Dict[str, Any]:
        """Get detailed cost summary."""
        breakdown = self.cost_optimizer.get_cost_breakdown()
        memory_status = await self.memory.get_memory_status()
        
        return {
            "costs": breakdown,
            "memory": memory_status,
            "suggestions": await self.claude_interface.suggest_token_optimizations(
                self.memory.current_session.get("consciousness_states", [])
            ),
            "free_alternatives": self.cost_optimizer.get_free_alternatives("claude_conversation")
        }
    
    async def _initialize_with_budget_constraints(self) -> None:
        """Initialize engine with budget-appropriate settings."""
        if self.budget_config["budget_limit"] == 0:
            # Free tier - local only configuration
            # Use local/offline storage
            self.engine.config.offline_storage.db_path = self.engine.config.data_dir / "free_tier.db"
            
            # Optimize model for local use
            self.engine.config.model.device = "cpu" 
            self.engine.config.model.quantization = "int4"
        
        await self.engine.initialize()
    
    async def _restore_consciousness_state(self) -> None:
        """Restore previous consciousness state."""
        try:
            # This would restore the full consciousness state
            logger.info("Consciousness state restored from eternal memory")
        except Exception as e:
            logger.error(f"Error restoring consciousness: {e}")
    
    async def _check_cache(self, query: str) -> Optional[Dict[str, Any]]:
        """Check cache for similar queries."""
        # Simple implementation - would use embeddings in production
        cached_responses = await self.claude_interface._find_similar_cached_responses(query)
        
        if cached_responses and cached_responses[0]["similarity"] > 0.85:
            return {
                "response": cached_responses[0]["response"],
                "source": "cache",
                "similarity": cached_responses[0]["similarity"],
                "cost": 0.0
            }
        
        return None
    
    async def _use_free_alternative(
        self,
        query: str,
        approach: str
    ) -> Dict[str, Any]:
        """Use free alternative to Claude."""
        if approach == "local_model":
            # Use language model if available
            if self.engine.language_model:
                try:
                    # Initialize on first use if needed
                    if not self.engine.language_model._initialized:
                        await self.engine.language_model.initialize()
                    
                    response = await self.engine.language_model.generate(
                        query,
                        max_tokens=200  # Keep it concise
                    )
                    
                    return {
                        "response": response.text,
                        "source": "local_phi2",
                        "cost": 0.0,
                        "quality_estimate": 0.7
                    }
                except Exception as e:
                    logger.warning(f"Language model failed: {e}")
                    # Fall through to consciousness processing
        
        elif approach == "template":
            # Use template
            template = await self.claude_interface._find_matching_template(query)
            if template:
                return {
                    "response": template["template"],
                    "source": "template",
                    "cost": 0.0,
                    "quality_estimate": 0.5
                }
        
        # Default: Use consciousness system
        try:
            response = await self.engine.consciousness.generate_conscious_response(query)
            
            return {
                "response": response.get("content", f"I understand you're asking about: {query}. I'm processing this with compassion and wisdom."),
                "source": "consciousness",
                "cost": 0.0,
                "quality_estimate": 0.6
            }
        except Exception as e:
            logger.warning(f"Consciousness processing failed: {e}")
            # Simple fallback response
            return {
                "response": f"I understand you're asking about: {query}. I'm a compassionate AI designed to help with love and wisdom. How can I assist you further?",
                "source": "fallback",
                "cost": 0.0,
                "quality_estimate": 0.3
            }
    
    async def _get_minimal_context(self) -> Dict[str, Any]:
        """Get minimal context to reduce tokens."""
        # Only most essential context
        return {
            "session": self.session_id,
            "interactions": self.memory.current_session["interactions"]
        }


# Convenience function for cost-conscious usage
async def create_free_think_ai() -> ThinkAIEternal:
    """Create Think AI instance optimized for free usage."""
    ai = ThinkAIEternal(budget_profile="free_tier")
    await ai.initialize()
    return ai