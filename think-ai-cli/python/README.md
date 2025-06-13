# Think AI CLI

AI-powered coding assistant with vector search capabilities. Uses CPU-optimized vector search for maximum compatibility.

## Installation

```bash
pip install think-ai-cli
```

For environments without SWIG (like Vercel), use alternative vector search:
```bash
pip install think-ai-cli[annoy]  # Uses Annoy instead of FAISS
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