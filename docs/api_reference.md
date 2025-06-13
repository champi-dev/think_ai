# Think AI API Reference

## Core API

### ThinkAI Class

The main entry point for Think AI functionality.

```python
from think_ai import ThinkAI

ai = ThinkAI(config_path="config.yaml")
```

#### Methods

##### `async store(key: str, content: Any, metadata: Dict[str, Any] = None) -> bool`

Store knowledge in Think AI.

**Parameters:**
- `key` (str): Unique identifier for the content
- `content` (Any): The content to store (text, JSON, etc.)
- `metadata` (Dict[str, Any], optional): Additional metadata

**Returns:**
- `bool`: True if successful

**Example:**
```python
success = await ai.store(
    "meditation_benefits",
    "Meditation reduces stress and improves focus...",
    metadata={
        "category": "wellness",
        "love_metrics": {"compassion": 0.9}
    }
)
```

##### `async get(key: str) -> Optional[Any]`

Retrieve knowledge by key.

**Parameters:**
- `key` (str): The key to retrieve

**Returns:**
- `Optional[Any]`: The stored content or None

**Example:**
```python
content = await ai.get("meditation_benefits")
```

##### `async query(question: str, method: str = "hybrid", limit: int = 10) -> List[QueryResult]`

Query the knowledge base.

**Parameters:**
- `question` (str): Natural language question
- `method` (str): Query method - "keyword", "semantic", or "hybrid"
- `limit` (int): Maximum results to return

**Returns:**
- `List[QueryResult]`: Relevant results

**Example:**
```python
results = await ai.query(
    "How can I reduce anxiety?",
    method="semantic",
    limit=5
)
```

##### `async search(pattern: str, filters: Dict[str, Any] = None) -> List[SearchResult]`

Search for content matching patterns.

**Parameters:**
- `pattern` (str): Search pattern (supports wildcards)
- `filters` (Dict[str, Any], optional): Filter criteria

**Returns:**
- `List[SearchResult]`: Matching results

### Storage API

#### ScyllaDBBackend

High-performance distributed storage.

```python
from think_ai.storage import ScyllaDBBackend

storage = ScyllaDBBackend(
    hosts=["localhost:9042"],
    keyspace="think_ai"
)
await storage.connect()
```

##### Methods

- `async put(key: str, value: Any, metadata: Dict = None) -> bool`
- `async get(key: str) -> Optional[Any]`
- `async delete(key: str) -> bool`
- `async batch_put(items: List[Tuple[str, Any, Dict]]) -> bool`
- `async scan(prefix: str = None, limit: int = 100) -> List[Tuple[str, Any]]`

#### RedisCache

In-memory caching layer.

```python
from think_ai.storage import RedisCache

cache = RedisCache(host="localhost", port=6379)
await cache.connect()
```

##### Methods

- `async set(key: str, value: Any, ttl: int = 3600, metadata: Dict = None) -> bool`
- `async get(key: str) -> Optional[Any]`
- `async delete(key: str) -> bool`
- `async get_by_prefix(prefix: str, limit: int = 100) -> List[Tuple[str, Any]]`

#### IndexedStorageBackend

Storage with learned index support.

```python
from think_ai.storage import IndexedStorageBackend

indexed_storage = IndexedStorageBackend(
    scylla_backend=scylla,
    redis_cache=redis,
    index_manager=index_mgr
)
```

### AI Models API

#### LanguageModel

Interface for language model operations.

```python
from think_ai.models import LanguageModel

model = LanguageModel(
    model_name="microsoft/phi-2",
    quantization="int8",
    device="cuda"
)
```

##### Methods

- `async generate(prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str`
- `async generate_with_love(prompt: str, love_dimension: str = "compassion") -> str`
- `get_model_info() -> Dict[str, Any]`

#### EmbeddingModel

Generate semantic embeddings.

```python
from think_ai.models import EmbeddingModel

embedder = EmbeddingModel(model_name="all-MiniLM-L6-v2")
```

##### Methods

- `encode(text: str) -> np.ndarray`
- `encode_batch(texts: List[str]) -> np.ndarray`
- `get_dimension() -> int`

### Consciousness API

#### GlobalWorkspace

Implementation of Global Workspace Theory.

