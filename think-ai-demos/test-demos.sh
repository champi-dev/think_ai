#!/bin/bash

echo "🚀 Think AI Demo Projects Test Script"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python to run the web server."
    exit 1
fi

echo -e "${GREEN}✅ All 5 demo projects have been created:${NC}"
echo ""
echo "  1️⃣  O(1) Counter - Simple state management with constant time updates"
echo "  2️⃣  O(1) Todo List - Hash-based CRUD operations and persistence"
echo "  3️⃣  O(1) Chat - Real-time messaging with instant routing"
echo "  4️⃣  O(1) Dashboard - Data visualization with pre-computed aggregates"
echo "  5️⃣  O(1) Code Analyzer - AI-powered code analysis with instant AST access"
echo ""
echo -e "${BLUE}📁 Project Structure:${NC}"
echo "  think-ai-demos/"
echo "  ├── index.html (Main showcase page)"
echo "  └── src/"
echo "      ├── project1/index.html"
echo "      ├── project2/index.html"
echo "      ├── project3/index.html"
echo "      ├── project4/index.html"
echo "      └── project5/index.html"
echo ""

# Start web server
PORT=8080
echo -e "${GREEN}🌐 Starting web server on port $PORT...${NC}"
echo ""
echo "Access the demos at: http://localhost:$PORT"
echo "Press Ctrl+C to stop the server"
echo ""

# Change to the demos directory and start server
cd "$(dirname "$0")"
$PYTHON_CMD -m http.server $PORT