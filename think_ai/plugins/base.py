"""Base plugin interface for Think AI."""

import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from think_ai.consciousness.principles import ConstitutionalAI
from think_ai.utils.logging import get_logger

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
    capabilities: list[PluginCapability]
    dependencies: list[str] = field(default_factory=list)
    config_schema: dict[str, Any] = field(default_factory=dict)
    love_aligned: bool = True
    ethical_review_passed: bool = False
    license: str = "Apache-2.0"
    homepage: str | None = None
    tags: list[str] = field(default_factory=list)


@dataclass
class PluginContext:
    """Context provided to plugins during execution."""

    engine: Any  # ThinkAIEngine instance
    config: dict[str, Any]
    constitutional_ai: ConstitutionalAI | None = None
    user_context: dict[str, Any] = field(default_factory=dict)


class Plugin(ABC):
    """Abstract base class for Think AI plugins."""

    def __init__(self, metadata: PluginMetadata) -> None:
        self.metadata = metadata
        self._initialized = False
        self._context: PluginContext | None = None
        self.hooks: dict[str, list[callable]] = {}

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
    async def health_check(self) -> dict[str, Any]:
        """Check plugin health status."""
        return {
            "status": "healthy" if self._initialized else "not_initialized",
            "plugin": self.metadata.name,
            "version": self.metadata.version,
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
            assessment = await self._context.constitutional_ai.evaluate_content(
                str(content)
            )
            return assessment.passed
        return True  # Pass by default if no AI available


class StoragePlugin(Plugin):
    """Base class for storage backend plugins."""

    @abstractmethod
    async def store(self, key: str, value: Any,
                    metadata: dict[str, Any]) -> bool:
        """Store data."""

    @abstractmethod
    async def retrieve(self, key: str) -> Any | None:
        """Retrieve data."""

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete data."""

    @abstractmethod
    async def list_keys(self, prefix: str | None = None,
                        limit: int = 100) -> list[str]:
        """List keys with optional prefix."""


class EmbeddingPlugin(Plugin):
    """Base class for embedding model plugins."""

    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for text."""

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""

    @abstractmethod
    def get_dimension(self) -> int:
        """Get embedding dimension."""


class QueryProcessorPlugin(Plugin):
    """Base class for query processing plugins."""

    @abstractmethod
    async def process_query(
        self, query: str, context: dict[str, Any]
    ) -> dict[str, Any]:
        """Process a query and return results."""

    @abstractmethod
    async def enhance_query(self, query: str) -> str:
        """Enhance or expand a query."""


class UIComponentPlugin(Plugin):
    """Base class for UI component plugins."""

    @abstractmethod
    def get_widget(self) -> Any:
        """Get the UI widget/component."""

    @abstractmethod
    async def handle_event(self, event: dict[str, Any]) -> None:
        """Handle UI events."""


class ConsciousnessPlugin(Plugin):
    """Base class for consciousness module plugins."""

    @abstractmethod
    async def process_consciousness_state(
        self, state: dict[str, Any]
    ) -> dict[str, Any]:
        """Process consciousness state."""

    @abstractmethod
    async def enhance_awareness(self, input_data: Any) -> Any:
        """Enhance consciousness awareness."""


class LoveAlignedPlugin(Plugin):
    """Base class for plugins that must be love-aligned."""

    async def initialize(self, context: PluginContext) -> None:
        """Initialize with love alignment check."""
        if not self.metadata.love_aligned:
            msg = f"Plugin {self.metadata.name} is not love-aligned"
            raise ValueError(msg)

        await super().initialize(context)

        # Verify ethical compliance
        if context.constitutional_ai:
            test_content = f"Plugin {self.metadata.name} promoting wellbeing"
            if not await self.check_ethical_compliance(test_content):
                msg = f"Plugin {self.metadata.name} failed ethical compliance"
                raise ValueError(msg)

    async def validate_love_metrics(self, action: str) -> bool:
        """Validate that an action aligns with love metrics."""
        love_keywords = ["help", "support", "care", "compassion", "kindness"]
        return any(keyword in action.lower() for keyword in love_keywords)


class PluginError(Exception):
    """Plugin-specific error."""


class PluginLoadError(PluginError):
    """Error loading a plugin."""


class PluginExecutionError(PluginError):
    """Error executing plugin functionality."""


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
        if hasattr(self, "metadata") and not self.metadata.love_aligned:
            msg = "Love-aligned operation called on non-love plugin"
            raise PluginError(msg)

        # Execute function
        result = await func(self, *args, **kwargs)

        # Validate result if possible
        if hasattr(self, "validate_love_metrics"):
            if not await self.validate_love_metrics(str(result)):
                logger.warning(
                    f"Operation result may not be love-aligned: {func.__name__}"
                )

        return result

    return wrapper
