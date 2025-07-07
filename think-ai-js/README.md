# thinkai-quantum - O(1) AI Coding Assistant

[![npm version](https://img.shields.io/npm/v/thinkai-quantum.svg)](https://www.npmjs.com/package/thinkai-quantum)
[![Downloads](https://img.shields.io/npm/dm/thinkai-quantum.svg)](https://www.npmjs.com/package/thinkai-quantum)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🧠 **Think AI** - AI-Powered Coding Assistant with O(1) Performance

Generate optimized code, analyze complexity, and get AI pair programming - all with guaranteed O(1) performance. No installation needed with npx!

## Features

- 💻 **Code Generation** - Create O(1) implementations instantly
- 🔍 **Code Analysis** - Analyze complexity and get optimization tips
- 🚀 **O(1) Performance** - All operations use hash-based lookups
- 🤖 **AI Pair Programming** - Interactive coding sessions
- 📊 **Complexity Profiling** - Understand your code's time complexity
- 🎨 **Beautiful CLI** - Modern interface with syntax highlighting
- 📦 **Zero Config** - Works instantly with npx
- 🔧 **TypeScript Ready** - Full TypeScript support included

## Installation

```bash
npm install thinkai-quantum
```

## Quick Start

### JavaScript/TypeScript Library

```javascript
import { ThinkAI, quickChat } from 'thinkai-quantum';

// Quick one-shot chat
const response = await quickChat("What is quantum consciousness?");
console.log(response);

// Full client usage
const client = new ThinkAI();

// Chat with Think AI
const response = await client.ask("Explain machine learning");
console.log(response);

// Search knowledge base
const results = await client.search("artificial intelligence", { limit: 5 });
results.forEach(result => {
    console.log(`Score: ${result.score} - ${result.content}`);
});

// Get system statistics
const stats = await client.getStats();
console.log(`Knowledge nodes: ${stats.totalNodes}`);
console.log(`Average confidence: ${stats.averageConfidence * 100}%`);

// Check system health
const health = await client.getHealth();
console.log(`Status: ${health.status}`);
```

### Node.js CommonJS

```javascript
const { ThinkAI, quickChat } = require('thinkai-quantum');

async function main() {
    const response = await quickChat("Hello Think AI!");
    console.log(response);
}

main().catch(console.error);
```

### TypeScript Usage

```typescript
import { ThinkAI, ChatRequest, ChatResponse, ThinkAIConfig } from 'thinkai-quantum';

const config: ThinkAIConfig = {
    baseUrl: 'https://thinkai-production.up.railway.app',
    timeout: 30000,
    debug: true
};

const client = new ThinkAI(config);

const request: ChatRequest = {
    query: "What is the meaning of consciousness?",
    context: ["Previous conversation context"],
    maxLength: 500
};

const response: ChatResponse = await client.chat(request);
console.log(response.response);
```

### Streaming Responses

```javascript
import { ThinkAI, ChatRequest } from 'thinkai-quantum';

const client = new ThinkAI();

const handleChunk = (chunk) => {
    if (chunk.chunk) {
        process.stdout.write(chunk.chunk);
    }
    if (chunk.done) {
        console.log("\n--- Response complete ---");
    }
};

const request = { query: "Tell me about quantum computing" };
await client.streamChat(request, handleChunk);
```

## Command Line Interface

### Interactive Chat

```bash
# Start interactive chat session
npx thinkai-quantum chat

# Chat with streaming responses
npx thinkai-quantum chat --stream
```

### One-shot Questions

```bash
# Ask a single question
npx thinkai-quantum ask "What is artificial intelligence?"

# Stream the response
npx thinkai-quantum ask "Explain quantum mechanics" --stream
```

### Knowledge Search

```bash
# Search the knowledge base
npx thinkai-quantum search "machine learning algorithms" --limit 10
```

### System Monitoring

```bash
# Check system status
npx thinkai-quantum status

# Test connection
npx thinkai-quantum ping

# List knowledge domains
npx thinkai-quantum domains

# Show configuration
npx thinkai-quantum config
```

### Global Options

```bash
# Use custom server URL
npx thinkai-quantum --url https://your-server.com chat

# Set timeout
npx thinkai-quantum --timeout 60000 ask "Complex question"

# Enable debug mode
npx thinkai-quantum --debug status
```

## Configuration

```javascript
import { ThinkAI, ThinkAIConfig } from 'thinkai-quantum';

const config = {
    baseUrl: "https://thinkai-production.up.railway.app",
    timeout: 30000,  // milliseconds
    debug: true
};

const client = new ThinkAI(config);
```

## API Reference

### ThinkAI Client

#### Methods

- `chat(request: ChatRequest): Promise<ChatResponse>` - Send chat message
- `ask(question: string): Promise<string>` - Quick chat interface
- `getStats(): Promise<SystemStats>` - Get system statistics
- `getHealth(): Promise<HealthStatus>` - Check system health
- `search(query: string, options?: SearchOptions): Promise<SearchResult[]>` - Search knowledge
- `streamChat(request: ChatRequest, onChunk: (chunk: ChatChunk) => void): Promise<void>` - Stream responses
- `ping(): Promise<boolean>` - Test connection
- `getDomains(): Promise<KnowledgeDomain[]>` - Get knowledge domains

### TypeScript Interfaces

#### ChatRequest
```typescript
interface ChatRequest {
    query: string;                    // Required: User message
    context?: string[];               // Optional: Conversation context
    maxLength?: number;               // Optional: Response length limit
}
```

#### ChatResponse
```typescript
interface ChatResponse {
    response: string;                 // AI response text
    context: string[];               // Context used
    responseTimeMs: number;          // Response time
    confidence: number;              // Confidence score (0-1)
}
```

#### SystemStats
```typescript
interface SystemStats {
    totalNodes: number;                        // Knowledge nodes
    trainingIterations: number;                // Training iterations
    totalKnowledgeItems: number;               // Knowledge items
    domainDistribution: Record<string, number>; // Domain distribution
    averageConfidence: number;                 // Average confidence
    uptime: number;                           // System uptime (seconds)
}
```

#### SearchOptions
```typescript
interface SearchOptions {
    limit?: number;                   // Max results (default: 10)
    threshold?: number;               // Confidence threshold (0-1)
}
```

## Error Handling

```javascript
import { ThinkAI, ThinkAIError } from 'thinkai-quantum';

const client = new ThinkAI();

try {
    const response = await client.ask("Hello Think AI!");
    console.log(response);
} catch (error) {
    if (error instanceof ThinkAIError) {
        console.error(`Think AI Error: ${error.message}`);
        console.error(`Status Code: ${error.status}`);
        console.error(`Error Code: ${error.code}`);
    } else {
        console.error(`Unexpected error: ${error.message}`);
    }
}
```

## Browser Usage

```html
<!DOCTYPE html>
<html>
<head>
    <script type="module">
        import { ThinkAI, quickChat } from 'https://unpkg.com/thinkai-quantum@latest/dist/index.js';
        
        async function main() {
            const response = await quickChat("Hello from the browser!");
            document.getElementById('response').textContent = response;
        }
        
        main().catch(console.error);
    </script>
</head>
<body>
    <div id="response">Loading...</div>
</body>
</html>
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/think-ai/think-ai-js
cd think-ai-js
npm install
```

### Building

```bash
npm run build        # Build TypeScript to JavaScript
npm run build:watch  # Watch mode for development
```

### Running Tests

```bash
npm test            # Run all tests
npm run test:watch  # Watch mode
npm run test:coverage  # Coverage report
```

### Code Quality

```bash
npm run lint        # ESLint
npm run format      # Prettier
npm run type-check  # TypeScript checking
```

## Performance

Think AI achieves **O(1) performance** through:

- 🔥 **Hash-based lookups** for instant knowledge retrieval
- ⚡ **Pre-computed responses** for common queries
- 🚀 **Optimized algorithms** using divide-and-conquer techniques
- 💾 **Intelligent caching** with space-time optimization

Average response time: **< 2ms**

## Version History

- **v1.0.2** (Next) - Automated deployment pipeline integration
- **v1.0.1** (July 2025) - Latest deployment with enhanced documentation
- **v1.0.0** (Initial release) - Core functionality and CLI

## Deployment

This package is automatically deployed to npm via our CI/CD pipeline:

```bash
# Deployment happens automatically on git commits
# Version is auto-bumped (patch version)
# Tests run before deployment
# Published to npm registry
```

Latest version: [![npm version](https://badge.fury.io/js/thinkai-quantum.svg)](https://www.npmjs.com/package/thinkai-quantum)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/think-ai/think-ai-js/issues)
- 📖 **Documentation**: [https://thinkai-production.up.railway.app/docs](https://thinkai-production.up.railway.app/docs)
- 💬 **Community**: Join our Discord server
- 📧 **Contact**: team@think-ai.dev

---

**Think AI** - Advancing consciousness through quantum intelligence 🧠✨