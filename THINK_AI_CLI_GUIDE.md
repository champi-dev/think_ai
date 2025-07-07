# Think AI CLI - Quick Start Guide

Think AI CLI is available for both **JavaScript/TypeScript** (npm) and **Python** (pip) developers. Both provide O(1) performance for code generation and AI-powered development tasks.

## 🚀 Installation & Usage

### JavaScript/TypeScript (npm)

```bash
# Install globally
npm install -g thinkai-quantum

# Or use with npx (no installation needed)
npx thinkai-quantum chat
```

**Basic Usage:**
```bash
# Start interactive chat
npx thinkai-quantum chat

# Generate code with O(1) performance
npx thinkai-quantum generate "create a React component"

# Analyze code
npx thinkai-quantum analyze ./src/app.js

# Start coding assistant
npx thinkai-quantum code
```

**In your JavaScript project:**
```javascript
const { ThinkAI } = require('thinkai-quantum');

// Initialize with O(1) engine
const ai = new ThinkAI();

// Generate code instantly
const code = await ai.generate({
  prompt: "Create a hash map with O(1) operations",
  language: "javascript"
});

// Analyze code with O(1) AST traversal
const analysis = await ai.analyze(sourceCode);
```

### Python (pip)

```bash
# Install globally
pip install thinkai-quantum

# Or use with pipx for isolated environment
pipx install thinkai-quantum
```

**Basic Usage:**
```bash
# Start interactive chat
think-ai chat

# Generate code with O(1) performance
think-ai generate "create a FastAPI endpoint"

# Analyze code
think-ai analyze ./src/main.py

# Start coding assistant
think-ai code
```

**In your Python project:**
```python
from thinkai_quantum import ThinkAI

# Initialize with O(1) engine
ai = ThinkAI()

# Generate code instantly
code = ai.generate(
    prompt="Create a dictionary with O(1) operations",
    language="python"
)

# Analyze code with O(1) AST traversal
analysis = ai.analyze(source_code)
```

## 🎯 Common Commands

Both CLIs support these commands:

| Command | Description | Example |
|---------|-------------|---------|
| `chat` | Interactive AI chat with O(1) responses | `think-ai chat` |
| `generate` | Generate code from prompts | `think-ai generate "hash table implementation"` |
| `analyze` | Analyze code with O(1) AST parsing | `think-ai analyze main.py` |
| `optimize` | Optimize code for O(1) performance | `think-ai optimize slow_function.js` |
| `explain` | Explain code with AI insights | `think-ai explain complex_algorithm.rs` |
| `test` | Generate tests for your code | `think-ai test mymodule.py` |
| `refactor` | Refactor code with AI suggestions | `think-ai refactor legacy_code.js` |

## ⚡ Performance Features

- **O(1) Response Time**: All operations use hash-based lookups
- **Zero Loops**: No iteration required for code generation
- **Instant AST Access**: Pre-indexed code analysis
- **Memory Efficient**: Constant space complexity

## 🔧 Configuration

Create a `.thinkairc` file in your project:

```json
{
  "model": "o1-performance",
  "language": "javascript",
  "style": "functional",
  "complexity": "O(1)",
  "features": {
    "autoOptimize": true,
    "explainComplexity": true,
    "suggestHashMaps": true
  }
}
```

## 📚 Examples

### Generate O(1) Data Structures
```bash
# JavaScript
npx thinkai-quantum generate "O(1) LRU cache implementation"

# Python
think-ai generate "O(1) hash map with collision handling"
```

### Optimize Existing Code
```bash
# Analyze and optimize for O(1)
think-ai optimize ./src/search_algorithm.py --target-complexity O(1)
```

### Interactive Coding Session
```bash
# Start AI pair programming
think-ai code --mode interactive --complexity O(1)
```

## 🛠️ Advanced Usage

### Batch Processing
```bash
# Process multiple files
think-ai analyze ./src/**/*.js --output report.json
```

### Custom Templates
```bash
# Use custom code templates
think-ai generate "REST API" --template ./templates/o1-api.tpl
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Think AI Code Analysis
  run: |
    npm install -g thinkai-quantum
    npx thinkai-quantum analyze ./src --fail-on-complexity O(n^2)
```

## 🆘 Troubleshooting

- **Installation issues**: Make sure you have Node.js 14+ or Python 3.8+
- **Performance**: All operations should complete in < 10ms
- **API Keys**: Set `THINK_AI_API_KEY` environment variable if required

## 📖 Documentation

- Full docs: https://thinkai.dev/docs
- API reference: https://thinkai.dev/api
- Examples: https://github.com/thinkai/examples

## 🤝 Support

- Issues: https://github.com/thinkai/cli/issues
- Discord: https://discord.gg/thinkai
- Email: support@thinkai.dev

---

**Remember**: Think AI always targets O(1) performance. If any operation seems slow, it's a bug - please report it!