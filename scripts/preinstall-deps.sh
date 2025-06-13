#!/bin/bash
# Preinstall and cache all dependencies

echo "🚀 Preinstalling and caching all dependencies..."
echo "============================================="

# Create cache directory
CACHE_DIR="$HOME/.think-ai-cache"
mkdir -p "$CACHE_DIR/pip"
mkdir -p "$CACHE_DIR/npm"
mkdir -p "$CACHE_DIR/models"

# Python dependencies
echo "📦 Installing Python dependencies..."
export PIP_CACHE_DIR="$CACHE_DIR/pip"

# Install in order of size/importance
pip install --upgrade pip setuptools wheel

# Heavy ML dependencies first
echo "🤖 Installing ML dependencies..."
pip install numpy>=1.19.0
pip install torch>=1.9.0 --index-url https://download.pytorch.org/whl/cpu
pip install transformers>=4.20.0
pip install sentence-transformers>=2.2.0

# Vector search backends
echo "🔍 Installing vector search..."
pip install annoy>=1.17.0
# REMOVED: faiss-cpu - replaced with O(1) vector search implementation

# Web framework
echo "🌐 Installing web framework..."
pip install fastapi>=0.68.0 uvicorn>=0.15.0

# Development tools
echo "🛠️ Installing dev tools..."
pip install -r requirements-dev.txt

# All other requirements
echo "📋 Installing remaining requirements..."
pip install -r requirements-fast.txt

# Predownload models
echo "📥 Pre-downloading models..."
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Node.js dependencies for CLI
if command -v npm &> /dev/null; then
    echo "📦 Installing Node.js dependencies..."
    cd think-ai-cli/nodejs
    npm config set cache "$CACHE_DIR/npm"
    npm install
    cd ../..
fi

# Compile Python files
echo "⚡ Pre-compiling Python files..."
python -m compileall -q .

# Create .env for optimizations
echo "🔧 Creating optimization config..."
cat > .env.optimized << EOF
# Performance optimizations
PYTHONOPTIMIZE=2
PYTHONDONTWRITEBYTECODE=1
TOKENIZERS_PARALLELISM=false
PYTORCH_ENABLE_MPS_FALLBACK=1

# Cache directories
PIP_CACHE_DIR=$CACHE_DIR/pip
NPM_CONFIG_CACHE=$CACHE_DIR/npm
TRANSFORMERS_CACHE=$CACHE_DIR/models
EOF

echo ""
echo "✅ Dependencies cached successfully!"
echo ""
echo "Cache locations:"
echo "  Python: $CACHE_DIR/pip"
echo "  NPM: $CACHE_DIR/npm" 
echo "  Models: $CACHE_DIR/models"
echo ""
echo "To use cached deps: source .env.optimized"