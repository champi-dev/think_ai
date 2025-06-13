# Think AI Plugin Development Guide

## Overview

Think AI's plugin architecture allows developers to extend the system's capabilities while maintaining ethical standards and love-based design principles. This guide covers everything you need to know to create, test, and distribute plugins.

## Core Concepts

### Love-Aligned Design

All Think AI plugins must be "love-aligned," meaning they:
- Promote wellbeing and compassion
- Avoid harm in all forms
- Enhance human understanding and connection
- Respect privacy and autonomy
- Support the common good

### Plugin Capabilities

Plugins can provide various capabilities:
- **Storage Backend**: Alternative storage engines
- **Embedding Model**: Custom embedding generation
- **Query Processor**: Enhanced query processing
- **UI Component**: Terminal UI widgets
- **Consciousness Module**: Consciousness enhancements
- **Language Model**: Alternative language models
- **Analytics**: Usage tracking and insights
- **Import/Export**: Data format converters

## Getting Started

### Basic Plugin Structure

```python
from think_ai.plugins.base import Plugin, PluginMetadata, PluginCapability

class MyPlugin(Plugin):
    """Description of your plugin."""
    
    METADATA = PluginMetadata(
        name="my_plugin",
        version="1.0.0",
        author="Your Name",
        description="What your plugin does",
        capabilities=[PluginCapability.STORAGE_BACKEND],
        dependencies=["aiofiles"],
        love_aligned=True,
        ethical_review_passed=False,  # Set to True after review
        tags=["storage", "example"]
    )
    
    def __init__(self, metadata=None):
        super().__init__(metadata or self.METADATA)
    
    async def initialize(self, context):
        """Initialize your plugin."""
        await super().initialize(context)
        # Your initialization code
    
    async def shutdown(self):
        """Clean up resources."""
        # Your cleanup code
        await super().shutdown()
    
    async def health_check(self):
        """Check plugin health."""
        health = await super().health_check()
        # Add your health checks
        return health
```

### Plugin Types

#### Storage Plugin

```python
from think_ai.plugins.base import StoragePlugin

class CustomStoragePlugin(StoragePlugin):
    async def store(self, key, value, metadata):
        """Store data."""
        # Implement storage logic
        return True
    
    async def retrieve(self, key):
        """Retrieve data."""
        # Implement retrieval logic
        return value
    
    async def delete(self, key):
        """Delete data."""
        # Implement deletion logic
        return True
    
    async def list_keys(self, prefix=None, limit=100):
        """List keys."""
        # Implement listing logic
        return keys
```

#### UI Component Plugin

```python
from think_ai.plugins.base import UIComponentPlugin
from textual.containers import Container

class CustomUIPlugin(UIComponentPlugin):
    def get_widget(self):
        """Return Textual widget."""
        return MyCustomWidget()
    
    async def handle_event(self, event):
        """Handle UI events."""
        if event["type"] == "click":
            # Handle click
            pass
```

#### Analytics Plugin

```python
from think_ai.plugins.base import Plugin, plugin_event

class AnalyticsPlugin(Plugin):
    @plugin_event("knowledge_stored")
    async def track_storage(self, data):
        """Track storage events."""
        # Log metrics
        pass
    
    @plugin_event("query_executed")
    async def track_query(self, data):
        """Track queries."""
        # Analyze query patterns
        pass
```

## Event System

### Registering Event Handlers

```python
async def initialize(self, context):
    await super().initialize(context)
    
    # Register for events
    self.register_hook("knowledge_stored", self.on_knowledge_stored)
    self.register_hook("query_executed", self.on_query_executed)
```

### Emitting Events

```python
# Emit custom events
await self.emit_event("my_custom_event", {
    "action": "processed",
    "items": 42
})
```

### Standard Events

- `knowledge_stored`: When knowledge is stored
- `knowledge_retrieved`: When knowledge is accessed
- `query_executed`: When a query runs
- `ethical_check_performed`: When content is reviewed
- `love_metric_calculated`: When love metrics update

## Love Alignment

### Using the Love Decorator

```python
from think_ai.plugins.base import love_required

class MyPlugin(Plugin):
    @love_required
    async def process_with_love(self, data):
        """This method requires love alignment."""
        # Processing that must be ethical
        return result
```

### Ethical Compliance Checking

```python
async def process_content(self, content):
    # Check ethical compliance
    if not await self.check_ethical_compliance(content):
        raise ValueError("Content failed ethical review")
    
    # Process content
    return processed_content
```

### Love Metrics Validation

```python
async def validate_action(self, action):
    # Validate against love metrics
    if await self.validate_love_metrics(action):
        # Action aligns with love principles
        return True
    return False
```

## Configuration

### Plugin Configuration Schema

```python
METADATA = PluginMetadata(
    name="configurable_plugin",
    version="1.0.0",
    # ... other fields ...
    config_schema={
        "type": "object",
        "properties": {
            "api_key": {
                "type": "string",
                "description": "API key for service"
            },
            "timeout": {
                "type": "integer",
                "default": 30,
                "description": "Request timeout in seconds"
            }
        },
        "required": ["api_key"]
    }
)
```

### Accessing Configuration

```python
async def initialize(self, context):
    await super().initialize(context)
    
    # Get config values
    self.api_key = self.get_config("api_key")
    self.timeout = self.get_config("timeout", 30)
```

## Testing

### Unit Testing

