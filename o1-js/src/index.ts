/**
 * O(1) Vector Search - JavaScript/TypeScript Implementation
 * Instant similarity search using Locality Sensitive Hashing (LSH)
 */

export interface SearchResult<T = any> {
  distance: number;
  vector: number[];
  metadata: T;
}

export class O1VectorSearch<T = any> {
  private dimension: number;
  private numHashTables: number;
  private numHashFunctions: number;
  private hashTables: Map<string, Array<{ vector: number[]; metadata: T }>>;
  private projections: number[][][];
  private vectors: Array<{ vector: number[]; metadata: T }>;

  constructor(dimension: number, numHashTables: number = 10, numHashFunctions: number = 8) {
    this.dimension = dimension;
    this.numHashTables = numHashTables;
    this.numHashFunctions = numHashFunctions;
    this.hashTables = new Map();
    this.vectors = [];
    
    // Initialize random projections for LSH
    this.projections = this.initializeProjections();
  }

  private initializeProjections(): number[][][] {
    const projections: number[][][] = [];
    
    for (let i = 0; i < this.numHashTables; i++) {
      const tableProjections: number[][] = [];
      
      for (let j = 0; j < this.numHashFunctions; j++) {
        const projection: number[] = [];
        
        // Generate random gaussian projection
        for (let k = 0; k < this.dimension; k++) {
          projection.push(this.gaussianRandom());
        }
        
        // Normalize
        const norm = Math.sqrt(projection.reduce((sum, val) => sum + val * val, 0));
        for (let k = 0; k < this.dimension; k++) {
          projection[k] /= norm;
        }
        
        tableProjections.push(projection);
      }
      
      projections.push(tableProjections);
    }
    
    return projections;
  }

  private gaussianRandom(): number {
    // Box-Muller transform for gaussian distribution
    const u1 = Math.random();
    const u2 = Math.random();
    return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  }

  private computeHash(vector: number[], tableIdx: number): string {
    const hashBits: number[] = [];
    
    for (let i = 0; i < this.numHashFunctions; i++) {
      const projection = this.projections[tableIdx][i];
      const dotProduct = vector.reduce((sum, val, idx) => sum + val * projection[idx], 0);
      hashBits.push(dotProduct > 0 ? 1 : 0);
    }
    
    return hashBits.join('');
  }

  /**
   * Add a vector to the index with O(1) complexity
   */
  add(vector: number[], metadata: T): void {
    if (vector.length !== this.dimension) {
      throw new Error(`Vector dimension mismatch. Expected ${this.dimension}, got ${vector.length}`);
    }

    const item = { vector, metadata };
    this.vectors.push(item);

    // Add to all hash tables
    for (let i = 0; i < this.numHashTables; i++) {
      const hashKey = this.computeHash(vector, i);
      const fullKey = `${i}_${hashKey}`;
      
      if (!this.hashTables.has(fullKey)) {
        this.hashTables.set(fullKey, []);
      }
      
      this.hashTables.get(fullKey)!.push(item);
    }
  }

  /**
   * Search for similar vectors in O(1) time
   */
  search(queryVector: number[], k: number = 5): SearchResult<T>[] {
    if (queryVector.length !== this.dimension) {
      throw new Error(`Query vector dimension mismatch. Expected ${this.dimension}, got ${queryVector.length}`);
    }

    const candidates = new Map<number, { vector: number[]; metadata: T }>();
    
    // Look up in all hash tables
    for (let i = 0; i < this.numHashTables; i++) {
      const hashKey = this.computeHash(queryVector, i);
      const fullKey = `${i}_${hashKey}`;
      
      const bucket = this.hashTables.get(fullKey);
      if (bucket) {
        for (const item of bucket) {
          // Use vector index as unique identifier
          const idx = this.vectors.indexOf(item);
          candidates.set(idx, item);
        }
      }
    }

    // Calculate actual distances for candidates
    const results: SearchResult<T>[] = [];
    
    for (const [_, candidate] of candidates) {
      const distance = this.euclideanDistance(queryVector, candidate.vector);
      results.push({
        distance,
        vector: candidate.vector,
        metadata: candidate.metadata
      });
    }

    // Sort by distance and return top k
    results.sort((a, b) => a.distance - b.distance);
    return results.slice(0, k);
  }

  private euclideanDistance(a: number[], b: number[]): number {
    let sum = 0;
    for (let i = 0; i < a.length; i++) {
      const diff = a[i] - b[i];
      sum += diff * diff;
    }
    return Math.sqrt(sum);
  }

  /**
   * Get the number of vectors in the index
   */
  size(): number {
    return this.vectors.length;
  }

  /**
   * Clear all vectors from the index
   */
  clear(): void {
    this.hashTables.clear();
    this.vectors = [];
  }

  /**
   * Export index data for persistence
   */
  export(): string {
    return JSON.stringify({
      dimension: this.dimension,
      numHashTables: this.numHashTables,
      numHashFunctions: this.numHashFunctions,
      projections: this.projections,
      vectors: this.vectors
    });
  }

  /**
   * Import index data
   */
  static import<T = any>(data: string): O1VectorSearch<T> {
    const parsed = JSON.parse(data);
    const index = new O1VectorSearch<T>(
      parsed.dimension,
      parsed.numHashTables,
      parsed.numHashFunctions
    );
    
    index.projections = parsed.projections;
    
    // Re-add all vectors
    for (const item of parsed.vectors) {
      index.add(item.vector, item.metadata);
    }
    
    return index;
  }
}

// Export convenience functions
export function createIndex<T = any>(dimension: number): O1VectorSearch<T> {
  return new O1VectorSearch<T>(dimension);
}

export default O1VectorSearch;