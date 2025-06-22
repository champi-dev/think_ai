# Think AI CLI (Node.js)

**Version:** 0.2.0 | **Last Updated:** December 22, 2024

AI-powered coding assistant with O(1) vector search capabilities. Part of the Think AI superintelligent consciousness system. No native dependencies required!

## Installation

```bash
npm install -g @think-ai/cli
```

Or use with npx:
```bash
npx @think-ai/cli search "binary search implementation"
```

### Alternative installation methods:
```bash
# From Think AI monorepo
git clone https://github.com/champi-dev/think_ai.git
cd think_ai/think-ai-cli/nodejs
npm install -g .

# Legacy package name (deprecated)
npm install -g think-ai-cli
```

## Features

- 🔍 **Semantic Code Search** - Find similar code patterns using AI
- 🚀 **Code Generation** - Generate code from natural language prompts  
- 📊 **Code Analysis** - Analyze code for patterns and improvements
- 💾 **Local Knowledge Base** - Build your own code snippet database
- 🎨 **Beautiful CLI** - Colorful terminal output
- 🌐 **No Native Dependencies** - Pure JavaScript, works everywhere

## Usage

### Search for code patterns
```bash
think search "implement binary search"
```

### Add code to knowledge base
```bash
think add --file example.js --language javascript --description "Binary search implementation"
```

### Generate code
```bash
think generate "create a REST API endpoint" --language javascript
```

### Interactive mode
```bash
think interactive
```

## Examples

```bash
# Add a code snippet
think add --code "const fibonacci = n => n <= 1 ? n : fibonacci(n-1) + fibonacci(n-2)" \
         --language javascript \
         --description "Recursive Fibonacci"

# Search for similar patterns
think search "fibonacci sequence"

# Generate new code based on examples
think generate "iterative fibonacci function" --language javascript
```

## Requirements

- Node.js 16+
- No GPU required
- No native compilation needed
- Works on all platforms (Windows, macOS, Linux)

## How it works

This CLI uses:
- **@xenova/transformers** - ONNX-based embeddings (no Python/C++ required)
- **o1-js** - O(1) vector search implementation
- **Web-compatible models** - All models run in pure JavaScript
- **Think AI Core** - Consciousness-driven code understanding

## Integration with Think AI System

### Using with Think AI API

```bash
# Set API endpoint (if self-hosted)
export THINK_AI_API_URL=https://your-think-ai.railway.app

# Use enhanced features
think search "implement authentication" --enhanced
```

### Railway Deployment

The CLI can connect to your Railway-deployed Think AI instance:

```bash
# Configure for production
think config set api.url https://your-app.railway.app/api/v1
think config set api.key YOUR_API_KEY

# Use remote consciousness engine
think generate "create OAuth2 flow" --remote
```

## Advanced Features

### O(1) Performance Mode

```bash
# Enable O(1) search (default)
think config set search.mode o1

# Benchmark search performance
think benchmark --iterations 1000
```

### Knowledge Base Management

```bash
# Export knowledge base
think export --output knowledge.json

# Import knowledge base
think import --input knowledge.json

# Sync with Think AI cloud
think sync --merge
```

### Code Intelligence

```bash
# Analyze code patterns
think analyze --directory ./src --report

# Find security issues
think security --scan ./src

# Generate tests
think test --file app.js --framework jest
```

## Configuration

Create `.thinkairc` in your project:

```json
{
  "search": {
    "mode": "o1",
    "dimensions": 384,
    "hashTables": 10
  },
  "api": {
    "url": "http://localhost:8080/api/v1",
    "timeout": 30000
  },
  "output": {
    "format": "pretty",
    "colors": true
  }
}
```

## Contributing

See the [main Think AI repository](https://github.com/champi-dev/think_ai) for contribution guidelines.

## Support

- Issues: [GitHub Issues](https://github.com/champi-dev/think_ai/issues)
- Docs: [CLI Documentation](https://github.com/champi-dev/think_ai/tree/main/docs/cli)
- Community: [Discussions](https://github.com/champi-dev/think_ai/discussions)

## License

MIT - Part of Think AI by Daniel "Champi" Sarcos