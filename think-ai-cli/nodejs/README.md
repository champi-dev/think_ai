# Think AI CLI (Node.js)

AI-powered coding assistant with vector search capabilities. No native dependencies required!

## Installation

```bash
npm install -g think-ai-cli
```

Or use with npx:
```bash
npx think-ai-cli search "binary search implementation"
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
- **vectordb** - Pure JavaScript vector database
- **Web-compatible models** - All models run in pure JavaScript