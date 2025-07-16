# Think AI JavaScript/TypeScript Library

Official JavaScript/TypeScript SDK for interacting with the Think AI API.

## Installation

```bash
npm install thinkai-quantum
# or
yarn add thinkai-quantum
# or
pnpm add thinkai-quantum
```

## Quick Start

```javascript
const { ThinkAI } = require('thinkai-quantum');

// Initialize client
const ai = new ThinkAI({
  baseUrl: 'https://thinkai.lat', // or your self-hosted instance
  apiKey: 'your-api-key' // optional, for future use
});

// Send a message
const response = await ai.query('What is consciousness?');
console.log(response);
```

## TypeScript Usage

```typescript
import { ThinkAI } from 'thinkai-quantum';

const ai = new ThinkAI();

// Full typed response
const response = await ai.chat({
  message: 'Explain quantum computing',
  mode: 'general',
  sessionId: 'user-123'
});

console.log(response.response);
console.log(`Confidence: ${response.confidence}`);
```

## CLI Usage

Interactive chat interface:

```bash
npx thinkai-quantum chat
```

Single query:

```bash
npx thinkai-quantum query "What is the meaning of life?"
```

## Features

- 🚀 **O(1) Performance**: Leverages Think AI's quantum-inspired algorithms
- 🌊 **Streaming Support**: Real-time response streaming
- 🔌 **WebSocket**: Bi-directional communication
- 💾 **Session Management**: Persistent conversations
- 📊 **Rich Metadata**: Confidence scores, consciousness levels, and more
- 🎯 **TypeScript**: Full type definitions included

## API Reference

### Initialize Client

```javascript
const ai = new ThinkAI({
  baseUrl: 'https://thinkai.lat',  // API endpoint
  timeout: 30000,                  // Request timeout (ms)
  retries: 3                       // Retry attempts
});
```

### Chat Methods

#### Basic Query

```javascript
// Simple query
const response = await ai.query('Hello, AI!');

// With options
const response = await ai.chat({
  message: 'Write a Python function',
  mode: 'code',
  sessionId: 'session-123',
  useWebSearch: false,
  factCheck: false
});
```

#### Streaming Responses

```javascript
const stream = await ai.stream('Tell me a long story');

stream.on('chunk', (text) => {
  process.stdout.write(text);
});

stream.on('done', (metadata) => {
  console.log('\nComplete!', metadata);
});
```

### Session Management

```javascript
// Create a session
const session = ai.createSession();

// Query with session
const response = await session.query('My name is Alice');

// Session remembers context
const followUp = await session.query('What is my name?');
console.log(followUp); // Will remember "Alice"

// Get session history
const history = session.getHistory();
```

### Advanced Features

#### Code Mode

```javascript
const codeResponse = await ai.chat({
  message: 'Implement quicksort in Rust',
  mode: 'code'
});
```

#### Web Search Integration

```javascript
const searchResponse = await ai.chat({
  message: 'Latest developments in quantum computing',
  useWebSearch: true
});
```

#### Fact Checking

```javascript
const factResponse = await ai.chat({
  message: 'The Earth is flat',
  factCheck: true
});
```

## Examples

### Basic Conversation

```javascript
const { ThinkAI } = require('thinkai-quantum');

async function main() {
  const ai = new ThinkAI();
  const session = ai.createSession();
  
  // Start conversation
  console.log(await session.query("Hello! I'm learning about AI."));
  
  // Continue with context
  console.log(await session.query("What should I learn first?"));
  
  // Get recommendations
  console.log(await session.query("Can you recommend some resources?"));
}

main().catch(console.error);
```

### Real-time Chat Application

```javascript
const express = require('express');
const { ThinkAI } = require('thinkai-quantum');

const app = express();
const ai = new ThinkAI();

app.post('/chat', express.json(), async (req, res) => {
  const { message, sessionId } = req.body;
  
  // Stream response
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
  });
  
  const stream = await ai.stream(message, { sessionId });
  
  stream.on('chunk', (chunk) => {
    res.write(`data: ${JSON.stringify({ chunk })}\n\n`);
  });
  
  stream.on('done', () => {
    res.write('data: [DONE]\n\n');
    res.end();
  });
});

app.listen(3000);
```

### CLI Tool

```javascript
#!/usr/bin/env node
const { ThinkAI } = require('thinkai-quantum');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const ai = new ThinkAI();
const session = ai.createSession();

console.log('🧠 Think AI CLI - Type "exit" to quit\n');

function prompt() {
  rl.question('You: ', async (input) => {
    if (input.toLowerCase() === 'exit') {
      rl.close();
      return;
    }
    
    console.log('AI: ', await session.query(input));
    prompt();
  });
}

prompt();
```

## Error Handling

```javascript
try {
  const response = await ai.query('Hello');
} catch (error) {
  if (error.code === 'RATE_LIMITED') {
    console.log('Too many requests, please wait');
  } else if (error.code === 'NETWORK_ERROR') {
    console.log('Connection failed');
  } else {
    console.error('Unexpected error:', error);
  }
}
```

## Configuration

### Environment Variables

```bash
THINKAI_API_URL=https://thinkai.lat
THINKAI_API_KEY=your-api-key
THINKAI_TIMEOUT=30000
```

### Custom Configuration

```javascript
const ai = new ThinkAI({
  // Custom retry logic
  retry: {
    attempts: 5,
    delay: (attempt) => Math.pow(2, attempt) * 1000
  },
  
  // Request interceptor
  beforeRequest: (config) => {
    console.log('Request:', config);
    return config;
  },
  
  // Response interceptor
  afterResponse: (response) => {
    console.log('Response:', response);
    return response;
  }
});
```

## Browser Support

### CDN

```html
<script src="https://unpkg.com/thinkai-quantum/dist/browser.min.js"></script>
<script>
  const ai = new ThinkAI();
  ai.query('Hello from browser!').then(console.log);
</script>
```

### ES Modules

```javascript
import { ThinkAI } from 'https://unpkg.com/thinkai-quantum/dist/browser.mjs';

const ai = new ThinkAI();
```

## Contributing

See the main [Contributing Guide](../CONTRIBUTING.md).

## Author

- **champi-dev** - [danielsarcor@gmail.com](mailto:danielsarcor@gmail.com)
- GitHub: [https://github.com/champi-dev/think_ai](https://github.com/champi-dev/think_ai)

## License

MIT License - see [LICENSE](../LICENSE) for details.