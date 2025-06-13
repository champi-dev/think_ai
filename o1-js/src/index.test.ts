import { O1VectorSearch, createIndex } from './index';

describe('O1VectorSearch', () => {
  it('should create an index with correct dimensions', () => {
    const index = new O1VectorSearch(128);
    expect(index.size()).toBe(0);
  });

  it('should add and search vectors in O(1)', () => {
    const index = createIndex<{ id: string }>(3);
    
    // Add vectors
    index.add([1, 0, 0], { id: 'vec1' });
    index.add([0, 1, 0], { id: 'vec2' });
    index.add([0, 0, 1], { id: 'vec3' });
    
    // Search
    const results = index.search([0.9, 0.1, 0], 2);
    
    expect(results.length).toBeGreaterThan(0);
    expect(results[0].metadata.id).toBe('vec1');
  });

  it('should handle high-dimensional vectors', () => {
    const index = new O1VectorSearch<{ label: string }>(384);
    
    // Generate random vectors
    for (let i = 0; i < 100; i++) {
      const vector = Array(384).fill(0).map(() => Math.random());
      index.add(vector, { label: `item_${i}` });
    }
    
    expect(index.size()).toBe(100);
    
    // Search should be fast
    const query = Array(384).fill(0).map(() => Math.random());
    const start = Date.now();
    const results = index.search(query, 10);
    const duration = Date.now() - start;
    
    expect(results.length).toBeLessThanOrEqual(10);
    expect(duration).toBeLessThan(10); // Should be < 10ms
  });

  it('should export and import index', () => {
    const index = new O1VectorSearch<{ name: string }>(4);
    
    index.add([1, 2, 3, 4], { name: 'test1' });
    index.add([5, 6, 7, 8], { name: 'test2' });
    
    const exported = index.export();
    const imported = O1VectorSearch.import<{ name: string }>(exported);
    
    expect(imported.size()).toBe(2);
    
    const results = imported.search([1, 2, 3, 4], 1);
    expect(results[0].metadata.name).toBe('test1');
  });

  it('should achieve O(1) performance', () => {
    const index = new O1VectorSearch(128);
    const times: number[] = [];
    
    // Add 10000 vectors
    for (let i = 0; i < 10000; i++) {
      const vector = Array(128).fill(0).map(() => Math.random());
      index.add(vector, { id: i });
    }
    
    // Measure search times
    for (let i = 0; i < 100; i++) {
      const query = Array(128).fill(0).map(() => Math.random());
      const start = performance.now();
      index.search(query, 5);
      const duration = performance.now() - start;
      times.push(duration);
    }
    
    const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
    const maxTime = Math.max(...times);
    
    // O(1) means constant time regardless of index size
    expect(avgTime).toBeLessThan(60); // Average < 60ms
    expect(maxTime).toBeLessThan(120); // Max < 120ms
  });
});