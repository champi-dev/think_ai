#!/bin/bash

# Think AI Local Setup Script
# Easy copy-paste script to run Think AI CLI locally

echo "🤖 Setting up Think AI CLI locally..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
if [ -z "$python_version" ]; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python $python_version detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Mac/Linux
    source venv/bin/activate
fi

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Think AI
echo "📦 Installing Think AI..."
pip install -e .

# Create .env file for local mode
echo "📝 Creating .env file for local mode..."
cat > .env << EOF
# Local development mode - no external services required
USE_LOCAL_STORAGE=true
SKIP_EXTERNAL_SERVICES=true
LOCAL_DEV_MODE=true

# Optional: Add your Claude API key if you have one
# CLAUDE_API_KEY=your_api_key_here
# CLAUDE_ENABLED=true
EOF

echo "✅ Setup complete!"
echo ""
echo "🚀 To start using Think AI CLI:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate  # Mac/Linux"
echo "   venv\\Scripts\\activate    # Windows"
echo ""
echo "2. Run the CLI:"
echo "   think-ai                  # Interactive mode"
echo "   think-ai chat 'Hello'     # Direct chat"
echo "   python think_ai_simple_chat.py  # Simple chat interface"
echo ""
echo "3. For help:"
echo "   think-ai --help"
echo ""
echo "💡 Tip: The .env file has been created with local-only settings."
echo "   This means no external services (databases, APIs) are required."
