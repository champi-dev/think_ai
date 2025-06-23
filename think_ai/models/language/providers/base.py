"""Base interface for language model providers."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator
from dataclasses import dataclass

from think_ai.models.language.types import GenerationConfig, ModelResponse


@dataclass
class ModelInfo:
    """Information about a model."""
    
    name: str
    provider: str
    size: Optional[str] = None
    quantization: Optional[str] = None
    context_length: int = 4096
    capabilities: List[str] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []


class ModelProvider(ABC):
    """Abstract base class for model providers."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the provider with configuration."""
        self.config = config
        self._models_cache: Optional[List[ModelInfo]] = None
    
    @abstractmethod
    async def list_models(self) -> List[ModelInfo]:
        """List available models from this provider."""
        pass
    
    @abstractmethod
    async def generate(
        self,
        model: str,
        prompt: str,
        config: GenerationConfig,
        system_prompt: Optional[str] = None
    ) -> ModelResponse:
        """Generate a response from the model."""
        pass
    
    @abstractmethod
    async def stream_generate(
        self,
        model: str,
        prompt: str,
        config: GenerationConfig,
        system_prompt: Optional[str] = None
    ) -> AsyncIterator[str]:
        """Stream generation from the model."""
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the provider is available and operational."""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of this provider."""
        pass
    
    async def load_model(self, model: str) -> None:
        """Pre-load a model if the provider supports it."""
        # Default implementation does nothing
        # Providers can override if they support pre-loading
        pass
    
    async def unload_model(self, model: str) -> None:
        """Unload a model if the provider supports it."""
        # Default implementation does nothing
        # Providers can override if they support unloading
        pass