"""Cost optimization configuration for Think AI."""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from datetime import datetime

from ..utils.logging import get_logger


logger = get_logger(__name__)


class CostOptimizer:
    """
    Helps users minimize costs while maximizing value.
    
    Designed for users who need to be mindful of API costs
    and computational resources.
    """
    
    def __init__(self, budget_limit: Optional[float] = None):
        self.budget_limit = budget_limit or 10.0  # Default $10/month
        self.current_spending = 0.0
        
        # Cost tracking
        self.cost_log_path = Path.home() / ".think_ai" / "cost_tracking.json"
        self.cost_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing costs
        self.load_cost_history()
        
        # Optimization strategies
        self.strategies = {
            "local_first": {
                "description": "Always try local models before external APIs",
                "savings_potential": 0.8,  # 80% cost reduction
                "enabled": True
            },
            "cache_everything": {
                "description": "Aggressively cache all responses",
                "savings_potential": 0.6,  # 60% cost reduction
                "enabled": True
            },
            "batch_requests": {
                "description": "Batch multiple queries together",
                "savings_potential": 0.3,  # 30% cost reduction
                "enabled": True
            },
            "compress_context": {
                "description": "Compress context to minimum viable",
                "savings_potential": 0.4,  # 40% cost reduction
                "enabled": True
            },
            "off_peak_processing": {
                "description": "Defer non-urgent tasks to off-peak times",
                "savings_potential": 0.2,  # 20% cost reduction
                "enabled": True
            }
        }
    
    def get_free_alternatives(self, task_type: str) -> List[Dict[str, Any]]:
        """Get free alternatives for common tasks."""
        alternatives = {
            "text_generation": [
                {
                    "name": "Local Phi-2",
                    "description": "Microsoft's 2.7B parameter model",
                    "quality": 0.7,
                    "cost": 0.0,
                    "setup": "Already included in Think AI"
                },
                {
                    "name": "Cached Responses",
                    "description": "Use previously generated similar responses",
                    "quality": 0.8,
                    "cost": 0.0,
                    "setup": "Automatic"
                }
            ],
            "embeddings": [
                {
                    "name": "Local Sentence Transformers",
                    "description": "all-MiniLM-L6-v2 runs locally",
                    "quality": 0.85,
                    "cost": 0.0,
                    "setup": "Already included"
                }
            ],
            "claude_conversation": [
                {
                    "name": "Think AI Assistant",
                    "description": "Use Think AI's consciousness system instead",
                    "quality": 0.6,
                    "cost": 0.0,
                    "setup": "Built-in alternative"
                },
                {
                    "name": "Template Responses",
                    "description": "Pre-written responses for common queries",
                    "quality": 0.5,
                    "cost": 0.0,
                    "setup": "Automatic"
                },
                {
                    "name": "Community Models",
                    "description": "Use Hugging Face free inference API",
                    "quality": 0.65,
                    "cost": 0.0,
                    "setup": "Requires HF account (free)"
                }
            ]
        }
        
        return alternatives.get(task_type, [])
    
    def suggest_cost_saving_config(self) -> Dict[str, Any]:
        """Suggest optimal configuration for minimal costs."""
        return {
            "storage": {
                "primary": "sqlite",  # Free, local
                "cache": "in_memory",  # No Redis costs
                "vector_db": "local_faiss"  # No Milvus costs
            },
            "models": {
                "language_model": {
                    "provider": "local",
                    "model": "microsoft/phi-2",
                    "quantization": "int4",  # Smallest size
                    "device": "cpu"  # No GPU costs
                },
                "embeddings": {
                    "provider": "local",
                    "model": "all-MiniLM-L6-v2"
                }
            },
            "features": {
                "claude_integration": "disabled",  # No API costs
                "cloud_sync": "disabled",  # No bandwidth costs
                "federated_learning": "local_only",  # No network costs
                "plugins": "essential_only"  # Minimal resource usage
            },
            "optimization": {
                "max_context_tokens": 512,  # Minimal context
                "cache_ttl_hours": 720,  # 30 days caching
                "batch_size": 10,  # Process in batches
                "compression": "aggressive"
            }
        }
    
    def track_usage(
        self,
        service: str,
        operation: str,
        units: int,
        unit_cost: float
    ) -> Dict[str, Any]:
        """Track usage and costs."""
        cost = units * unit_cost
        self.current_spending += cost
        
        usage_entry = {
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "operation": operation,
            "units": units,
            "unit_cost": unit_cost,
            "total_cost": cost,
            "budget_remaining": self.budget_limit - self.current_spending
        }
        
        # Log to file
        self.save_cost_entry(usage_entry)
        
        # Check budget
        if self.current_spending > self.budget_limit * 0.8:
            logger.warning(f"Approaching budget limit: ${self.current_spending:.2f} of ${self.budget_limit:.2f}")
        
        return usage_entry
    
    def get_cost_breakdown(self) -> Dict[str, Any]:
        """Get detailed cost breakdown."""
        breakdown = {
            "total_spent": self.current_spending,
            "budget_limit": self.budget_limit,
            "budget_used_percentage": (self.current_spending / self.budget_limit * 100) if self.budget_limit > 0 else 0,
            "by_service": {},
            "by_day": {},
            "optimization_savings": 0.0
        }
        
        # Load and analyze cost history
        if self.cost_log_path.exists():
            with open(self.cost_log_path, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    service = entry["service"]
                    
                    if service not in breakdown["by_service"]:
                        breakdown["by_service"][service] = 0.0
                    breakdown["by_service"][service] += entry["total_cost"]
        
        # Calculate savings from optimizations
        for strategy, config in self.strategies.items():
            if config["enabled"]:
                potential_original = self.current_spending / (1 - config["savings_potential"])
                breakdown["optimization_savings"] += potential_original - self.current_spending
        
        return breakdown
    
    def emergency_cost_reduction(self) -> Dict[str, Any]:
        """Emergency measures when approaching budget limit."""
        measures = {
            "immediate_actions": [
                "Switch all operations to local models",
                "Disable external API calls",
                "Use cached responses only",
                "Reduce context to 256 tokens max"
            ],
            "config_changes": {
                "models.language_model.provider": "local",
                "features.claude_integration": "disabled",
                "optimization.max_context_tokens": 256,
                "optimization.cache_only_mode": True
            },
            "estimated_savings": "90-95% cost reduction"
        }
        
        logger.warning("Emergency cost reduction activated!")
        
        return measures
    
    def estimate_operation_cost(
        self,
        operation_type: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, float]:
        """Estimate cost before operation."""
        estimates = {
            "claude_api": {
                "base": 0.01,  # per 1k tokens
                "multiplier": parameters.get("tokens", 1000) / 1000
            },
            "embedding": {
                "base": 0.0001,  # per embedding
                "multiplier": parameters.get("batch_size", 1)
            },
            "storage": {
                "base": 0.00001,  # per operation
                "multiplier": parameters.get("size_kb", 1)
            }
        }
        
        op_estimate = estimates.get(operation_type, {"base": 0, "multiplier": 1})
        estimated_cost = op_estimate["base"] * op_estimate["multiplier"]
        
        # Apply optimization discounts
        for strategy, config in self.strategies.items():
            if config["enabled"]:
                estimated_cost *= (1 - config["savings_potential"] * 0.5)  # Partial savings
        
        return {
            "estimated_cost": estimated_cost,
            "with_optimizations": estimated_cost,
            "without_optimizations": op_estimate["base"] * op_estimate["multiplier"],
            "savings": op_estimate["base"] * op_estimate["multiplier"] - estimated_cost
        }
    
    def save_cost_entry(self, entry: Dict[str, Any]) -> None:
        """Save cost entry to log."""
        with open(self.cost_log_path, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    
    def load_cost_history(self) -> None:
        """Load cost history from log."""
        if self.cost_log_path.exists():
            total = 0.0
            with open(self.cost_log_path, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        total += entry.get("total_cost", 0.0)
                    except:
                        pass
            self.current_spending = total


# Pre-configured profiles for different budget levels
BUDGET_PROFILES = {
    "free_tier": {
        "description": "Completely free - no external costs",
        "budget_limit": 0.0,
        "features": {
            "storage": "local_only",
            "models": "local_only", 
            "api_calls": "disabled",
            "cloud_features": "disabled"
        }
    },
    "minimal": {
        "description": "Under $5/month",
        "budget_limit": 5.0,
        "features": {
            "storage": "local_with_cache",
            "models": "local_preferred",
            "api_calls": "emergency_only",
            "cloud_features": "minimal"
        }
    },
    "balanced": {
        "description": "Under $20/month",
        "budget_limit": 20.0,
        "features": {
            "storage": "hybrid",
            "models": "mixed",
            "api_calls": "optimized",
            "cloud_features": "selective"
        }
    },
    "power_user": {
        "description": "Under $50/month",
        "budget_limit": 50.0,
        "features": {
            "storage": "distributed",
            "models": "best_available",
            "api_calls": "intelligent",
            "cloud_features": "full"
        }
    }
}