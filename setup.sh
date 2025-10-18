#!/bin/bash

echo "╔═══════════════════════════════════════════╗"
echo "║                                           ║"
echo "║      AI Chat - Setup Script               ║"
echo "║                                           ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Node.js is not installed. Please install Node.js v18 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Node.js $(node -v) found${NC}"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}⚠ PostgreSQL CLI not found. Make sure PostgreSQL is installed and running.${NC}"
else
    echo -e "${GREEN}✓ PostgreSQL found${NC}"
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}⚠ Ollama not found. Please install from https://ollama.com${NC}"
else
    echo -e "${GREEN}✓ Ollama found${NC}"
fi

echo ""
echo "Installing dependencies..."
echo ""

# Install server dependencies
echo "📦 Installing server dependencies..."
cd server
npm install
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Server dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install server dependencies${NC}"
    exit 1
fi

# Install client dependencies
echo ""
echo "📦 Installing client dependencies..."
cd ../client
npm install
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Client dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install client dependencies${NC}"
    exit 1
fi

cd ..

echo ""
echo "═══════════════════════════════════════════"
echo ""
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Create PostgreSQL database:"
echo "   psql -U postgres"
echo "   CREATE DATABASE ai_chat;"
echo ""
echo "2. Configure environment:"
echo "   cd server"
echo "   cp .env.example .env"
echo "   # Edit .env with your database credentials"
echo ""
echo "3. Run migrations:"
echo "   npm run migrate"
echo ""
echo "4. Start Ollama and pull a model:"
echo "   ollama serve"
echo "   ollama pull qwen2.5:1.5b"
echo ""
echo "5. Start the servers (in separate terminals):"
echo "   Terminal 1: cd server && npm run dev"
echo "   Terminal 2: cd client && npm run dev"
echo ""
echo "6. Open http://localhost:5173 in your browser"
echo ""
echo "═══════════════════════════════════════════"