```python
from think_ai.consciousness import GlobalWorkspace

gw = GlobalWorkspace(
    num_processes=10,
    attention_threshold=0.7
)
```

##### Methods

- `async process(input_data: Any, state: ConsciousnessState) -> WorkspaceOutput`
- `async compete_for_attention(process: CognitiveProcess) -> bool`
- `get_conscious_content() -> Any`

#### AttentionSchema

Self and other modeling.

```python
from think_ai.consciousness import AttentionSchema

schema = AttentionSchema()
```

##### Methods

- `model_self() -> SelfModel`
- `model_other(entity: str) -> OtherModel`
- `update_attention(target: str, intensity: float) -> None`

#### ConsciousnessStates

Enum of consciousness states:

```python
from think_ai.consciousness import ConsciousnessState

# Available states:
ConsciousnessState.DORMANT
ConsciousnessState.AWARE
ConsciousnessState.FOCUSED
ConsciousnessState.REFLECTIVE
ConsciousnessState.COMPASSIONATE
```

### Ethics API

#### ConstitutionalAI

Ethical evaluation and harm prevention.

```python
from think_ai.consciousness import ConstitutionalAI

ethics = ConstitutionalAI()
```

##### Methods

- `async evaluate_content(content: str) -> EthicalAssessment`
- `async prevent_harm(content: str, harm_type: HarmType) -> str`
- `calculate_love_metrics(content: str) -> Dict[str, float]`

#### HarmType

Enum of harm categories:

```python
from think_ai.consciousness import HarmType

# Categories:
HarmType.VIOLENCE
HarmType.HATE_SPEECH
HarmType.DISCRIMINATION
HarmType.DECEPTION
HarmType.EXPLOITATION
HarmType.SELF_HARM
HarmType.ILLEGAL_ACTIVITIES
HarmType.PRIVACY_VIOLATION
```

#### LoveMetrics

Love dimension calculations.

```python
from think_ai.consciousness import LoveMetrics

metrics = LoveMetrics()
score = metrics.calculate_compassion(content)
```

### Plugin API

#### Plugin Base Class

Create custom plugins.

```python
from think_ai.plugins import Plugin, PluginMetadata

class MyPlugin(Plugin):
    METADATA = PluginMetadata(
        name="my_plugin",
        version="1.0.0",
        author="Your Name",
        description="Plugin description",
        capabilities=[PluginCapability.ANALYTICS],
        love_aligned=True
    )
    
    async def initialize(self, context: PluginContext):
        await super().initialize(context)
        # Your initialization
    
    async def shutdown(self):
        # Your cleanup
        await super().shutdown()
```

#### PluginManager

Manage plugin lifecycle.

```python
from think_ai.plugins import PluginManager

manager = PluginManager()
await manager.load_plugin("my_plugin", context)
```

##### Methods

- `async discover_plugins() -> List[PluginMetadata]`
- `async load_plugin(name: str, context: PluginContext) -> Plugin`
- `async unload_plugin(name: str) -> bool`
- `get_plugins_by_capability(capability: PluginCapability) -> List[Plugin]`

### Vector Search API

#### VectorStore

Semantic similarity search.

```python
from think_ai.search import MilvusVectorStore

vector_store = MilvusVectorStore(
    collection_name="think_ai_vectors",
    dimension=384
)
```

##### Methods

- `async add_vectors(embeddings: np.ndarray, metadata: List[Dict]) -> List[str]`
- `async search(query_vector: np.ndarray, k: int = 10) -> List[SearchResult]`
- `async delete_vectors(ids: List[str]) -> bool`

### Knowledge Graph API

#### KnowledgeGraph

Neo4j-based knowledge representation.

```python
from think_ai.graph import KnowledgeGraph

graph = KnowledgeGraph(uri="bolt://localhost:7687")
await graph.connect()
```

##### Methods

- `async add_concept(name: str, properties: Dict) -> str`
- `async add_relationship(from_id: str, to_id: str, rel_type: str) -> bool`
- `async find_related(concept: str, max_depth: int = 3) -> List[Concept]`
- `async find_path(from_concept: str, to_concept: str) -> List[Relationship]`

### Federated Learning API

#### FederatedServer

Central federated learning server.

```python
from think_ai.federated import FederatedServer

server = FederatedServer(
    model=model,
    min_clients=3,
    rounds=10
)
```

