"""Model manager for handling multiple providers and task-specific model selection."""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import asyncio
from enum import Enum

from .providers.base import ModelProvider, ModelInfo
from .providers.ollama import OllamaProvider  
from .providers.huggingface import HuggingFaceProvider
from think_ai.models.language.types import GenerationConfig, ModelResponse
from think_ai.utils.logger import get_logger

logger = get_logger(__name__)


class TaskType(Enum):
    """Types of tasks for model selection."""
    CHAT = "chat"
    CODING = "coding"
    MATH = "math"
    MULTIMODAL = "multimodal"
    REASONING = "reasoning"
    FAST_RESPONSE = "fast"
    

@dataclass
class ModelSelection:
    """Selected model and provider for a task."""
    provider: str
    model: str
    reason: str


class ModelManager:
    """Manages multiple model providers and selects appropriate models for tasks."""
    
    # Task-specific model preferences (provider -> model)
    TASK_MODELS = {
        TaskType.CHAT: {
            "ollama": ["qwen2.5:0.5b", "qwen2.5:1.5b", "qwen2.5:3b"],
            "huggingface": ["Qwen/Qwen2.5-1.5B-Instruct", "Qwen/Qwen2.5-3B-Instruct"]
        },
        TaskType.CODING: {
            "ollama": ["qwen2.5-coder:1.5b", "qwen2.5-coder:7b", "qwen2.5-coder:32b"],
            "huggingface": ["Qwen/Qwen2.5-Coder-1.5B-Instruct"]
        },
        TaskType.MATH: {
            "ollama": ["qwen2.5-math:1.5b", "qwen2.5-math:7b"],
            "huggingface": ["Qwen/Qwen2.5-Math-1.5B-Instruct"]
        },
        TaskType.MULTIMODAL: {
            "ollama": ["qwenvl2:2b", "qwenvl2:7b"],
            "huggingface": []  # Not supported in HF provider yet
        },
        TaskType.REASONING: {
            "ollama": ["qwen2.5:7b", "qwen2.5:14b", "qwen2.5:32b"],
            "huggingface": ["Qwen/Qwen2.5-7B-Instruct"]
        },
        TaskType.FAST_RESPONSE: {
            "ollama": ["qwen2.5:0.5b", "qwen2.5:1.5b"],
            "huggingface": ["Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2.5-1.5B-Instruct"]
        }
    }
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize model manager.
        
        Args:
            config: Configuration with provider settings
        """
        self.config = config
        self.providers: Dict[str, ModelProvider] = {}
        self._available_models: Dict[str, List[ModelInfo]] = {}
        self._initialized = False
        
        # Default provider preference order
        self.provider_preference = config.get('provider_preference', ['ollama', 'huggingface'])
    
    async def initialize(self) -> None:
        """Initialize all configured providers."""
        if self._initialized:
            return
            
        # Initialize Ollama provider if configured
        if self.config.get('ollama', {}).get('enabled', True):
            ollama_config = self.config.get('ollama', {})
            self.providers['ollama'] = OllamaProvider(ollama_config)
        
        # Initialize HuggingFace provider if configured
        if self.config.get('huggingface', {}).get('enabled', True):
            hf_config = self.config.get('huggingface', {})
            self.providers['huggingface'] = HuggingFaceProvider(hf_config)
        
        # Check provider availability and list models
        await self._refresh_available_models()
        
        self._initialized = True
        logger.info(f"Initialized {len(self.providers)} model providers")
    
    async def _refresh_available_models(self) -> None:
        """Refresh the list of available models from all providers."""
        for provider_name, provider in self.providers.items():
            try:
                if await provider.is_available():
                    models = await provider.list_models()
                    self._available_models[provider_name] = models
                    logger.info(f"{provider_name}: {len(models)} models available")
                else:
                    self._available_models[provider_name] = []
                    logger.warning(f"{provider_name}: Provider not available")
            except Exception as e:
                self._available_models[provider_name] = []
                logger.error(f"Error checking {provider_name}: {e}")
    
    def select_model_for_task(
        self, 
        task_type: TaskType,
        prefer_fast: bool = False,
        prefer_quality: bool = False
    ) -> Optional[ModelSelection]:
        """Select the best available model for a task.
        
        Args:
            task_type: Type of task to perform
            prefer_fast: Prefer faster/smaller models
            prefer_quality: Prefer higher quality/larger models
            
        Returns:
            Selected model and provider, or None if no suitable model found
        """
        task_models = self.TASK_MODELS.get(task_type, {})
        
        # Try providers in preference order
        for provider_name in self.provider_preference:
            if provider_name not in self._available_models:
                continue
                
            available = self._available_models[provider_name]
            if not available:
                continue
                
            preferred_models = task_models.get(provider_name, [])
            if not preferred_models:
                continue
            
            # Find first available preferred model
            for model_name in preferred_models:
                # Check if model is available
                for model_info in available:
                    if model_info.name == model_name or model_info.name.startswith(model_name):
                        # Apply size preferences
                        if prefer_fast and '7b' not in model_name.lower() and '14b' not in model_name.lower() and '32b' not in model_name.lower():
                            return ModelSelection(
                                provider=provider_name,
                                model=model_info.name,
                                reason=f"Fast {task_type.value} model"
                            )
                        elif prefer_quality and ('7b' in model_name.lower() or '14b' in model_name.lower() or '32b' in model_name.lower()):
                            return ModelSelection(
                                provider=provider_name,
                                model=model_info.name,
                                reason=f"High-quality {task_type.value} model"
                            )
                        elif not prefer_fast and not prefer_quality:
                            return ModelSelection(
                                provider=provider_name,
                                model=model_info.name,
                                reason=f"Balanced {task_type.value} model"
                            )
        
        # Fallback: return any available model with matching capability
        for provider_name in self.provider_preference:
            if provider_name not in self._available_models:
                continue
                
            for model_info in self._available_models[provider_name]:
                if task_type.value in model_info.capabilities:
                    return ModelSelection(
                        provider=provider_name,
                        model=model_info.name,
                        reason=f"Fallback {task_type.value} model"
                    )
        
        return None
    
    async def generate(
        self,
        task_type: TaskType,
        prompt: str,
        config: Optional[GenerationConfig] = None,
        system_prompt: Optional[str] = None,
        prefer_fast: bool = False,
        prefer_quality: bool = False
    ) -> Tuple[ModelResponse, ModelSelection]:
        """Generate response using appropriate model for task.
        
        Returns:
            Tuple of (response, model_selection)
        """
        if not self._initialized:
            await self.initialize()
        
        # Select model
        selection = self.select_model_for_task(task_type, prefer_fast, prefer_quality)
        if not selection:
            raise ValueError(f"No suitable model found for task {task_type.value}")
        
        # Get provider
        provider = self.providers.get(selection.provider)
        if not provider:
            raise ValueError(f"Provider {selection.provider} not available")
        
        # Use default config if not provided
        if config is None:
            config = GenerationConfig()
        
        # Generate response
        logger.info(f"Using {selection.model} ({selection.reason}) for {task_type.value}")
        response = await provider.generate(
            selection.model,
            prompt,
            config,
            system_prompt
        )
        
        return response, selection
    
    async def list_all_models(self) -> Dict[str, List[ModelInfo]]:
        """List all available models from all providers."""
        if not self._initialized:
            await self.initialize()
        
        await self._refresh_available_models()
        return self._available_models
    
    async def close(self) -> None:
        """Close all providers."""
        for provider in self.providers.values():
            if hasattr(provider, '__aexit__'):
                await provider.__aexit__(None, None, None)