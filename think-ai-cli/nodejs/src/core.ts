import { pipeline } from '@xenova/transformers';
import { VectorDB } from 'vectordb';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as os from 'os';

interface CodeMetadata {
  language: string;
  description: string;
  tags: string[];
  length: number;
}

interface SearchResult {
  score: number;
  code: string;
  metadata: CodeMetadata;
}

export class ThinkAI {
  private embedder: any;
  private db: VectorDB;
  private initialized: boolean = false;
  private dbPath: string;

  constructor() {
    this.dbPath = path.join(os.homedir(), '.think-ai', 'vectordb');
  }

  async initialize(): Promise<void> {
    if (this.initialized) return;

    // Initialize embedding model (uses ONNX - no native dependencies)
    this.embedder = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
    
    // Ensure directory exists
    await fs.mkdir(path.dirname(this.dbPath), { recursive: true });
    
    // Initialize vector database
    this.db = new VectorDB({
      path: this.dbPath,
      dimension: 384, // all-MiniLM-L6-v2 dimension
    });

    await this.db.load();
    this.initialized = true;
  }

  private async getEmbedding(text: string): Promise<number[]> {
    const output = await this.embedder(text, { pooling: 'mean', normalize: true });
    return Array.from(output.data);
  }

  async addCode(
    code: string,
    language: string,
    description: string,
    tags: string[] = []
  ): Promise<number> {
    await this.initialize();

    const embedding = await this.getEmbedding(code);
    const metadata: CodeMetadata = {
      language,
      description,
      tags,
      length: code.length,
    };

    const id = await this.db.add({
      vector: embedding,
      metadata: {
        ...metadata,
        code, // Store code in metadata
      },
    });

    await this.db.save();
    return id;
  }

  async search(query: string, k: number = 5): Promise<SearchResult[]> {
    await this.initialize();

    const queryEmbedding = await this.getEmbedding(query);
    const results = await this.db.search(queryEmbedding, k);

    return results.map((result: any) => ({
      score: result.score,
      code: result.metadata.code,
      metadata: {
        language: result.metadata.language,
        description: result.metadata.description,
        tags: result.metadata.tags || [],
        length: result.metadata.length,
      },
    }));
  }

  async generateCode(prompt: string, language: string = 'javascript'): Promise<string> {
    await this.initialize();

    // Search for similar code
    const similar = await this.search(prompt, 3);
    
    // Build context from similar code
    const context: string[] = [];
    for (const result of similar) {
      if (result.score > 0.5) {
        context.push(`// ${result.metadata.description}\n${result.code}`);
      }
    }

    if (context.length > 0) {
      return `// Generated based on: ${prompt}
// Similar examples found:

${context.slice(0, 2).join('\n\n')}

// Your implementation here:
function implement${language.charAt(0).toUpperCase() + language.slice(1)}Solution() {
  // TODO: Implement based on the examples above
}`;
    } else {
      return `// Generated for: ${prompt}
// Language: ${language}

function implementSolution() {
  // TODO: No similar examples found
  // Start with a basic implementation
}`;
    }
  }

  async analyzeCode(code: string): Promise<any> {
    await this.initialize();

    const similar = await this.search(code, 3);
    
    const analysis = {
      length: code.length,
      lines: code.split('\n').length,
      similarPatterns: [] as any[],
      suggestions: [] as string[],
    };

    for (const result of similar) {
      if (result.score > 0.7) {
        analysis.similarPatterns.push({
          description: result.metadata.description,
          similarity: `${(result.score * 100).toFixed(1)}%`,
          language: result.metadata.language,
        });
      }
    }

    // Basic suggestions
    if (code.includes('TODO') || code.includes('FIXME')) {
      analysis.suggestions.push('Complete TODO/FIXME items');
    }

    if (!code.toLowerCase().includes('test') && !code.includes('assert') && !code.includes('expect')) {
      analysis.suggestions.push('Consider adding tests');
    }

    return analysis;
  }

  async getStats(): Promise<any> {
    await this.initialize();

    const allItems = await this.db.getAll();
    const languages: Record<string, number> = {};
    let totalCharacters = 0;

    for (const item of allItems) {
      const lang = item.metadata.language;
      languages[lang] = (languages[lang] || 0) + 1;
      totalCharacters += item.metadata.length;
    }

    return {
      totalSnippets: allItems.length,
      totalCharacters,
      languages,
    };
  }
}