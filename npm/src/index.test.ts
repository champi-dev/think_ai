/**
 * Basic tests for Think AI npm package
 */

import ThinkAI, { 
  createThinkAI, 
  ThinkAIClient,
  CodeGenerator,
  SelfTrainer 
} from './index';

describe('Think AI NPM Package', () => {
  test('exports default client', () => {
    expect(ThinkAI).toBeDefined();
    expect(ThinkAI).toBe(ThinkAIClient);
  });

  test('exports named components', () => {
    expect(ThinkAIClient).toBeDefined();
    expect(CodeGenerator).toBeDefined();
    expect(SelfTrainer).toBeDefined();
  });

  test('createThinkAI factory works', () => {
    const ai = createThinkAI({ enableWebSocket: false });
    expect(ai).toBeInstanceOf(ThinkAIClient);
  });

  test('client accepts configuration', () => {
    const ai = new ThinkAIClient({
      serverUrl: 'http://localhost:9999',
      colombianMode: false,
      timeout: 5000,
      enableWebSocket: false
    });
    expect(ai).toBeInstanceOf(ThinkAIClient);
  });
});