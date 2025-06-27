/**
 * Think AI - Main Client
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import WebSocket from 'ws';
import { 
  ThinkAIConfig, 
  ChatRequest, 
  ChatResponse, 
  SystemStats, 
  HealthStatus,
  StreamResponse,
  ThinkAIError,
  LogLevel 
} from './types';

export class ThinkAI {
  private client: AxiosInstance;
  private config: Required<ThinkAIConfig>;
  private ws?: WebSocket;

  constructor(config: ThinkAIConfig = {}) {
    this.config = {
      baseUrl: config.baseUrl || 'https://thinkai-production.up.railway.app',
      timeout: config.timeout || 30000,
      debug: config.debug || false
    };

    this.client = axios.create({
      baseURL: this.config.baseUrl,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'think-ai-js/1.0.0'
      }
    });

    // Add request/response interceptors for debugging
    if (this.config.debug) {
      this.client.interceptors.request.use(req => {
        console.log(`[Think AI] ${req.method?.toUpperCase()} ${req.url}`);
        return req;
      });

      this.client.interceptors.response.use(
        res => {
          console.log(`[Think AI] ${res.status} ${res.config.url} (${res.headers['content-length']} bytes)`);
          return res;
        },
        err => {
          console.error(`[Think AI] Error: ${err.message}`);
          return Promise.reject(err);
        }
      );
    }
  }

  /**
   * Send a chat message to Think AI
   */
  async chat(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await this.client.post<ChatResponse>('/api/chat', request);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Get system statistics
   */
  async getStats(): Promise<SystemStats> {
    try {
      const response = await this.client.get<SystemStats>('/api/stats');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Check system health
   */
  async getHealth(): Promise<HealthStatus> {
    try {
      const response = await this.client.get<HealthStatus>('/health');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Search knowledge base
   */
  async search(query: string, limit: number = 10): Promise<any> {
    try {
      const response = await this.client.get('/api/search', {
        params: { query, limit }
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Stream chat responses (real-time)
   */
  async streamChat(
    request: ChatRequest, 
    onChunk: (chunk: StreamResponse) => void
  ): Promise<void> {
    return new Promise((resolve, reject) => {
      const wsUrl = this.config.baseUrl.replace('http', 'ws') + '/ws/chat';
      this.ws = new WebSocket(wsUrl);

      this.ws.on('open', () => {
        this.ws!.send(JSON.stringify(request));
      });

      this.ws.on('message', (data) => {
        try {
          const chunk: StreamResponse = JSON.parse(data.toString());
          onChunk(chunk);
          
          if (chunk.done) {
            this.ws!.close();
            resolve();
          }
        } catch (error) {
          reject(new ThinkAIError(`Failed to parse stream response: ${error}`));
        }
      });

      this.ws.on('error', (error) => {
        reject(new ThinkAIError(`WebSocket error: ${error.message}`));
      });

      this.ws.on('close', () => {
        resolve();
      });
    });
  }

  /**
   * Quick chat - simplified interface
   */
  async ask(question: string): Promise<string> {
    const response = await this.chat({ query: question });
    return response.response;
  }

  /**
   * Check if the service is available
   */
  async ping(): Promise<boolean> {
    try {
      await this.getHealth();
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Get knowledge domains
   */
  async getDomains(): Promise<any> {
    try {
      const stats = await this.getStats();
      return Object.entries(stats.domain_distribution).map(([name, count]) => ({
        name,
        count
      }));
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Set debug mode
   */
  setDebug(enabled: boolean): void {
    this.config.debug = enabled;
  }

  /**
   * Close WebSocket connection if open
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = undefined;
    }
  }

  private handleError(error: any): ThinkAIError {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError;
      const message = (axiosError.response?.data as any)?.message || 
                     axiosError.message || 
                     'Unknown error';
      
      return new ThinkAIError(
        message,
        axiosError.response?.status,
        axiosError.code,
        axiosError.response?.data
      );
    }
    
    if (error instanceof ThinkAIError) {
      return error;
    }
    
    return new ThinkAIError(error.message || 'Unknown error');
  }
}

// Convenience functions for quick usage
export const createClient = (config?: ThinkAIConfig) => new ThinkAI(config);

export const quickChat = async (question: string, config?: ThinkAIConfig): Promise<string> => {
  const client = createClient(config);
  return await client.ask(question);
};