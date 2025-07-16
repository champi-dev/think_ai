#!/bin/bash

# Think AI - Local Development Runner
# Complete setup and run script for local development

set -e

echo "🧠 Think AI - Local Development Setup"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "Cargo.toml" ]; then
    echo -e "${RED}❌ Error: Please run this script from the think_ai root directory${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check Rust installation
if ! command -v cargo &> /dev/null; then
    echo -e "${RED}❌ Rust not found. Please install Rust first:${NC}"
    echo "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python3 not found. Some features may not work.${NC}"
fi

echo -e "${GREEN}✅ Prerequisites OK${NC}"
echo ""

# Step 1: Build Rust components
echo -e "${BLUE}🔨 Step 1: Building Rust components...${NC}"
echo "This may take a few minutes on first run..."

cargo build --release

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Rust build completed successfully!${NC}"
else
    echo -e "${RED}❌ Rust build failed!${NC}"
    exit 1
fi

echo ""

# Step 2: Optional - Enhance knowledge base
echo -e "${BLUE}🧠 Step 2: Knowledge enhancement (optional)${NC}"
read -p "Do you want to enhance the knowledge base with legal sources? (y/N): " enhance_knowledge

if [[ $enhance_knowledge =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}📚 Enhancing knowledge base...${NC}"
    
    if [ -d "knowledge-enhancement" ]; then
        cd knowledge-enhancement
        
        # Install Python dependencies
        echo "Installing Python dependencies..."
        python3 -m pip install -r requirements.txt --user
        
        # Run knowledge enhancement
        echo "Harvesting legal knowledge sources..."
        python3 test_knowledge_system.py
        
        cd ..
        echo -e "${GREEN}✅ Knowledge enhancement completed!${NC}"
    else
        echo -e "${YELLOW}⚠️  Knowledge enhancement directory not found${NC}"
    fi
fi

echo ""

# Step 3: Choose what to run
echo -e "${BLUE}🚀 Step 3: Choose what to run${NC}"
echo "1) Full system (webapp + API)"
echo "2) CLI only"
echo "3) API server only"
echo "4) 3D Webapp only"
echo "5) Published library test"

read -p "Choose option (1-5): " choice

case $choice in
    1)
        echo -e "${GREEN}🌐 Starting full Think AI system...${NC}"
        echo ""
        echo -e "${BLUE}📡 API Server will be at: http://localhost:8080${NC}"
        echo -e "${BLUE}🌐 3D Webapp will be at: http://localhost:8080${NC}"
        echo -e "${BLUE}💬 Chat interface available at: http://localhost:8080${NC}"
        echo ""
        echo "Press Ctrl+C to stop"
        echo ""
        
        # Kill any existing processes on port 8080
        lsof -ti:8080 | xargs kill -9 2>/dev/null || true
        
        # Run the full server
        ./target/release/full-server
        ;;
        
    2)
        echo -e "${GREEN}💬 Starting Think AI CLI...${NC}"
        echo "Type 'exit' to quit"
        echo ""
        ./target/release/think-ai chat
        ;;
        
    3)
        echo -e "${GREEN}📡 Starting API server only...${NC}"
        echo ""
        echo -e "${BLUE}API will be available at: http://localhost:8080/api${NC}"
        echo -e "${BLUE}Health check: http://localhost:8080/health${NC}"
        echo ""
        echo "Press Ctrl+C to stop"
        echo ""
        
        # Kill any existing processes on port 8080
        lsof -ti:8080 | xargs kill -9 2>/dev/null || true
        
        ./target/release/think-ai server
        ;;
        
    4)
        echo -e "${GREEN}🌐 Starting 3D Webapp only...${NC}"
        echo ""
        echo -e "${BLUE}3D Webapp will be at: http://localhost:8080${NC}"
        echo ""
        echo "Press Ctrl+C to stop"
        echo ""
        
        # Kill any existing processes on port 8080
        lsof -ti:8080 | xargs kill -9 2>/dev/null || true
        
        ./target/release/think-ai-webapp
        ;;
        
    5)
        echo -e "${GREEN}📦 Testing published libraries...${NC}"
        echo ""
        
        # Test JavaScript library
        if command -v npm &> /dev/null; then
            echo -e "${BLUE}Testing JavaScript library...${NC}"
            echo "Installing thinkai-quantum..."
            npm install -g thinkai-quantum 2>/dev/null || npm install thinkai-quantum
            
            echo "Testing CLI..."
            echo "ask 'Hello Think AI'" | npx thinkai-quantum || echo "CLI test completed"
            echo ""
        fi
        
        # Test Python library  
        if command -v python3 &> /dev/null; then
            echo -e "${BLUE}Testing Python library...${NC}"
            echo "Installing thinkai-quantum..."
            python3 -m pip install thinkai-quantum --user
            
            echo "Testing CLI..."
            echo "Available commands:"
            think-ai --help || echo "Install completed - run 'think-ai chat' to start"
            echo ""
        fi
        
        echo -e "${GREEN}✅ Library testing completed!${NC}"
        echo ""
        echo "You can now use:"
        echo "  npx thinkai-quantum chat    # JavaScript CLI"
        echo "  think-ai chat               # Python CLI"
        ;;
        
    *)
        echo -e "${RED}❌ Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Think AI local setup completed!${NC}"

# Show available endpoints
echo ""
echo -e "${BLUE}📋 Available endpoints when running locally:${NC}"
echo "  🌐 Web App: http://localhost:8080"
echo "  📡 API: http://localhost:8080/api"
echo "  🔍 Health: http://localhost:8080/health"
echo "  📊 Stats: http://localhost:8080/api/stats"
echo "  💬 Chat API: http://localhost:8080/api/chat"
echo ""
echo -e "${BLUE}📱 CLI options:${NC}"
echo "  ./target/release/think-ai chat"
echo "  npx thinkai-quantum chat"
echo "  think-ai chat"
echo ""
echo -e "${YELLOW}💡 Tip: You can also use the live deployment at:${NC}"
echo "  https://thinkai-production.up.railway.app"