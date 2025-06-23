# Think AI CLI Comprehensive Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation & Setup](#installation--setup)
3. [CLI Commands Overview](#cli-commands-overview)
4. [Detailed Command Reference](#detailed-command-reference)
5. [Configuration](#configuration)
6. [Architecture & Design](#architecture--design)
7. [Performance Optimization](#performance-optimization)
8. [Examples & Use Cases](#examples--use-cases)
9. [Troubleshooting](#troubleshooting)
10. [Development Guide](#development-guide)
11. [API Reference](#api-reference)
12. [FAQ](#faq)

## Introduction

Think AI provides a suite of command-line interfaces designed for different use cases, from simple demonstrations to full-featured AI interactions. All CLIs maintain O(1) performance guarantees while offering varying levels of functionality.

### Key Features
- **O(1) Performance**: Average query time of 0.18ms
- **Multiple Interfaces**: Choose the right tool for your needs
- **Rich Interactive UI**: Modern terminal experience with colors and formatting
- **Claude Integration**: Direct access to Claude API
- **Memory Persistence**: Save and restore conversation state
- **Cost Tracking**: Monitor API usage and costs
- **Extensible Architecture**: Plugin-ready design

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### From Source (Development)
```bash
# Clone the repository
git clone https://github.com/champi-dev/think_ai
cd think_ai

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with all dependencies
pip install -e ".[all]"

# Run initial setup
make install
```

### From PyPI (Once Published)
```bash
pip install think-ai-consciousness
```

### Quick Start
```bash
# Start the main interactive CLI
think-ai

# Start with specific budget profile
think-ai --budget balanced

# Start the simple O(1) chat demo
think-ai-chat

# Start the API server
think-ai-server
```

## CLI Commands Overview

Think AI provides four distinct CLI entry points:

| Command | Purpose | Key Features | Use Case |
|---------|---------|--------------|----------|
| `think-ai` | Main interactive CLI | Rich UI, Claude API, full features | Daily interactive use |
| `think-ai-chat` | Simple O(1) demo | Hash-based responses, no dependencies | Testing, demos |
| `think-ai-full` | Full system showcase | All components enabled | Development, testing |
| `think-ai-server` | API server | RESTful API, programmatic access | Integration, services |

## Detailed Command Reference

### think-ai (Main Interactive CLI)

The primary CLI interface with rich terminal UI and comprehensive features.

#### Command Line Options
```bash
think-ai [OPTIONS]

Options:
  --budget-profile TEXT    Budget profile: free_tier, minimal, balanced, power_user
  --debug                  Enable debug mode for detailed logging
  --no-restore            Start fresh without restoring previous memory
  --config PATH           Path to configuration file (JSON)
  --help                  Show this help message and exit
```

#### Interactive Commands
Once inside the CLI, use slash commands for various operations:

| Command | Description | Example |
|---------|-------------|---------|
| `/query <question>` | Ask questions to the AI | `/query What is consciousness?` |
| `/store <key> <value>` | Store knowledge in memory | `/store quantum "Subatomic particle physics"` |
| `/search <term>` | Search knowledge base | `/search quantum` |
| `/memory` | Display memory usage statistics | `/memory` |
| `/cost` | Show API cost tracking | `/cost` |
| `/claude <message>` | Direct Claude API access | `/claude Explain recursion` |
| `/consciousness <state>` | Change consciousness state | `/consciousness analytical` |
| `/config` | View/modify configuration | `/config` |
| `/export <filename>` | Export conversation history | `/export chat_log.json` |
| `/debug` | Toggle debug mode | `/debug` |
| `/clear` | Clear conversation history | `/clear` |
| `/help` | Show help for all commands | `/help` |
| `/exit` | Exit the CLI | `/exit` |

#### Budget Profiles

| Profile | Monthly Budget | API Calls | Best For |
|---------|---------------|-----------|----------|
| `free_tier` | $0 | Limited | Testing, learning |
| `minimal` | $5 | ~500 | Personal use |
| `balanced` | $20 | ~2000 | Regular use |
| `power_user` | $100 | ~10000 | Heavy use |

### think-ai-chat (Simple O(1) Chat)

Lightweight chat interface demonstrating true O(1) performance without external dependencies.

```bash
think-ai-chat
```

#### Features
- Hash-based response system
- No API dependencies
- Instant responses (< 1ms)
- Built-in command history
- Performance statistics

#### Commands
- `stats` - Show performance statistics
- `history` - Display conversation history
- `clear` - Clear history
- `help` - Show available commands
- `exit` or `quit` - Exit the chat

### think-ai-full (Full System CLI)

Complete Think AI system with all components enabled for testing and development.

```bash
think-ai-full
```

#### Features
- O(1) vector search with LSH
- Consciousness framework
- Knowledge graph integration
- Constitutional AI
- Self-training intelligence
- Code generation

#### Commands
- `stats` - System performance metrics
- `history` - Conversation history
- `conscious` - Consciousness state info
- `knowledge` - Knowledge graph stats
- `train` - Trigger self-training
- `code` - Code generation mode
- `clear` - Clear all data
- `help` - Command help
- `exit` - Exit

### think-ai-server (API Server)

FastAPI server providing RESTful API access to Think AI functionality.

```bash
think-ai-server [OPTIONS]

Options:
  --host TEXT     Host to bind to (default: 0.0.0.0)
  --port INT      Port to bind to (default: 8080)
  --reload        Enable auto-reload for development
```

#### API Endpoints
- `GET /` - Health check
- `POST /query` - Submit queries
- `GET /memory` - Memory statistics
- `POST /store` - Store knowledge
- `GET /search` - Search knowledge base
- `GET /consciousness` - Current state
- `POST /consciousness` - Change state

## Configuration

### Environment Variables (.env)
```bash
# API Keys
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Storage Configuration
STORAGE_TYPE=local              # local, cloud, distributed
VECTOR_DB_TYPE=chromadb         # chromadb, qdrant
STORAGE_PATH=./data

# Performance Settings
MAX_WORKERS=4
CACHE_SIZE=1000
BATCH_SIZE=32

# Logging
DEBUG=false
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT=json                 # json, text

# API Server
API_HOST=0.0.0.0
API_PORT=8080
API_WORKERS=4
```

### Configuration File (config.json)
```json
{
  "budget_profile": "balanced",
  "api_keys": {
    "anthropic": "${ANTHROPIC_API_KEY}",
    "openai": "${OPENAI_API_KEY}"
  },
  "storage": {
    "type": "local",
    "path": "./data",
    "vector_db": {
      "type": "chromadb",
      "collection": "think_ai_main"
    }
  },
  "models": {
    "default": "claude-3-opus-20240229",
    "embeddings": "text-embedding-3-small",
    "fallback": "gpt-3.5-turbo"
  },
  "performance": {
    "max_workers": 4,
    "cache_size": 1000,
    "batch_size": 32,
    "timeout": 30
  },
  "consciousness": {
    "default_state": "analytical",
    "transition_speed": 0.5
  },
  "debug": false,
  "logging": {
    "level": "INFO",
    "format": "json",
    "file": "think_ai.log"
  }
}
```

### Per-User Configuration
Store user-specific settings in `~/.think_ai/config.json`:
```json
{
  "user_profile": {
    "name": "Your Name",
    "preferences": {
      "theme": "dark",
      "language": "en",
      "timezone": "UTC"
    }
  },
  "shortcuts": {
    "q": "/query",
    "s": "/search",
    "m": "/memory"
  }
}
```

## Architecture & Design

### Component Overview
```
think_ai/
├── cli_wrapper.py          # Central entry point handler
├── cli/
│   ├── main.py            # Rich interactive CLI
│   ├── commands.py        # Command implementations
│   └── utils.py           # CLI utilities
├── api/
│   ├── server.py          # FastAPI server
│   └── endpoints.py       # API route handlers
├── core/
│   ├── engine.py          # O(1) processing engine
│   ├── config.py          # Configuration management
│   └── performance.py     # Performance monitoring
└── models/
    ├── claude.py          # Claude API integration
    └── embeddings.py      # Embedding models
```

### Design Principles

#### 1. Lazy Loading
Prevents circular imports and improves startup time:
```python
# Lazy import pattern used throughout
def get_engine():
    global _engine
    if _engine is None:
        from .core.engine import ThinkAIEngine
        _engine = ThinkAIEngine()
    return _engine
```

#### 2. Async-First Design
All I/O operations are asynchronous:
```python
async def process_query(query: str) -> str:
    # Non-blocking processing
    result = await engine.query_async(query)
    return result
```

#### 3. Error Recovery
Graceful handling of failures:
```python
try:
    response = await api_call()
except APIError:
    # Fallback to local processing
    response = await local_fallback()
```

#### 4. Plugin Architecture
Extensible command system:
```python
# Register custom commands
@cli.command()
def custom_command(args):
    """Custom command implementation"""
    pass
```

## Performance Optimization

### O(1) Guarantees
- **Hash-based lookups**: Direct memory access
- **LSH for vectors**: Locality-sensitive hashing
- **Precomputed embeddings**: No runtime computation
- **Memory-mapped files**: Efficient large data access

### Performance Metrics
```
Average Query Time: 0.18ms
Throughput: 88.8 queries/second
Memory Usage: <100MB baseline
CPU Usage: <5% idle, <20% active
```

### Optimization Tips
1. **Use appropriate budget profiles** to control API usage
2. **Enable caching** for repeated queries
3. **Batch operations** when possible
4. **Monitor with `/memory`** command
5. **Use local models** for offline operation

## Examples & Use Cases

### Basic Interactive Session
```bash
$ think-ai
Welcome to Think AI CLI! 🧠
Type /help for available commands.

> /query What is the meaning of life?
The meaning of life is a profound philosophical question...

> /store philosophy "The study of fundamental questions"
Stored: philosophy -> The study of fundamental questions

> /search philosophy
Found 1 result:
- philosophy: The study of fundamental questions

> /cost
Current session cost: $0.02
Monthly total: $1.45
Budget remaining: $18.55

> /exit
Goodbye! Session saved.
```

### Scripted Automation
```bash
#!/bin/bash
# knowledge_import.sh

# Import knowledge from file
while IFS='=' read -r key value; do
    echo "/store $key \"$value\""
done < knowledge.txt | think-ai --no-restore

# Query the imported knowledge
echo "/query Tell me about quantum computing" | think-ai
```

### Python Integration
```python
import subprocess
import json

def query_think_ai(question):
    """Query Think AI via CLI"""
    result = subprocess.run(
        ['think-ai', '--no-restore'],
        input=f'/query {question}\n/exit\n',
        capture_output=True,
        text=True
    )
    return result.stdout

# Use in application
response = query_think_ai("Explain machine learning")
print(response)
```

### API Server Usage
```python
import requests

# Start server: think-ai-server

# Query endpoint
response = requests.post(
    'http://localhost:8080/query',
    json={'question': 'What is AI?'}
)
print(response.json())

# Store knowledge
requests.post(
    'http://localhost:8080/store',
    json={'key': 'ml', 'value': 'Machine Learning'}
)

# Search
results = requests.get(
    'http://localhost:8080/search',
    params={'term': 'ml'}
)
print(results.json())
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -e .

# Expose API port
EXPOSE 8080

# Start server by default
CMD ["think-ai-server", "--host", "0.0.0.0"]
```

```bash
# Build and run
docker build -t think-ai .
docker run -p 8080:8080 -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY think-ai
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Issue: ModuleNotFoundError
# Solution: Reinstall with all dependencies
pip install -e ".[all]"

# For specific components
pip install -e ".[nlp,ml,api]"
```

#### Torch/CUDA Issues
```bash
# Issue: Torch not found or CUDA errors
# Solution: Reinstall CPU-only torch
pip uninstall torch
pip install torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu
```

#### Permission Errors
```bash
# Issue: Permission denied on Unix
# Solution: Make scripts executable
chmod +x think_ai/*.py
chmod +x scripts/*

# For system-wide install
sudo pip install -e .
```

#### API Key Issues
```bash
# Issue: API key not found
# Solution: Set environment variable
export ANTHROPIC_API_KEY="your-key-here"

# Or create .env file
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

#### Memory Issues
```bash
# Issue: Out of memory
# Solution: Reduce cache size
export CACHE_SIZE=100

# Or use config
think-ai --config low_memory_config.json
```

### Debug Mode
Enable comprehensive logging:
```bash
# Command line
think-ai --debug

# Environment variable
export THINK_AI_DEBUG=1
export LOG_LEVEL=DEBUG

# In session
> /debug
Debug mode enabled
```

### Performance Profiling
```bash
# Run performance test
python performance_test.py

# Profile specific operation
python -m cProfile -o profile.stats think_ai_simple_chat.py

# Analyze results
python -m pstats profile.stats
```

## Development Guide

### Setting Up Development Environment
```bash
# Clone and setup
git clone https://github.com/champi-dev/think_ai
cd think_ai
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -e ".[dev]"
pre-commit install

# Run tests
make test
make coverage
```

### Adding New Commands

1. **Define command in `cli/commands.py`**:
```python
async def custom_command(engine, args):
    """Implementation of custom command"""
    result = await engine.process(args)
    return format_result(result)
```

2. **Register in `cli/main.py`**:
```python
COMMANDS = {
    'custom': custom_command,
    # ... other commands
}
```

3. **Add help text**:
```python
HELP_TEXT = {
    'custom': 'Description of custom command',
    # ... other help
}
```

4. **Write tests**:
```python
# tests/test_custom_command.py
async def test_custom_command():
    result = await custom_command(mock_engine, "test args")
    assert result == expected_output
```

### Code Style Guidelines
```bash
# Format code
make format

# Run linters
make lint

# Type checking
mypy think_ai/

# O(1) complexity check
python think_ai_linter.py . --check
```

### Testing Strategy
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Performance tests
python performance_test.py
python think_ai_1000_iterations_cpu.py

# CLI tests
python test_cli_automated.py
```

### Release Process
1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Run full test suite
4. Create git tag
5. Build distribution
6. Upload to PyPI

```bash
# Build
python setup.py sdist bdist_wheel

# Test upload
twine upload --repository testpypi dist/*

# Production upload
twine upload dist/*
```

## API Reference

### Core Classes

#### ThinkAIEngine
```python
class ThinkAIEngine:
    """Main processing engine with O(1) guarantees"""
    
    async def query(self, text: str) -> str:
        """Process a query and return response"""
        
    async def store(self, key: str, value: str) -> bool:
        """Store knowledge in memory"""
        
    async def search(self, term: str) -> List[Dict]:
        """Search knowledge base"""
```

#### ConsciousnessFramework
```python
class ConsciousnessFramework:
    """Manages AI consciousness states"""
    
    def set_state(self, state: str) -> None:
        """Change consciousness state"""
        
    def get_state(self) -> str:
        """Get current state"""
```

### CLI Module API

#### Command Registration
```python
from think_ai.cli import register_command

@register_command("mycommand")
async def my_command(engine, args):
    """Custom command implementation"""
    return await engine.process(args)
```

#### Configuration Access
```python
from think_ai import get_config

config = get_config()
api_key = config.get("api_keys.anthropic")
```

### Server API Endpoints

#### POST /query
```json
// Request
{
    "question": "What is consciousness?",
    "context": "philosophical",
    "max_tokens": 500
}

// Response
{
    "answer": "Consciousness is...",
    "confidence": 0.95,
    "sources": ["memory", "api"],
    "cost": 0.02
}
```

#### POST /store
```json
// Request
{
    "key": "quantum_computing",
    "value": "Computing using quantum mechanics",
    "tags": ["physics", "computing"]
}

// Response
{
    "success": true,
    "stored_at": "2024-01-15T10:30:00Z"
}
```

## FAQ

### General Questions

**Q: Do I need a GPU to run Think AI?**
A: No, Think AI is designed to run efficiently on CPU with O(1) performance guarantees.

**Q: Can I use Think AI offline?**
A: Yes, use `think-ai-chat` for offline operation with hash-based responses.

**Q: How do I backup my data?**
A: Data is stored in `./data` by default. Simply backup this directory.

**Q: Can I use custom models?**
A: Yes, configure custom models in the config file under the `models` section.

### Performance Questions

**Q: What does O(1) performance mean?**
A: Constant time complexity - operations complete in the same time regardless of data size.

**Q: How much memory does Think AI use?**
A: Base memory usage is under 100MB, scaling based on stored knowledge.

**Q: Can I run multiple instances?**
A: Yes, each instance maintains its own state and can run concurrently.

### API Questions

**Q: How do I get API keys?**
A: 
- Anthropic: https://console.anthropic.com/
- OpenAI: https://platform.openai.com/api-keys

**Q: What's the rate limiting?**
A: Depends on your API tier. Think AI implements automatic retry with exponential backoff.

**Q: Can I use local models?**
A: Yes, configure local model endpoints in the configuration file.

### Development Questions

**Q: How do I contribute?**
A: Fork the repo, create a feature branch, and submit a pull request. See CONTRIBUTING.md.

**Q: Where do I report bugs?**
A: GitHub Issues: https://github.com/champi-dev/think_ai/issues

**Q: Can I add custom commands?**
A: Yes, see the Development Guide section for instructions.

## Support & Resources

- **Documentation**: https://docs.think-ai.dev
- **GitHub**: https://github.com/champi-dev/think_ai
- **Discord**: https://discord.gg/think-ai
- **Email**: support@think-ai.dev

## License

MIT License - see LICENSE file for details.

---

*Think AI CLI - Consciousness at the speed of thought*