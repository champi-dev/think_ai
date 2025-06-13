/**
 * Type definitions for Think AI
 */

export interface ThinkAIConfig {
  /**
   * Think AI server URL
   * @default "http://localhost:8000"
   */
  serverUrl?: string;

  /**
   * Enable Colombian expressions
   * @default true
   */
  colombianMode?: boolean;

  /**
   * Auto-start self-training
   * @default true
   */
  autoTrain?: boolean;

  /**
   * WebSocket for real-time updates
   * @default true
   */
  enableWebSocket?: boolean;

  /**
   * Request timeout in milliseconds
   * @default 30000
   */
  timeout?: number;
}

export interface ThinkAIResponse {
  /**
   * The AI's response text
   */
  response: string;

  /**
   * Current intelligence metrics
   */
  intelligence: IntelligenceMetrics;

  /**
   * Architecture components used
   */
  architectureUsed: {
    cache: boolean;
    knowledgeBase: number;
    vectorSearch: number;
    graphConnections: number;
    selfTraining: boolean;
  };

  /**
   * Processing time in milliseconds
   */
  processingTime: number;

  /**
   * Confidence score (0-1)
   */
  confidence: number;
}

export interface IntelligenceMetrics {
  /**
   * Current intelligence level
   */
  level: number;

  /**
   * Active neural pathways
   */
  neuralPathways: number;

  /**
   * Wisdom accumulated
   */
  wisdom: number;

  /**
   * Total insights generated
   */
  insights: number;

  /**
   * Knowledge concepts stored
   */
  knowledgeConcepts: number;

  /**
   * Learning rate
   */
  learningRate: number;
}

export interface CodeGenerationOptions {
  /**
   * Programming language
   */
  language: 'python' | 'javascript' | 'typescript' | 'java' | 'cpp' | 'go' | 'rust' | 'ruby' | 'php' | 'bash';

  /**
   * Output filename
   */
  filename?: string;

  /**
   * Execute after generation
   * @default false
   */
  execute?: boolean;

  /**
   * Include tests
   * @default true
   */
  includeTests?: boolean;

  /**
   * Include documentation
   * @default true
   */
  includeDocs?: boolean;
}

export interface CodeResult {
  /**
   * Generated code
   */
  code: string;

  /**
   * File path where code was saved
   */
  filePath?: string;

  /**
   * Execution result if executed
   */
  executionResult?: {
    success: boolean;
    output?: string;
    error?: string;
  };

  /**
   * Test results if tests were generated
   */
  testResults?: {
    passed: number;
    failed: number;
    coverage: number;
  };
}

export interface TrainingUpdate {
  /**
   * Update type
   */
  type: 'intelligence' | 'knowledge' | 'insight' | 'pattern';

  /**
   * Update message
   */
  message: string;

  /**
   * Current metrics
   */
  metrics: IntelligenceMetrics;

  /**
   * Timestamp
   */
  timestamp: Date;
}