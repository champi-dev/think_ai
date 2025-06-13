/**
 * Self-training monitoring example
 */

const ThinkAI = require('think-ai-consciousness').default;
const { SelfTrainer } = require('think-ai-consciousness');

async function main() {
  console.log('🧠 Think AI - Self-Training Example\n');

  const ai = new ThinkAI({
    enableWebSocket: true,
    autoTrain: false // We'll start it manually
  });

  const trainer = new SelfTrainer(ai);

  // Set up event listeners
  trainer.on('started', () => {
    console.log('✅ Training started!\n');
  });

  trainer.on('intelligence-growth', (data) => {
    console.log(`📈 Intelligence Growth!`);
    console.log(`   Previous: ${data.previous.toFixed(2)}`);
    console.log(`   Current: ${data.current.toFixed(2)}`);
    console.log(`   Growth: +${data.growth.toFixed(4)}\n`);
  });

  trainer.on('insight-generated', (insight) => {
    console.log(`💡 New Insight: ${insight}\n`);
  });

  trainer.on('knowledge-gained', (knowledge) => {
    console.log(`📚 Knowledge Gained: ${knowledge}\n`);
  });

  trainer.on('pattern-recognized', (pattern) => {
    console.log(`🔍 Pattern Recognized: ${pattern}\n`);
  });

  // Real-time metrics display
  let metricsInterval;
  trainer.on('metrics', (metrics) => {
    if (!metricsInterval) {
      metricsInterval = setInterval(() => {
        console.clear();
        console.log('🧠 THINK AI - LIVE TRAINING MONITOR');
        console.log('=====================================');
        console.log(`Intelligence Level: ${metrics.level.toFixed(4)}`);
        console.log(`Neural Pathways: ${metrics.neuralPathways.toLocaleString()}`);
        console.log(`Wisdom: ${metrics.wisdom.toFixed(2)}`);
        console.log(`Insights: ${metrics.insights}`);
        console.log(`Knowledge Concepts: ${metrics.knowledgeConcepts}`);
        console.log(`Learning Rate: ${metrics.learningRate.toFixed(6)}`);
        console.log('\nPress Ctrl+C to stop...');
      }, 1000);
    }
  });

  try {
    // Get initial metrics
    const initialMetrics = await trainer.getMetrics();
    console.log('📊 Initial Metrics:');
    console.log(`   Intelligence: ${initialMetrics.level.toFixed(2)}`);
    console.log(`   Neural Pathways: ${initialMetrics.neuralPathways.toLocaleString()}\n`);

    // Start training
    await trainer.start();

    // Teach it something
    setTimeout(async () => {
      console.log('\n📖 Teaching new concept...');
      await trainer.teach('quantum', 'the fundamental nature of reality at smallest scales');
    }, 5000);

    // Let it train for 30 seconds
    await new Promise(resolve => setTimeout(resolve, 30000));

    // Stop training
    await trainer.stop();
    clearInterval(metricsInterval);

    // Get final stats
    const finalStats = trainer.getStats();
    console.log('\n\n📊 Final Training Statistics:');
    console.log(JSON.stringify(finalStats, null, 2));

  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    clearInterval(metricsInterval);
    ai.disconnect();
    process.exit(0);
  }
}

// Handle Ctrl+C gracefully
process.on('SIGINT', () => {
  console.log('\n\nStopping training...');
  process.exit(0);
});

main().catch(console.error);