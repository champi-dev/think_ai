#\!/bin/bash

echo "🚀 Think AI - Local Runner"
echo "=========================="

# Navigate to project directory
cd /home/champi/Development/think_ai

# Kill any existing processes on port 8080
echo "🔄 Killing existing processes on port 8080..."
pkill -f "think-ai" || true
fuser -k 8080/tcp 2>/dev/null || true

# Build the project in release mode
echo "🔧 Building Think AI..."
cargo build --release

if [ $? -ne 0 ]; then
    echo "❌ Build failed\!"
    exit 1
fi

echo "✅ Build successful\!"
echo ""

# Show available commands
echo "📋 Available Think AI Commands:"
echo "==============================="
echo ""
echo "🗣️  Interactive Chat:"
echo "   ./target/release/think-ai chat"
echo ""
echo "🌐 Web Server (port 8080):"
echo "   ./target/release/think-ai server"
echo ""
echo "🖥️  Web App with 3D Visualization:"
echo "   ./target/release/think-ai-webapp"
echo ""
echo "🧹 Auto-format Rust code:"
echo "   ./target/release/think-ai-lint ."
echo ""
echo "📚 Published Libraries:"
echo "   npm install thinkai-quantum"
echo "   pip install thinkai-quantum"
echo ""

# Ask user what they want to run
echo "What would you like to run?"
echo "1) Chat interface"
echo "2) Web server" 
echo "3) Web app"
echo "4) Show help"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "🗣️ Starting Think AI Chat..."
        ./target/release/think-ai chat
        ;;
    2)
        echo "🌐 Starting Think AI Server on port 8080..."
        echo "Access at: http://localhost:8080"
        ./target/release/think-ai server
        ;;
    3)
        echo "🖥️ Starting Think AI Web App..."
        echo "Access at: http://localhost:3000"
        ./target/release/think-ai-webapp
        ;;
    4)
        echo "📖 Think AI Help:"
        ./target/release/think-ai --help 2>/dev/null || echo "Binary not found - run 'cargo build --release' first"
        ;;
    *)
        echo "🗣️ Starting default chat interface..."
        ./target/release/think-ai chat
        ;;
esac
EOF < /dev/null
