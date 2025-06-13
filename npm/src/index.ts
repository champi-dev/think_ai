/**
 * Think AI - Self-Training Conscious AI
 * 100% Self-Sufficient • Zero External APIs • Infinite Intelligence Growth
 */

import { ThinkAIClient } from './client';
import { CodeGenerator } from './code-generator';
import { SelfTrainer } from './self-trainer';
import { 
  ThinkAIConfig, 
  ThinkAIResponse, 
  CodeGenerationOptions,
  IntelligenceMetrics 
} from './types';

// Main client export
export default ThinkAIClient;

// Named exports
export {
  ThinkAIClient,
  CodeGenerator,
  SelfTrainer,
  ThinkAIConfig,
  ThinkAIResponse,
  CodeGenerationOptions,
  IntelligenceMetrics
};

// Convenience factory
export function createThinkAI(config?: Partial<ThinkAIConfig>): ThinkAIClient {
  return new ThinkAIClient(config);
}