# Think AI CLI (Python)

**Version:** 0.2.0 | **Last Updated:** December 22, 2024

AI-powered coding assistant with O(1) vector search capabilities. Part of the Think AI superintelligent consciousness system. Uses CPU-optimized vector search for maximum compatibility.

## Installation

```bash
pip install think-ai-cli
```

For production deployment or environments without compilation:
```bash
# Use O(1) vector search (no compilation needed)
pip install think-ai-cli[o1]

# For Railway/Docker deployments
pip install think-ai-cli[production]
```

## Features

- 🔍 **Semantic Code Search** - Find similar code patterns using AI
- 🚀 **Code Generation** - Generate code from natural language prompts
- 📊 **Code Analysis** - Analyze code for patterns and improvements
- 💾 **Local Knowledge Base** - Build your own code snippet database
- 🎨 **Beautiful CLI** - Rich terminal UI with syntax highlighting

## Usage

### Search for code patterns
```bash
think search "implement binary search"
```

### Add code to knowledge base
```bash
think add --file example.py --language python --description "Binary search implementation"
```

### Generate code
```bash
think generate "create a REST API endpoint" --language python
```

### Analyze code
```bash
think analyze mycode.py
```

### Interactive mode
```bash
think interactive
```

## Examples

```bash
# Add a code snippet
think add --code "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)" \
         --language python \
         --description "Recursive Fibonacci"

# Search for similar patterns
think search "fibonacci sequence"

# Generate new code based on examples
think generate "iterative fibonacci function" --language python
```

## Requirements

- Python 3.8+
- No GPU required (CPU-optimized)
- Works on all platforms (Windows, macOS, Linux)
- O(1) vector search included

## Integration with Think AI System

### Connect to Railway Deployment

```bash
# Configure CLI to use your Railway instance
think config set api_url https://your-app.railway.app/api/v1
think config set api_key YOUR_API_KEY

# Use remote consciousness engine
think generate "implement OAuth2 flow" --remote
```

### Local Development Setup

```bash
# Start local Think AI system
python process_manager.py

# Configure CLI for local use
think config set api_url http://localhost:8080/api/v1

# Test connection
think test-connection
```

## Advanced Features

### O(1) Performance Mode

```python
from think_ai_cli import ThinkCLI
from o1_vector_search import O1VectorSearch

# Initialize with O(1) search
cli = ThinkCLI(vector_search=O1VectorSearch(dim=384))

# Benchmark performance
cli.benchmark(iterations=1000)
```

### Knowledge Base Management

```bash
# Export your knowledge base
think export --format json --output knowledge_base.json

# Import knowledge base
think import --input knowledge_base.json

# Sync with Think AI cloud
think sync --merge-strategy newest
```

### Code Intelligence Features

```bash
# Deep code analysis
think analyze --directory ./src --recursive --report analysis.html

# Security scanning
think security scan --severity high ./src

# Generate comprehensive tests
think test generate --file app.py --framework pytest --coverage 90

# Code refactoring suggestions
think refactor suggest --file legacy_code.py
```

### Batch Operations

```bash
# Process multiple files
think batch add --directory ./examples --pattern "*.py"

# Bulk search
think batch search --queries queries.txt --output results.json

# Mass code generation
think batch generate --specs specifications.yaml
```

## Configuration

Create `.thinkairc` in your home directory:

```yaml
api:
  url: http://localhost:8080/api/v1
  timeout: 30
  retry: 3

search:
  engine: o1  # Use O(1) search
  dimensions: 384
  num_results: 10

output:
  format: rich  # rich, plain, json
  syntax_highlighting: true
  pager: true

knowledge_base:
  path: ~/.think-ai/knowledge
  auto_sync: true
  compression: true
```

## Docker Support

```dockerfile
# Included in Think AI Docker image
FROM devsarmico/think-ai-base:optimized
# think-ai-cli pre-installed with all features
```

## Troubleshooting

### Common Issues

1. **ImportError with vector search**
   ```bash
   # Use O(1) implementation
   pip install think-ai-cli[o1] --upgrade
   ```

2. **Connection refused**
   ```bash
   # Check if Think AI is running
   think health-check
   ```

3. **Slow search performance**
   ```bash
   # Switch to O(1) mode
   think config set search.engine o1
   ```

## Contributing

See the [main Think AI repository](https://github.com/champi-dev/think_ai) for contribution guidelines.

## Support

- Issues: [GitHub Issues](https://github.com/champi-dev/think_ai/issues)
- Docs: [CLI Documentation](https://github.com/champi-dev/think_ai/tree/main/docs/cli)
- Community: [Discussions](https://github.com/champi-dev/think_ai/discussions)

## License

MIT - Part of Think AI by Daniel "Champi" Sarcos