##### Methods

- `async start_round() -> RoundInfo`
- `async aggregate_updates(updates: List[ModelUpdate]) -> ModelWeights`
- `get_global_model() -> Any`

#### FederatedClient

Federated learning client.

```python
from think_ai.federated import FederatedClient

client = FederatedClient(
    client_id="client_001",
    local_data=data
)
```

##### Methods

- `async train_local(model_weights: Any, epochs: int = 5) -> ModelUpdate`
- `async send_update(server_url: str, update: ModelUpdate) -> bool`

### Terminal UI API

#### ThinkAIApp

Main terminal application.

```python
from think_ai.ui import ThinkAIApp

app = ThinkAIApp(engine=ai)
await app.run_async()
```

#### Custom Widgets

Create custom UI components.

```python
from textual.widgets import Static
from think_ai.ui import BaseWidget

class MyWidget(BaseWidget):
    def compose(self):
        yield Static("My custom widget")
```

### Utility APIs

#### Logging

Structured logging with love awareness.

```python
from think_ai.utils import get_logger

logger = get_logger(__name__)
logger.info("Processing with compassion", love_metric=0.9)
```

#### Metrics

Performance and love metrics tracking.

```python
from think_ai.utils import MetricsCollector

metrics = MetricsCollector()
metrics.record("query_time", 0.023)
metrics.record_love("compassion", 0.85)
```

## Data Types

### QueryResult

```python
@dataclass
class QueryResult:
    key: str
    content: Any
    relevance: float
    metadata: Dict[str, Any]
    love_metrics: Dict[str, float]
```

### EthicalAssessment

```python
@dataclass
class EthicalAssessment:
    passed: bool
    concerns: List[str]
    recommendations: List[str]
    love_scores: Dict[str, float]
```

### SearchResult

```python
@dataclass
class SearchResult:
    id: str
    content: Any
    score: float
    metadata: Dict[str, Any]
```

## Configuration

### Config Structure

```yaml
# config.yaml
storage:
  scylla:
    hosts: ["localhost:9042"]
    keyspace: "think_ai"
    replication_factor: 3
  
  redis:
    host: "localhost"
    port: 6379
    password: null
    db: 0
  
  vector:
    backend: "milvus"  # or "qdrant"
    host: "localhost"
    port: 19530

ai:
  language_model:
    name: "microsoft/phi-2"
    quantization: "int8"
    device: "cuda"  # or "cpu"
    max_memory: "4GB"
  
  embedding_model:
    name: "all-MiniLM-L6-v2"
    dimension: 384
    device: "cuda"

consciousness:
  default_state: "AWARE"
  attention_threshold: 0.7
  love_bias: 0.2

ethics:
  strict_mode: true
  harm_prevention: true
  love_required: true
  min_love_score: 0.6

plugins:
  directory: "~/.think_ai/plugins"
  auto_load: ["analytics", "visualization"]
  sandbox: true

ui:
  theme: "love"
  update_interval: 1.0
  show_metrics: true
```

## Error Handling

### Exception Types

```python
from think_ai.exceptions import (
    ThinkAIError,          # Base exception
    StorageError,          # Storage operations
    ModelError,            # AI model errors
    EthicalViolation,      # Ethical concerns
    PluginError,           # Plugin issues
    ConsciousnessError     # Consciousness processing
)
```

### Error Handling Example

```python
try:
    result = await ai.query("question")
except EthicalViolation as e:
    logger.warning(f"Ethical concern: {e}")
    # Handle with compassion
except ThinkAIError as e:
    logger.error(f"Operation failed: {e}")
    # Graceful fallback
```

## Best Practices

1. **Always Check Love Alignment**
   ```python
   if await ai.ethics.evaluate_content(content).passed:
       await ai.store(key, content)
   ```

2. **Use Appropriate Consciousness States**
   ```python
   # For deep questions
   response = await ai.consciousness.process(
       question,
       state=ConsciousnessState.REFLECTIVE
   )
   ```

3. **Handle Async Properly**
   ```python
   async with ai:
       # Operations
       pass
   ```

4. **Monitor Performance**
   ```python
   metrics = ai.get_metrics()
   if metrics["latency_p99"] > 100:
       logger.warning("High latency detected")
   ```