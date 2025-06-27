/**
 * Think AI - Core Types
 */

export interface ThinkAIConfig {
  /** Base URL for Think AI API */
  baseUrl?: string;
  /** API timeout in milliseconds */
  timeout?: number;
  /** Enable debug logging */
  debug?: boolean;
}

export interface ChatRequest {
  /** User query/message */
  query: string;
  /** Optional context for the conversation */
  context?: string[];
  /** Maximum response length */
  maxLength?: number;
}

export interface ChatResponse {
  /** AI response text */
  response: string;
  /** Context used for generating response */
  context?: string[];
  /** Response generation time in milliseconds */
  response_time_ms: number;
  /** Confidence score (0-1) */
  confidence?: number;
}

export interface SystemStats {
  /** Total knowledge nodes in the system */
  total_nodes: number;
  /** Number of training iterations completed */
  training_iterations: number;
  /** Total knowledge items processed */
  total_knowledge_items: number;
  /** Distribution of knowledge across domains */
  domain_distribution: Record<string, number>;
  /** Average confidence across all knowledge */
  average_confidence: number;
  /** System uptime in seconds */
  uptime?: number;
}

export interface HealthStatus {
  /** System status */
  status: 'healthy' | 'degraded' | 'unhealthy';
  /** Detailed health information */
  details?: {
    knowledge_engine: boolean;
    vector_search: boolean;
    ai_models: boolean;
    database: boolean;
  };
  /** Last health check timestamp */
  timestamp: string;
}

export interface KnowledgeDomain {
  /** Domain name */
  name: string;
  /** Number of knowledge items in this domain */
  count: number;
  /** Recent activity score */
  activity: number;
}

export interface SearchResult {
  /** Matching content */
  content: string;
  /** Relevance score */
  score: number;
  /** Knowledge domain */
  domain: string;
  /** Related concepts */
  related_concepts: string[];
}

export interface StreamResponse {
  /** Response chunk */
  chunk: string;
  /** Whether this is the final chunk */
  done: boolean;
  /** Metadata for the chunk */
  metadata?: Record<string, any>;
}

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

export class ThinkAIError extends Error {
  status?: number;
  code?: string;
  details?: any;

  constructor(message: string, status?: number, code?: string, details?: any) {
    super(message);
    this.name = 'ThinkAIError';
    this.status = status;
    this.code = code;
    this.details = details;
  }
}