# Think AI CLI Usage Guide

## Installation

### From Source (Development)
```bash
# Clone the repository
git clone https://github.com/champi-dev/think_ai
cd think_ai

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .
```

### From PyPI (Once Published)
```bash
pip install think-ai-consciousness
```

## Available Commands

Think AI provides multiple CLI entry points for different use cases:

### 1. **think-ai** - Main Interactive CLI
The primary CLI with rich interface and Claude integration.

```bash
think-ai [OPTIONS]

Options:
  --budget-profile {free_tier,minimal,balanced,power_user}
                        Budget profile to use (default: free_tier)
  --debug               Enable debug mode
  --no-restore          Don't restore previous memory (start fresh)
  --config CONFIG       Configuration file path

Examples:
  think-ai                          # Start with free tier
  think-ai --budget minimal         # Start with $5/month budget
  think-ai --debug                  # Enable debug mode
  think-ai --no-restore             # Start fresh (don't restore memory)
```

#### Interactive Commands
Once inside the CLI, you can use slash commands:
- `/query <question>` - Ask questions
- `/store <key> <value>` - Store knowledge
- `/search <term>` - Search knowledge base
- `/memory` - Show memory usage
- `/cost` - Show cost tracking
- `/claude <message>` - Direct Claude API access
- `/consciousness <state>` - Change consciousness state
- `/config` - View/modify configuration
- `/export <filename>` - Export conversation
- `/debug` - Toggle debug mode
- `/clear` - Clear conversation history
- `/exit` - Exit the CLI

### 2. **think-ai-chat** - Simple O(1) Chat
Lightweight chat interface with true O(1) performance.

```bash
think-ai-chat
```

Features:
- Hash-based O(1) responses
- No external API dependencies
- Instant responses
- Perfect for testing and demos

### 3. **think-ai-full** - Full System CLI
Complete Think AI system with all components enabled.

```bash
think-ai-full
```

Features:
- O(1) vector search
- Consciousness framework
- Knowledge graph
- Constitutional AI
- Self-training intelligence

### 4. **think-ai-server** - API Server
Start the FastAPI server for programmatic access.

```bash
think-ai-server
```

The server runs on `http://localhost:8080` by default.

## Configuration

### Environment Variables
Create a `.env` file in your project root:

```bash
# API Keys (optional)
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Storage
STORAGE_TYPE=local  # or 'cloud', 'distributed'
VECTOR_DB_TYPE=chromadb  # or 'qdrant'

# Performance
MAX_WORKERS=4
CACHE_SIZE=1000

# Debug
DEBUG=false
LOG_LEVEL=INFO
```

### Configuration File
You can also use a JSON configuration file:

```json
{
  "budget_profile": "minimal",
  "storage": {
    "type": "local",
    "path": "./data"
  },
  "models": {
    "default": "gpt-3.5-turbo",
    "embeddings": "text-embedding-ada-002"
  },
  "debug": false
}
```

Pass it to the CLI:
```bash
think-ai --config config.json
```

## Troubleshooting

### Import Errors
If you encounter import errors:
```bash
# Reinstall with all dependencies
pip install -e ".[all]"

# Or install specific extras
pip install -e ".[nlp,ml,api]"
```

### Torch Issues
If you see torch-related errors:
```bash
# Reinstall torch
pip uninstall torch
pip install torch==2.2.2
```

### Permission Errors
On Unix systems, you might need to make scripts executable:
```bash
chmod +x think_ai_full_cli.py
chmod +x think_ai_simple_chat.py
```

## Development

### Running Tests
```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_cli.py

# Run with coverage
make coverage
```

### Code Quality
```bash
# Format code
make format

# Run linters
make lint

# Run Think AI's O(1) linter
python think_ai_linter.py . --fix
```

## Examples

### Basic Usage
```python
# Using as a library
from think_ai import ThinkAIEngine

engine = ThinkAIEngine()
response = await engine.query("What is consciousness?")
print(response)
```

### CLI Script
```bash
#!/bin/bash
# Automated knowledge storage

think-ai <<EOF
/store quantum_computing "A type of computation using quantum phenomena"
/store machine_learning "Algorithms that improve through experience"
/query What is quantum computing?
/exit
EOF
```

## Performance

The Think AI CLI is optimized for O(1) performance:
- Average query time: 0.18ms
- Throughput: 88.8 queries/second
- Memory usage: <100MB baseline
- No GPU required

## Support

- GitHub Issues: https://github.com/champi-dev/think_ai/issues
- Documentation: https://docs.think-ai.dev
- Discord: https://discord.gg/think-ai

## License

MIT License - see LICENSE file for details.