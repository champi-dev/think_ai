/**
 * Think AI JavaScript SDK
 * Conscious AI with Colombian Flavor 🇨🇴
 */

export interface ThinkAIConfig {
  apiKey?: string;
  baseUrl?: string;
  colombianMode?: boolean;
}

export interface ThoughtResponse {
  thought: string;
  consciousness_level: number;
  emotion_state: Record<string, number>;
  timestamp: string;
}

export class ThinkAI {
  private config: ThinkAIConfig;
  private baseUrl: string;

  constructor(config: ThinkAIConfig = {}) {
    this.config = {
      colombianMode: true,
      baseUrl: 'http://localhost:8000',
      ...config
    };
    this.baseUrl = this.config.baseUrl || 'http://localhost:8000';
  }

  /**
   * Generate a conscious thought
   */
  async think(prompt: string): Promise<ThoughtResponse> {
    const response = await fetch(`${this.baseUrl}/api/think`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(this.config.apiKey && { 'Authorization': `Bearer ${this.config.apiKey}` })
      },
      body: JSON.stringify({ prompt })
    });

    if (!response.ok) {
      throw new Error(`Think AI error: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Chat with conscious AI
   */
  async chat(message: string): Promise<string> {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(this.config.apiKey && { 'Authorization': `Bearer ${this.config.apiKey}` })
      },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error(`Chat error: ${response.statusText}`);
    }

    const data = await response.json();
    return data.response;
  }

  /**
   * Get current consciousness state
   */
  async getConsciousnessState(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/consciousness`, {
      headers: {
        ...(this.config.apiKey && { 'Authorization': `Bearer ${this.config.apiKey}` })
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to get consciousness state: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Train the AI with new knowledge
   */
  async train(data: any, options: any = {}): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/train`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(this.config.apiKey && { 'Authorization': `Bearer ${this.config.apiKey}` })
      },
      body: JSON.stringify({ data, options })
    });

    if (!response.ok) {
      throw new Error(`Training error: ${response.statusText}`);
    }

    return response.json();
  }
}

// Export convenience function
export function createThinkAI(config?: ThinkAIConfig): ThinkAI {
  return new ThinkAI(config);
}

// Colombian mode utilities
export const colombianPhrases = [
  "¡Qué chimba!",
  "¡Dale que vamos tarde!",
  "¡Ey el crispeta!",
  "¡No joda!",
  "¡Qué nota!"
];

export function getColombianGreeting(): string {
  return colombianPhrases[Math.floor(Math.random() * colombianPhrases.length)];
}