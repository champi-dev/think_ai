/**
 * Think AI - Main Client
 * 
 * # What is This?
 * Think of this as your personal AI assistant's phone number.
 * You create one "phone" (client) and then you can:
 * - Send messages (chat)
 * - Ask quick questions (ask)
 * - Check if it's awake (health)
 * - See how smart it is (stats)
 * 
 * # The O(1) Connection
 * Every request goes to our O(1) backend, which means:
 * - Instant responses (no thinking time)
 * - Same speed with 1 user or 1 million users
 * - Like having a genius friend who already knows every answer!
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

/**
 * The main Think AI client class
 * 
 * # How to Think About This
 * This class is like a smart TV remote:
 * - `client`: The infrared beam that sends commands
 * - `config`: Your personal settings (volume, brightness)
 * - `ws`: The streaming connection for live shows
 */
export class ThinkAI {
  private client: AxiosInstance;    // HTTP client for regular requests
  private config: Required<ThinkAIConfig>;  // Settings (with defaults filled in)
  private ws?: WebSocket;           // WebSocket for streaming (optional)

  /**
   * Create a new Think AI client
   * 
   * # What Happens Here
   * Like setting up a new phone:
   * 1. Choose which tower to connect to (baseUrl)
   * 2. Set how long to wait for answers (timeout)
   * 3. Turn on debug mode to see what's happening
   * 
   * # Example
   * ```js
   * const ai = new ThinkAI({
   *   baseUrl: 'https://my-server.com',  // Custom server
   *   timeout: 60000,                     // Wait 1 minute
   *   debug: true                         // See all traffic
   * });
   * ```
   */
  constructor(config: ThinkAIConfig = {}) {
    // Fill in defaults - like a TV remote with preset channels
    this.config = {
      baseUrl: config.baseUrl || 'https://thinkai-production.up.railway.app',
      timeout: config.timeout || 30000,  // 30 seconds default
      debug: config.debug || false
    };

    // Create the HTTP client - like tuning to the right frequency
    this.client = axios.create({
      baseURL: this.config.baseUrl,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',  // We speak JSON
        'User-Agent': 'think-ai-js/1.0.0'    // Identify ourselves
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
   * 
   * # The Magic Mailbox
   * This is like dropping a letter in a mailbox that:
   * 1. Instantly teleports to the AI (POST request)
   * 2. Gets processed with O(1) magic (instant lookup)
   * 3. Returns with an answer before you blink
   * 
   * # What Goes In
   * - query: Your question ("What is consciousness?")
   * - context: Previous conversation (optional)
   * - maxLength: How long the answer can be
   * 
   * # What Comes Out
   * - response: The AI's answer
   * - confidence: How sure it is (0-1)
   * - responseTimeMs: How fast it was (usually < 50ms!)
   */
  async chat(request: ChatRequest): Promise<ChatResponse> {
    try {
      // Send the question to our O(1) backend
      // Like dropping a letter in a pneumatic tube!
      const response = await this.client.post<ChatResponse>('/api/chat', request);
      return response.data;
    } catch (error) {
      // Something went wrong - translate to friendly error
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
   * 
   * # Live TV vs Recorded Shows
   * Regular chat() is like watching a recorded show - you get it all at once.
   * streamChat() is like watching live TV - you see it as it happens!
   * 
   * # How Streaming Works
   * 1. Open a WebSocket (like tuning to a live channel)
   * 2. Send your question
   * 3. Receive answer piece by piece
   * 4. Each piece appears instantly (still O(1)!)
   * 
   * # Why Use This?
   * - See the AI "thinking" in real-time
   * - Better for long responses
   * - Users don't wait for the whole answer
   * 
   * # Example
   * ```js
   * await ai.streamChat(
   *   { query: "Tell me a story" },
   *   (chunk) => {
   *     process.stdout.write(chunk.chunk); // Print as it arrives
   *   }
   * );
   * ```
   */
  async streamChat(
    request: ChatRequest, 
    onChunk: (chunk: StreamResponse) => void
  ): Promise<void> {
    return new Promise((resolve, reject) => {
      // Convert HTTP URL to WebSocket URL
      // Like switching from phone to video call
      const wsUrl = this.config.baseUrl.replace('http', 'ws') + '/ws/chat';
      this.ws = new WebSocket(wsUrl);

      // When connected, send our question
      this.ws.on('open', () => {
        this.ws!.send(JSON.stringify(request));
      });

      // When we receive a piece of the answer
      this.ws.on('message', (data) => {
        try {
          const chunk: StreamResponse = JSON.parse(data.toString());
          onChunk(chunk);  // Give it to the user immediately!
          
          // If this was the last piece, close the connection
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
  async ask(question: string, options?: { sessionId?: string; model?: string }): Promise<string> {
    const response = await this.chat({ 
      query: question,
      sessionId: options?.sessionId,
      model: options?.model
    });
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

export const quickChat = async (
  question: string, 
  options?: { 
    config?: ThinkAIConfig; 
    sessionId?: string; 
    model?: string;
  }
): Promise<string> => {
  const client = createClient(options?.config);
  return await client.ask(question, {
    sessionId: options?.sessionId,
    model: options?.model
  });
};