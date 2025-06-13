/**
 * Think AI Client - Main interface for Think AI
 */

import axios, { AxiosInstance } from 'axios';
import WebSocket from 'ws';
import { EventEmitter } from 'events';
import {
  ThinkAIConfig,
  ThinkAIResponse,
  IntelligenceMetrics,
  TrainingUpdate
} from './types';

export class ThinkAIClient extends EventEmitter {
  private config: Required<ThinkAIConfig>;
  private api: AxiosInstance;
  private ws?: WebSocket;
  private connected: boolean = false;
  private reconnectAttempts: number = 0;

  constructor(config: Partial<ThinkAIConfig> = {}) {
    super();
    
    this.config = {
      serverUrl: config.serverUrl || 'http://localhost:8000',
      colombianMode: config.colombianMode ?? true,
      autoTrain: config.autoTrain ?? true,
      enableWebSocket: config.enableWebSocket ?? true,
      timeout: config.timeout || 30000
    };

    this.api = axios.create({
      baseURL: this.config.serverUrl,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (this.config.enableWebSocket) {
      this.connectWebSocket();
    }
  }

  /**
   * Send a message to Think AI
   */
  async think(message: string): Promise<ThinkAIResponse> {
    try {
      const response = await this.api.post('/think', {
        query: message,
        colombianMode: this.config.colombianMode
      });

      const data = response.data;
      
      // Emit intelligence update
      this.emit('intelligence-update', data.intelligence);

      return data;
    } catch (error) {
      throw new Error(`Think AI request failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Generate code with Think AI
   */
  async generateCode(
    description: string,
    language: string = 'python'
  ): Promise<any> {
    try {
      const response = await this.api.post('/generate-code', {
        description,
        language
      });

      return response.data;
    } catch (error) {
      throw new Error(`Code generation failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Get current intelligence metrics
   */
  async getIntelligence(): Promise<IntelligenceMetrics> {
    try {
      const response = await this.api.get('/intelligence');
      return response.data;
    } catch (error) {
      throw new Error(`Failed to get intelligence metrics: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Start self-training
   */
  async startTraining(): Promise<void> {
    try {
      await this.api.post('/training/start');
      this.emit('training-started');
    } catch (error) {
      throw new Error(`Failed to start training: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Stop self-training
   */
  async stopTraining(): Promise<void> {
    try {
      await this.api.post('/training/stop');
      this.emit('training-stopped');
    } catch (error) {
      throw new Error(`Failed to stop training: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Connect to WebSocket for real-time updates
   */
  private connectWebSocket(): void {
    const wsUrl = this.config.serverUrl.replace(/^http/, 'ws') + '/ws';
    
    this.ws = new WebSocket(wsUrl);

    this.ws.on('open', () => {
      this.connected = true;
      this.reconnectAttempts = 0;
      this.emit('connected');
      console.log('Connected to Think AI WebSocket');
    });

    this.ws.on('message', (data: WebSocket.Data) => {
      try {
        const update = JSON.parse(data.toString()) as TrainingUpdate;
        this.emit('training-update', update);
        
        // Emit specific events
        switch (update.type) {
          case 'intelligence':
            this.emit('intelligence-update', update.metrics);
            break;
          case 'knowledge':
            this.emit('knowledge-update', update);
            break;
          case 'insight':
            this.emit('insight', update.message);
            break;
          case 'pattern':
            this.emit('pattern-recognized', update.message);
            break;
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    });

    this.ws.on('close', () => {
      this.connected = false;
      this.emit('disconnected');
      
      // Attempt reconnection
      if (this.reconnectAttempts < 5) {
        this.reconnectAttempts++;
        setTimeout(() => this.connectWebSocket(), 5000 * this.reconnectAttempts);
      }
    });

    this.ws.on('error', (error: Error) => {
      this.emit('error', error);
    });
  }

  /**
   * Disconnect from Think AI
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = undefined;
    }
    this.connected = false;
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.connected;
  }

  /**
   * Colombian expression helper
   */
  async expressColombian(expression: string): Promise<string> {
    const expressions: Record<string, string> = {
      'hello': '¡Quiubo parce!',
      'thanks': '¡Gracias parcero!',
      'awesome': '¡Qué chimba!',
      'lets_go': '¡Dale que vamos tarde!',
      'wow': '¡Uy, parce!',
      'difficult': 'Me quedó grande',
      'fast': '¡Las neuronas a mil!'
    };

    return expressions[expression] || '¡Dale!';
  }
}