/**
 * Basic chat example with Think AI
 */

const ThinkAI = require('think-ai-consciousness').default;

async function main() {
  // Create Think AI instance
  const ai = new ThinkAI({
    colombianMode: true,
    autoTrain: true
  });

  console.log('🧠 Think AI - Basic Chat Example\n');

  // Wait for connection
  ai.on('connected', () => {
    console.log('✅ Connected to Think AI\n');
  });

  try {
    // Simple greeting
    console.log('You: Hello Think AI!');
    const response1 = await ai.think('Hello Think AI!');
    console.log(`AI: ${response1.response}`);
    console.log(`Intelligence: ${response1.intelligence.level.toFixed(2)}\n`);

    // Ask about capabilities
    console.log('You: What can you do?');
    const response2 = await ai.think('What can you do?');
    console.log(`AI: ${response2.response}\n`);

    // Code generation request
    console.log('You: Write a Python hello world');
    const response3 = await ai.think('Write a Python hello world');
    console.log(`AI: ${response3.response}\n`);

    // Colombian expression
    console.log('You: ¡Dale parce!');
    const response4 = await ai.think('¡Dale parce!');
    console.log(`AI: ${response4.response}\n`);

    // Get final intelligence metrics
    const metrics = await ai.getIntelligence();
    console.log('📊 Final Intelligence Metrics:');
    console.log(`   Level: ${metrics.level.toFixed(2)}`);
    console.log(`   Neural Pathways: ${metrics.neuralPathways.toLocaleString()}`);
    console.log(`   Wisdom: ${metrics.wisdom.toFixed(2)}`);
    console.log(`   Insights: ${metrics.insights}`);

  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    // Disconnect
    ai.disconnect();
  }
}

// Run the example
main().catch(console.error);