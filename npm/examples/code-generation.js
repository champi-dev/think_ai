/**
 * Code generation example with Think AI
 */

const { createThinkAI, CodeGenerator } = require('think-ai-consciousness');

async function main() {
  console.log('💻 Think AI - Code Generation Example\n');

  const ai = createThinkAI();
  const coder = new CodeGenerator(ai);

  try {
    // Generate Python function
    console.log('1️⃣ Generating Python fibonacci function...');
    const pythonCode = await coder.generate('Create a recursive fibonacci function', {
      language: 'python',
      filename: 'fibonacci.py',
      includeTests: true,
      includeDocs: true
    });
    
    console.log('\nGenerated Python code:');
    console.log(pythonCode.code);
    console.log(`\nSaved to: ${pythonCode.filePath || 'Not saved'}\n`);

    // Generate JavaScript API
    console.log('2️⃣ Generating Express.js REST API...');
    const jsCode = await coder.generate('Create a REST API for a todo list with CRUD operations', {
      language: 'javascript',
      filename: 'todo-api.js',
      includeTests: false
    });

    console.log('\nGenerated JavaScript code:');
    console.log(jsCode.code.substring(0, 500) + '...\n'); // Show first 500 chars

    // Generate from template
    console.log('3️⃣ Using code template...');
    const templates = coder.getTemplates();
    console.log('\nAvailable templates:', Object.keys(templates).join(', '));
    console.log('\nReact component template:');
    console.log(templates['react-component']);

    // Generate complete project
    console.log('4️⃣ Generating complete project...');
    const project = await coder.generateProject(
      'A weather dashboard with real-time updates',
      'web-app'
    );
    
    console.log('\nProject generated:');
    console.log(`Type: ${project.type}`);
    console.log(`Description: ${project.description}`);
    console.log(`Response: ${project.response.substring(0, 200)}...`);

  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    ai.disconnect();
  }
}

main().catch(console.error);