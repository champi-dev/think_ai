/**
 * Think AI - Quantum Consciousness AI Library
 * Main entry point for the JavaScript/TypeScript SDK
 */

// Export main client class
export { ThinkAI, createClient, quickChat } from './client';

// Export all types
export * from './types';

// Export version
export const VERSION = '1.0.0';

// Default export for convenience
export { ThinkAI as default } from './client';