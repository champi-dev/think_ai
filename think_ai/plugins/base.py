"""Base plugin interface for Think AI."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from enum import Enum
import inspect
import asyncio

from ..consciousness.principles import ConstitutionalAI
from ..utils.logging import get_logger


logger = get_logger(__name__)


class PluginCapability(Enum):
    """Capabilities that plugins can provide."""
    STORAGE_BACKEND = "storage_backend"
    EMBEDDING_MODEL = "embedding_model"
    QUERY_PROCESSOR = "query_processor"
    UI_COMPONENT = "ui_component"
    CONSCIOUSNESS_MODULE = "consciousness_module"
    KNOWLEDGE_FILTER = "knowledge_filter"
    LANGUAGE_MODEL = "language_model"
    ANALYTICS = "analytics"
    EXPORT_FORMAT = "export_format"
    IMPORT_FORMAT = "import_format"


@dataclass
class PluginMetadata:
    """Metadata for a plugin."""
    name: str
    version: str
    author: str
    description: str
    capabilities: List[PluginCapability]
    dependencies: List[str] = field(default_factory=list)
    config_schema: Dict[str, Any] = field(default_factory=dict)
    love_aligned: bool = True
    ethical_review_passed: bool = False
    license: str = "Apache-2.0"
    homepage: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class PluginContext:
    """Context provided to plugins during execution."""
    engine: Any  # ThinkAIEngine instance
    config: Dict[str, Any]
    constitutional_ai: Optional[ConstitutionalAI] = None
    user_context: Dict[str, Any] = field(default_factory=dict)


class Plugin(ABC):
    """Abstract base class for Think AI plugins."""
    
    def __init__(self, metadata: PluginMetadata):
        self.metadata = metadata
        self._initialized = False
        self._context: Optional[PluginContext] = None
        self.hooks: Dict[str, List[callable]] = {}
    
    @abstractmethod
    async def initialize(self, context: PluginContext) -> None:
        """Initialize the plugin with context."""
        self._context = context
        self._initialized = True
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Cleanup plugin resources."""
        self._initialized = False
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check plugin health status."""
        return {
            "status": "healthy" if self._initialized else "not_initialized",
            "plugin": self.metadata.name,
            "version": self.metadata.version
        }
    
    def register_hook(self, event: str, callback: callable) -> None:
        """Register a callback for an event."""
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(callback)
    
    async def emit_event(self, event: str, data: Any = None) -> None:
        """Emit an event to registered callbacks."""
        if event in self.hooks:
            for callback in self.hooks[event]:
                if inspect.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        if self._context:
            return self._context.config.get(key, default)
        return default
    
    async def check_ethical_compliance(self, content: Any) -> bool:
        """Check if content meets ethical standards."""
        if self._context and self._context.constitutional_ai:
            assessment = await self._context.constitutional_ai.evaluate_content(str(content))
            return assessment.passed
        return True  # Pass by default if no AI available


class StoragePlugin(Plugin):
    """Base class for storage backend plugins."""
    
    @abstractmethod
    async def store(self, key: str, value: Any, metadata: Dict[str, Any]) -> bool:
        """Store data."""
        pass
    
    @abstractmethod
    async def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve data."""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete data."""
        pass
    
    @abstractmethod
    async def list_keys(self, prefix: Optional[str] = None, limit: int = 100) -> List[str]:
        """List keys with optional prefix."""
        pass


class EmbeddingPlugin(Plugin):
    """Base class for embedding model plugins."""
    
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text."""
        pass
    
    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        pass


class QueryProcessorPlugin(Plugin):
    """Base class for query processing plugins."""
    
    @abstractmethod
    async def process_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a query and return results."""
        pass
    
    @abstractmethod
    async def enhance_query(self, query: str) -> str:
        """Enhance or expand a query."""
        pass


class UIComponentPlugin(Plugin):
    """Base class for UI component plugins."""
    
    @abstractmethod
    def get_widget(self) -> Any:
        """Get the UI widget/component."""
        pass
    
    @abstractmethod
    async def handle_event(self, event: Dict[str, Any]) -> None:
        """Handle UI events."""
        pass


class ConsciousnessPlugin(Plugin):
    """Base class for consciousness module plugins."""
    
    @abstractmethod
    async def process_consciousness_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process consciousness state."""
        pass
    
    @abstractmethod
    async def enhance_awareness(self, input_data: Any) -> Any:
        """Enhance consciousness awareness."""
        pass


class LoveAlignedPlugin(Plugin):
    """Base class for plugins that must be love-aligned."""
    
    async def initialize(self, context: PluginContext) -> None:
        """Initialize with love alignment check."""
        if not self.metadata.love_aligned:
            raise ValueError(f"Plugin {self.metadata.name} is not love-aligned")
        
        await super().initialize(context)
        
        # Verify ethical compliance
        if context.constitutional_ai:
            test_content = f"Plugin {self.metadata.name} promoting wellbeing"
            if not await self.check_ethical_compliance(test_content):
                raise ValueError(f"Plugin {self.metadata.name} failed ethical compliance")
    
    async def validate_love_metrics(self, action: str) -> bool:
        """Validate that an action aligns with love metrics."""
        love_keywords = ["help", "support", "care", "compassion", "kindness"]
        return any(keyword in action.lower() for keyword in love_keywords)


class PluginError(Exception):
    """Plugin-specific error."""
    pass


class PluginLoadError(PluginError):
    """Error loading a plugin."""
    pass


class PluginExecutionError(PluginError):
    """Error executing plugin functionality."""
    pass


def plugin_event(event_name: str):
    """Decorator to mark methods as event handlers."""
    def decorator(func):
        func._plugin_event = event_name
        return func
    return decorator


def requires_capability(capability: PluginCapability):
    """Decorator to mark methods that require specific capabilities."""
    def decorator(func):
        func._required_capability = capability
        return func
    return decorator


def love_required(func):
    """Decorator to ensure function calls are love-aligned."""
    async def wrapper(self, *args, **kwargs):
        # Check if plugin is love-aligned
        if hasattr(self, 'metadata') and not self.metadata.love_aligned:
            raise PluginError(f"Love-aligned operation called on non-love plugin")
        
        # Execute function
        result = await func(self, *args, **kwargs)
        
        # Validate result if possible
        if hasattr(self, 'validate_love_metrics'):
            if not await self.validate_love_metrics(str(result)):
                logger.warning(f"Operation result may not be love-aligned: {func.__name__}")
        
        return result
    
    return wrapper