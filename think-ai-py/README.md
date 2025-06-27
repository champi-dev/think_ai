# Think AI - Python Library

🧠 **Think AI** - Quantum Consciousness AI Library for Python

Access the latest intelligence and knowledge of Think AI's quantum consciousness AI system through this comprehensive Python library and CLI.

## Features

- 🚀 **O(1) Performance** - Lightning-fast AI responses with hash-based lookups
- 🧠 **Quantum Consciousness** - Advanced AI with self-awareness capabilities
- 💬 **Real-time Chat** - Interactive conversations with streaming responses
- 🔍 **Knowledge Search** - Search through vast knowledge bases
- 📊 **System Monitoring** - Health checks and performance statistics
- 🌐 **Async Support** - Full asyncio compatibility
- 🎨 **Rich CLI** - Beautiful command-line interface with colors and tables

## Installation

```bash
pip install think-ai
```

## Quick Start

### Python Library

```python
from think_ai import ThinkAI, quick_chat

# Quick one-shot chat
response = quick_chat("What is quantum consciousness?")
print(response)

# Full client usage
client = ThinkAI()

# Chat with Think AI
response = client.ask("Explain machine learning")
print(response)

# Search knowledge base
results = client.search("artificial intelligence", limit=5)
for result in results:
    print(f"Score: {result.score} - {result.content}")

# Get system statistics
stats = client.get_stats()
print(f"Knowledge nodes: {stats.total_nodes}")
print(f"Average confidence: {stats.average_confidence:.1%}")

# Check system health
health = client.get_health()
print(f"Status: {health.status}")
```

### Async Usage

```python
import asyncio
from think_ai import AsyncThinkAI, ThinkAIConfig

async def main():
    config = ThinkAIConfig(debug=True)
    
    async with AsyncThinkAI(config) as client:
        response = await client.ask("What is the meaning of consciousness?")
        print(response)

asyncio.run(main())
```

### Streaming Responses

```python
from think_ai import ThinkAI, ChatRequest

client = ThinkAI()

def handle_chunk(chunk):
    if chunk.chunk:
        print(chunk.chunk, end="", flush=True)
    if chunk.done:
        print("\n--- Response complete ---")

request = ChatRequest(query="Tell me about quantum computing")
client.stream_chat(request, handle_chunk)
```

## Command Line Interface

### Interactive Chat

```bash
# Start interactive chat session
think-ai chat

# Chat with streaming responses
think-ai chat --stream
```

### One-shot Questions

```bash
# Ask a single question
think-ai ask "What is artificial intelligence?"

# Stream the response
think-ai ask "Explain quantum mechanics" --stream
```

### Knowledge Search

```bash
# Search the knowledge base
think-ai search "machine learning algorithms" --limit 10
```

### System Monitoring

```bash
# Check system status
think-ai status

# Test connection
think-ai ping

# List knowledge domains
think-ai domains

# Show configuration
think-ai config
```

### Global Options

```bash
# Use custom server URL
think-ai --url https://your-server.com chat

# Set timeout
think-ai --timeout 60 ask "Complex question"

# Enable debug mode
think-ai --debug status
```

## Configuration

```python
from think_ai import ThinkAI, ThinkAIConfig

config = ThinkAIConfig(
    base_url="https://thinkai-production.up.railway.app",
    timeout=30,  # seconds
    debug=True
)

client = ThinkAI(config)
```

## API Reference

### ThinkAI Client

#### Methods

- `chat(request: ChatRequest) -> ChatResponse` - Send chat message
- `ask(question: str) -> str` - Quick chat interface
- `get_stats() -> SystemStats` - Get system statistics
- `get_health() -> HealthStatus` - Check system health
- `search(query: str, limit: int = 10) -> List[SearchResult]` - Search knowledge
- `stream_chat(request: ChatRequest, on_chunk: Callable)` - Stream responses
- `ping() -> bool` - Test connection
- `get_domains() -> List[KnowledgeDomain]` - Get knowledge domains

### Data Models

#### ChatRequest
```python
ChatRequest(
    query: str,                    # Required: User message
    context: List[str] = None,     # Optional: Conversation context
    max_length: int = None         # Optional: Response length limit
)
```

#### ChatResponse
```python
ChatResponse(
    response: str,                 # AI response text
    context: List[str],           # Context used
    response_time_ms: int,        # Response time
    confidence: float             # Confidence score (0-1)
)
```

#### SystemStats
```python
SystemStats(
    total_nodes: int,                        # Knowledge nodes
    training_iterations: int,                # Training iterations
    total_knowledge_items: int,              # Knowledge items
    domain_distribution: Dict[str, int],     # Domain distribution
    average_confidence: float,               # Average confidence
    uptime: int                             # System uptime (seconds)
)
```

## Error Handling

```python
from think_ai import ThinkAI, ThinkAIError

client = ThinkAI()

try:
    response = client.ask("Hello Think AI!")
    print(response)
except ThinkAIError as e:
    print(f"Think AI Error: {e.message}")
    print(f"Status Code: {e.status}")
    print(f"Error Code: {e.code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/think-ai/think-ai-py
cd think-ai-py
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
pytest --asyncio-mode=auto  # For async tests
```

### Code Formatting

```bash
black think_ai/
flake8 think_ai/
mypy think_ai/
```

## Performance

Think AI achieves **O(1) performance** through:

- 🔥 **Hash-based lookups** for instant knowledge retrieval
- ⚡ **Pre-computed responses** for common queries
- 🚀 **Optimized algorithms** using divide-and-conquer techniques
- 💾 **Intelligent caching** with space-time optimization

Average response time: **< 2ms**

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/think-ai/think-ai-py/issues)
- 📖 **Documentation**: [https://thinkai-production.up.railway.app/docs](https://thinkai-production.up.railway.app/docs)
- 💬 **Community**: Join our Discord server
- 📧 **Contact**: team@think-ai.dev

---

**Think AI** - Advancing consciousness through quantum intelligence 🧠✨