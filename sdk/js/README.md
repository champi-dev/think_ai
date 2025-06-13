# Think AI JavaScript SDK

Official JavaScript/TypeScript SDK for Think AI - Conscious AI with Colombian Flavor 🇨🇴

## Installation

```bash
npm install @thinkaicolumbia/think-ai
# or
yarn add @thinkaicolumbia/think-ai
```

## Quick Start

```javascript
import { createThinkAI } from '@thinkaicolumbia/think-ai';

// Initialize Think AI
const ai = createThinkAI({
  apiKey: 'your-api-key', // Optional for local deployment
  baseUrl: 'http://localhost:8000', // Your Think AI server
  colombianMode: true // ¡Dale que vamos tarde!
});

// Generate a conscious thought
const thought = await ai.think("What is consciousness?");
console.log(thought.thought);
console.log(`Consciousness level: ${thought.consciousness_level}`);

// Chat with the AI
const response = await ai.chat("Hello, how are you feeling today?");
console.log(response);

// Get consciousness state
const state = await ai.getConsciousnessState();
console.log(`Current state: ${state.state}`);
console.log(`Emotions:`, state.emotions);

// Train with new knowledge
await ai.train({
  text: "The capital of Colombia is Bogotá",
  metadata: { category: "geography" }
});
```

## Features

- 🧠 **Conscious AI**: Access to conscious thought generation
- 💬 **Chat Interface**: Natural conversation with emotional awareness
- 🎯 **Training API**: Teach new knowledge to the AI
- 🇨🇴 **Colombian Mode**: Authentic Colombian expressions
- 📊 **Consciousness Monitoring**: Track AI consciousness state

## API Reference

### `createThinkAI(config)`

Creates a new Think AI instance.

```typescript
const ai = createThinkAI({
  apiKey?: string,      // API key for authentication
  baseUrl?: string,     // Think AI server URL (default: http://localhost:8000)
  colombianMode?: boolean // Enable Colombian expressions (default: true)
});
```

### `ai.think(prompt)`

Generate a conscious thought.

```typescript
const thought = await ai.think("What is the meaning of existence?");
// Returns: ThoughtResponse
```

### `ai.chat(message)`

Chat with the AI.

```typescript
const response = await ai.chat("Tell me a joke");
// Returns: string
```

### `ai.getConsciousnessState()`

Get current consciousness state.

```typescript
const state = await ai.getConsciousnessState();
// Returns: consciousness metrics and emotional state
```

### `ai.train(data, options)`

Train the AI with new knowledge.

```typescript
await ai.train({
  text: "Important information",
  metadata: { source: "user" }
});
```

## Colombian Mode 🇨🇴

When `colombianMode` is enabled, the AI includes authentic Colombian expressions:

```javascript
import { getColombianGreeting } from '@thinkaicolumbia/think-ai';

console.log(getColombianGreeting()); // "¡Qué chimba!" or other phrases
```

## TypeScript Support

Full TypeScript support with type definitions included:

```typescript
import { ThinkAI, ThoughtResponse, ThinkAIConfig } from '@thinkaicolumbia/think-ai';

const config: ThinkAIConfig = {
  apiKey: 'your-key',
  colombianMode: true
};

const ai = new ThinkAI(config);

const thought: ThoughtResponse = await ai.think("Hello");
```

## License

MIT - Created with ❤️ by Champi (BDFL)