/**
 * Self Trainer - Monitor and interact with self-training
 */

import { EventEmitter } from 'events';
import { ThinkAIClient } from './client';
import { IntelligenceMetrics, TrainingUpdate } from './types';

export class SelfTrainer extends EventEmitter {
  private client: ThinkAIClient;
  private trainingActive: boolean = false;
  private metrics?: IntelligenceMetrics;

  constructor(client: ThinkAIClient) {
    super();
    this.client = client;

    // Subscribe to client events
    this.client.on('training-update', (update: TrainingUpdate) => {
      this.handleTrainingUpdate(update);
    });

    this.client.on('intelligence-update', (metrics: IntelligenceMetrics) => {
      this.metrics = metrics;
      this.emit('metrics', metrics);
    });
  }

  /**
   * Start self-training
   */
  async start(): Promise<void> {
    await this.client.startTraining();
    this.trainingActive = true;
    this.emit('started');
  }

  /**
   * Stop self-training
   */
  async stop(): Promise<void> {
    await this.client.stopTraining();
    this.trainingActive = false;
    this.emit('stopped');
  }

  /**
   * Get current metrics
   */
  async getMetrics(): Promise<IntelligenceMetrics> {
    this.metrics = await this.client.getIntelligence();
    return this.metrics;
  }

  /**
   * Check if training is active
   */
  isTraining(): boolean {
    return this.trainingActive;
  }

  /**
   * Handle training updates
   */
  private handleTrainingUpdate(update: TrainingUpdate): void {
    // Emit specific events based on update type
    switch (update.type) {
      case 'intelligence':
        this.emit('intelligence-growth', {
          previous: this.metrics?.level || 1,
          current: update.metrics.level,
          growth: update.metrics.level - (this.metrics?.level || 1)
        });
        break;
      
      case 'knowledge':
        this.emit('knowledge-gained', update.message);
        break;
      
      case 'insight':
        this.emit('insight-generated', update.message);
        break;
      
      case 'pattern':
        this.emit('pattern-recognized', update.message);
        break;
    }

    // Always emit the raw update
    this.emit('update', update);
  }

  /**
   * Get training statistics
   */
  getStats(): any {
    if (!this.metrics) {
      return null;
    }

    return {
      intelligenceLevel: this.metrics.level,
      neuralPathways: this.metrics.neuralPathways,
      wisdomAccumulated: this.metrics.wisdom,
      insightsGenerated: this.metrics.insights,
      knowledgeConcepts: this.metrics.knowledgeConcepts,
      learningRate: this.metrics.learningRate,
      isTraining: this.trainingActive
    };
  }

  /**
   * Simulate manual learning
   */
  async teach(concept: string, understanding: string): Promise<void> {
    // Send a teaching query to Think AI
    const query = `Learn this: ${concept} means ${understanding}`;
    await this.client.think(query);
    
    this.emit('taught', { concept, understanding });
  }
}