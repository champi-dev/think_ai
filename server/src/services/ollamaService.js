import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const OLLAMA_BASE_URL = process.env.OLLAMA_BASE_URL || 'http://localhost:11434';
const DEFAULT_MODEL = process.env.OLLAMA_MODEL || 'qwen2.5:1.5b';
const VISION_MODEL = process.env.OLLAMA_VISION_MODEL || 'llava:7b';

class OllamaService {
  constructor() {
    this.baseURL = OLLAMA_BASE_URL;
    this.defaultModel = DEFAULT_MODEL;
    this.visionModel = VISION_MODEL;
  }

  async checkConnection() {
    try {
      const response = await axios.get(`${this.baseURL}/api/tags`);
      return { success: true, models: response.data.models };
    } catch (error) {
      console.error('Ollama connection error:', error.message);
      return { success: false, error: error.message };
    }
  }

  async generateResponse(messages, options = {}) {
    const {
      model = this.defaultModel,
      temperature = 0.7,
      maxTokens = 2048,
      stream = false,
    } = options;

    try {
      const payload = {
        model,
        messages,
        stream,
        options: {
          temperature,
          num_predict: maxTokens,
        },
      };

      const response = await axios.post(
        `${this.baseURL}/api/chat`,
        payload,
        {
          responseType: stream ? 'stream' : 'json',
        }
      );

      return response;
    } catch (error) {
      console.error('Ollama generate error:', error.message);
      throw new Error(`Failed to generate response: ${error.message}`);
    }
  }

  async generateStreamResponse(messages, options = {}, onChunk) {
    const {
      model = this.defaultModel,
      temperature = 0.7,
      maxTokens = 2048,
    } = options;

    try {
      const response = await axios.post(
        `${this.baseURL}/api/chat`,
        {
          model,
          messages,
          stream: true,
          options: {
            temperature,
            num_predict: maxTokens,
          },
        },
        {
          responseType: 'stream',
        }
      );

      return new Promise((resolve, reject) => {
        let fullResponse = '';

        response.data.on('data', (chunk) => {
          const lines = chunk.toString().split('\n').filter(line => line.trim());

          for (const line of lines) {
            try {
              const json = JSON.parse(line);
              if (json.message && json.message.content) {
                fullResponse += json.message.content;
                onChunk(json.message.content);
              }
              if (json.done) {
                resolve({ content: fullResponse, ...json });
              }
            } catch (e) {
              // Skip invalid JSON
            }
          }
        });

        response.data.on('error', (error) => {
          reject(error);
        });

        response.data.on('end', () => {
          if (!fullResponse) {
            reject(new Error('Stream ended without response'));
          }
        });
      });
    } catch (error) {
      console.error('Ollama stream error:', error.message);
      throw new Error(`Failed to generate stream response: ${error.message}`);
    }
  }

  async analyzeImage(base64Image, prompt, options = {}) {
    const { model = this.visionModel } = options;

    try {
      const response = await axios.post(`${this.baseURL}/api/generate`, {
        model,
        prompt,
        images: [base64Image],
        stream: false,
      });

      return response.data.response;
    } catch (error) {
      console.error('Ollama image analysis error:', error.message);
      throw new Error(`Failed to analyze image: ${error.message}`);
    }
  }

  async listModels() {
    try {
      const response = await axios.get(`${this.baseURL}/api/tags`);
      return response.data.models || [];
    } catch (error) {
      console.error('Failed to list models:', error.message);
      return [];
    }
  }

  async pullModel(modelName) {
    try {
      const response = await axios.post(
        `${this.baseURL}/api/pull`,
        { name: modelName },
        { responseType: 'stream' }
      );

      return response;
    } catch (error) {
      console.error('Failed to pull model:', error.message);
      throw error;
    }
  }
}

export default new OllamaService();
