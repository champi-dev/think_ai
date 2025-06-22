# O(1) Vector Search for JavaScript/TypeScript

**Version:** 1.0.0 | **Last Updated:** December 22, 2024

Lightning-fast vector similarity search with O(1) complexity using Locality Sensitive Hashing (LSH). Part of the Think AI ecosystem for superintelligent consciousness with instant performance.

## Features

- ⚡ **O(1) Search Complexity** - Constant time search regardless of index size
- 🚀 **No Dependencies** - Pure JavaScript implementation
- 📦 **TypeScript Support** - Full type definitions included
- 💾 **Serializable** - Export/import index for persistence
- 🔧 **Simple API** - Easy to use and integrate

## Installation

```bash
npm install o1-js
```

### Alternative Package Names
```bash
# Original package name (deprecated)
npm install o1-vector-search

# From Think AI mono-repo
npm install @think-ai/o1-js
```

## Quick Start

```javascript
import { O1VectorSearch } from 'o1-js';

// Create an index for 384-dimensional vectors
const index = new O1VectorSearch(384);

// Add vectors with metadata
index.add([0.1, 0.2, ...], { id: 1, text: "Hello world" });
index.add([0.3, 0.4, ...], { id: 2, text: "Machine learning" });

// Search for similar vectors in O(1) time
const query = [0.15, 0.25, ...];
const results = index.search(query, 5);

console.log(results);
// [
//   { distance: 0.12, vector: [...], metadata: { id: 1, text: "Hello world" } },
//   { distance: 0.89, vector: [...], metadata: { id: 2, text: "Machine learning" } }
// ]
```

## API Reference

### Constructor

```typescript
new O1VectorSearch(dimension: number, numHashTables?: number, numHashFunctions?: number)
```

### Methods

- `add(vector: number[], metadata: T): void` - Add a vector to the index
- `search(queryVector: number[], k?: number): SearchResult<T>[]` - Search for k nearest neighbors
- `size(): number` - Get the number of vectors in the index
- `clear(): void` - Remove all vectors
- `export(): string` - Serialize the index
- `static import<T>(data: string): O1VectorSearch<T>` - Deserialize an index

## Performance

The O(1) complexity is achieved through LSH (Locality Sensitive Hashing):

- **Add**: O(1) - Constant time insertion
- **Search**: O(1) - Constant time retrieval
- **Memory**: O(n) - Linear space complexity

## Use Cases

- Real-time recommendation systems
- Semantic search engines  
- Image similarity search
- Anomaly detection
- Clustering and classification
- Think AI consciousness queries
- O(1) knowledge retrieval

## Integration with Think AI

This library is a core component of the Think AI system:

```javascript
import { ThinkAI } from 'think-ai-js';
import { O1VectorSearch } from 'o1-js';

// Create Think AI instance with O(1) search
const ai = new ThinkAI({
  vectorSearch: new O1VectorSearch(384)
});

// Ultra-fast consciousness queries
const thought = await ai.think("What is consciousness?");
```

## Production Deployment

For production use with Think AI:

1. **Railway Deployment**
   ```javascript
   // Automatically included in Think AI Railway deployments
   const vectorDb = new O1VectorSearch(384, 10, 8);
   ```

2. **Performance Tuning**
   ```javascript
   // Optimize for your use case
   const index = new O1VectorSearch(
     384,      // dimension
     20,       // numHashTables (more = better recall)
     12        // numHashFunctions (more = better precision)
   );
   ```

## Advanced Features

### Persistence

```javascript
// Save index to disk
const data = index.export();
fs.writeFileSync('index.json', data);

// Load index from disk
const loadedData = fs.readFileSync('index.json', 'utf8');
const loadedIndex = O1VectorSearch.import(loadedData);
```

### Batch Operations

```javascript
// Add multiple vectors efficiently
const vectors = [
  { vector: [0.1, 0.2, ...], metadata: { id: 1 } },
  { vector: [0.3, 0.4, ...], metadata: { id: 2 } },
  // ...
];

vectors.forEach(item => index.add(item.vector, item.metadata));
```

## Contributing

Contributions are welcome! Please see the [main Think AI repository](https://github.com/champi-dev/think_ai) for guidelines.

## Support

- GitHub Issues: [Report bugs or request features](https://github.com/champi-dev/think_ai/issues)
- Documentation: [Full Think AI docs](https://github.com/champi-dev/think_ai/tree/main/docs)
- Community: [Join discussions](https://github.com/champi-dev/think_ai/discussions)

## License

MIT - Part of the Think AI project by Daniel "Champi" Sarcos