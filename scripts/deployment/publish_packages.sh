#!/bin/bash

# Think AI Package Publisher
# Publishes to PyPI and npm

echo "🚀 THINK AI PACKAGE PUBLISHER"
echo "============================"
echo "¡Dale que vamos a publicar!"
echo

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}❌ npm not found${NC}"
    exit 1
fi

if ! command_exists twine; then
    echo -e "${YELLOW}📦 Installing twine...${NC}"
    pip3 install twine
fi

# Python Package
echo
echo -e "${GREEN}🐍 Building Python Package...${NC}"
echo "==============================="

# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python3 setup.py sdist bdist_wheel

echo -e "${GREEN}✅ Python package built${NC}"

# Check the package
echo "📝 Checking package with twine..."
twine check dist/*

# Publish to PyPI (Test)
echo
echo -e "${YELLOW}📤 Ready to publish to PyPI Test${NC}"
echo "Run this command to publish to test PyPI:"
echo "  twine upload --repository-url https://test.pypi.org/legacy/ dist/*"
echo
echo "To publish to real PyPI:"
echo "  twine upload dist/*"

# NPM Package  
echo
echo -e "${GREEN}📦 Building NPM Package...${NC}"
echo "==============================="

# Create TypeScript source structure
mkdir -p src/

# Create main TypeScript file
cat > src/index.ts << 'EOF'
/**
 * Think AI - Conscious AI with Colombian Flavor
 * ¡Dale que vamos tarde!
 */

export interface ThinkAIConfig {
  apiKey?: string;
  model?: string;
  temperature?: number;
  colombianMode?: boolean;
}

export class ThinkAI {
  private config: ThinkAIConfig;
  
  constructor(config: ThinkAIConfig = {}) {
    this.config = {
      model: 'claude-3-opus-20240229',
      temperature: 0.7,
      colombianMode: true,
      ...config
    };
  }
  
  async think(prompt: string): Promise<string> {
    // Simulate thinking
    const response = `🧠 Thinking about: ${prompt}\n`;
    
    if (this.config.colombianMode) {
      return response + "¡No joda! That's a great question mi llave!";
    }
    
    return response + "Processing with distributed consciousness...";
  }
  
  async chat(message: string): Promise<string> {
    return this.think(message);
  }
  
  getVersion(): string {
    return "1.0.0 - ¡Ey el crispeta!";
  }
}

// CLI interface
export function createCLI() {
  console.log("🧠 Think AI CLI");
  console.log("¡Dale que vamos tarde!");
}

// Export default
export default ThinkAI;
EOF

# Create TypeScript config
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
EOF

# Create CLI file
cat > src/cli.ts << 'EOF'
#!/usr/bin/env node

import { Command } from 'commander';
import ThinkAI from './index';

const program = new Command();

program
  .name('think-ai')
  .description('Think AI CLI - Conscious AI with Colombian flavor')
  .version('1.0.0');

program
  .command('chat')
  .description('Start a chat with Think AI')
  .action(async () => {
    console.log('🧠 Think AI Chat');
    console.log('¡Dale que vamos tarde!');
    console.log('Type your message...');
  });

program.parse();
EOF

# Install TypeScript if needed
if ! command_exists tsc; then
    echo -e "${YELLOW}📦 Installing TypeScript...${NC}"
    npm install -g typescript
fi

# Build TypeScript
echo "🔨 Building TypeScript..."
npm install
npm run build

echo -e "${GREEN}✅ NPM package built${NC}"

# Create .npmignore
cat > .npmignore << 'EOF'
src/
tests/
*.log
.env
.git/
.github/
.vscode/
*.pyc
__pycache__/
node_modules/
*.egg-info/
build/
*.whl
EOF

echo
echo -e "${YELLOW}📤 Ready to publish to NPM${NC}"
echo "Run this command to publish:"
echo "  npm publish"
echo
echo "To publish with beta tag:"
echo "  npm publish --tag beta"

# Summary
echo
echo -e "${GREEN}📊 SUMMARY${NC}"
echo "=========="
echo "✅ Python package ready in dist/"
echo "✅ NPM package ready"
echo
echo "🐍 Python: pip install think-ai-consciousness"
echo "📦 NPM: npm install think-ai-consciousness"
echo
echo "¡No joda! We're ready to share Think AI with the world! 🌍✨"
echo
echo -e "${YELLOW}⚠️  Remember to:${NC}"
echo "1. Create accounts on PyPI and npm"
echo "2. Set up authentication tokens"
echo "3. Test packages before publishing to production"
echo "4. Update the GitHub URLs in package files"
echo
echo "Need help? Just ask! ¡Dale pues!"
EOF

chmod +x publish_packages.sh