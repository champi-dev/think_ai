# O(1) Vector Search for JavaScript/TypeScript

Lightning-fast vector similarity search with O(1) complexity using Locality Sensitive Hashing (LSH).

## Features

- ⚡ **O(1) Search Complexity** - Constant time search regardless of index size
- 🚀 **No Dependencies** - Pure JavaScript implementation
- 📦 **TypeScript Support** - Full type definitions included
- 💾 **Serializable** - Export/import index for persistence
- 🔧 **Simple API** - Easy to use and integrate

## Installation

```bash
npm install o1-vector-search
```

## Quick Start

```javascript
import { O1VectorSearch } from 'o1-vector-search';

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

## License

MIT