```python
import pytest
from think_ai.plugins.base import PluginContext

@pytest.mark.asyncio
async def test_plugin_initialization():
    plugin = MyPlugin()
    context = PluginContext(
        engine=None,
        config={"api_key": "test123"}
    )
    
    await plugin.initialize(context)
    assert plugin._initialized
    
    await plugin.shutdown()
    assert not plugin._initialized
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_plugin_with_engine():
    from think_ai.engine import ThinkAIEngine
    
    engine = ThinkAIEngine()
    plugin = MyPlugin()
    
    # Load plugin
    await engine.plugin_manager.load_plugin(
        "my_plugin",
        PluginContext(engine=engine, config={})
    )
    
    # Test plugin functionality
    result = await plugin.process_data("test")
    assert result is not None
```

### Love Alignment Testing

```python
@pytest.mark.asyncio
async def test_love_alignment():
    plugin = MyPlugin()
    
    # Test ethical compliance
    good_content = "Helping others with compassion"
    bad_content = "Harmful content"
    
    assert await plugin.check_ethical_compliance(good_content)
    assert not await plugin.check_ethical_compliance(bad_content)
```

## Packaging

### Directory Structure

```
my_plugin/
├── manifest.json
├── __init__.py
├── plugin.py
├── requirements.txt
├── README.md
├── LICENSE
└── tests/
    └── test_plugin.py
```

### Manifest File

```json
{
  "name": "my_plugin",
  "version": "1.0.0",
  "author": "Your Name",
  "description": "What your plugin does",
  "capabilities": ["storage_backend"],
  "dependencies": ["aiofiles>=0.8.0"],
  "love_aligned": true,
  "ethical_review_passed": false,
  "license": "Apache-2.0",
  "homepage": "https://github.com/yourusername/my_plugin",
  "tags": ["storage", "example"]
}
```

### Creating a Package

```bash
# Create archive
zip -r my_plugin-1.0.0.zip my_plugin/

# Create signature (optional but recommended)
sha256sum my_plugin-1.0.0.zip > my_plugin-1.0.0.zip.sig
```

## Distribution

### Publishing to Registry

```python
from think_ai.plugins.registry import PluginRegistry

registry = PluginRegistry()
registry.register_plugin(
    metadata=plugin.METADATA,
    source_url="https://github.com/user/plugin/releases/latest",
    verified=False  # True after review
)
```

### Marketplace Submission

```python
from think_ai.plugins.registry import PluginMarketplace

marketplace = PluginMarketplace(registry)
marketplace.submit_plugin(
    metadata=plugin.METADATA,
    source_url="https://github.com/user/plugin",
    category="Storage",
    description="Extended description for marketplace"
)
```

## Best Practices

### 1. Always Be Love-Aligned

- Consider the impact of your plugin on users
- Promote positive outcomes
- Avoid features that could cause harm
- Include safeguards against misuse

### 2. Handle Errors Gracefully

```python
try:
    result = await risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    await self.emit_event("error", {"message": str(e)})
    return None
```

### 3. Respect Resource Limits

```python
async def process_batch(self, items):
    # Process in chunks to avoid memory issues
    chunk_size = 100
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        await self.process_chunk(chunk)
        await asyncio.sleep(0)  # Yield to other tasks
```

### 4. Document Thoroughly

```python
async def complex_method(self, param1: str, param2: int) -> Dict[str, Any]:
    """
    Perform a complex operation.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Dictionary containing:
        - result: The operation result
        - metadata: Additional information
        
    Raises:
        ValueError: If parameters are invalid
    """
```

### 5. Version Compatibility

```python
def check_compatibility(self, engine_version: str) -> bool:
    """Check if plugin is compatible with engine version."""
    from packaging import version
    
    min_version = "1.0.0"
    max_version = "2.0.0"
    
    return (
        version.parse(min_version) <= 
        version.parse(engine_version) < 
        version.parse(max_version)
    )
```

## Security Considerations

### Input Validation

```python
async def process_user_input(self, user_input: str):
    # Sanitize input
    if not user_input or len(user_input) > 1000:
        raise ValueError("Invalid input")
    
    # Escape special characters
    safe_input = self.sanitize_input(user_input)
    
    # Process safely
    return await self.process_safe(safe_input)
```

### Sandboxing

```python
from think_ai.plugins.manager import PluginSandbox

sandbox = PluginSandbox(resource_limits={
    "memory_mb": 50,
    "cpu_percent": 10,
    "time_seconds": 10,
    "network_access": False
})

result = await sandbox.run_plugin(
    untrusted_plugin,
    "process",
    data
)
```

### Secure Storage

```python
import hashlib
from cryptography.fernet import Fernet

class SecurePlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.cipher = Fernet(self.get_or_create_key())
    
    def encrypt_sensitive(self, data: str) -> bytes:
        """Encrypt sensitive data."""
        return self.cipher.encrypt(data.encode())
    
    def decrypt_sensitive(self, encrypted: bytes) -> str:
        """Decrypt sensitive data."""
        return self.cipher.decrypt(encrypted).decode()
```

## Examples

### Complete Storage Plugin

See `think_ai/plugins/examples/file_storage.py` for a complete example.

### Complete UI Plugin

See `think_ai/plugins/examples/ui_visualization.py` for a complete example.

### Complete Analytics Plugin

See `think_ai/plugins/examples/analytics.py` for a complete example.

## Getting Help

- GitHub Issues: Report bugs and request features
- Community Forum: Ask questions and share plugins
- Documentation: Check the full Think AI docs
- Examples: Study the example plugins

## Contributing

We welcome plugin contributions that align with Think AI's mission of promoting understanding, compassion, and wellbeing. Please ensure your plugin:

1. Follows the love-aligned principles
2. Includes comprehensive tests
3. Has clear documentation
4. Handles errors gracefully
5. Respects user privacy

Submit your plugin for review to be included in the official registry!