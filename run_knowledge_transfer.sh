#!/bin/bash

# Think AI Knowledge Transfer Training Script
# This script runs the 1000 iteration knowledge transfer from Claude to Think AI

echo "════════════════════════════════════════════════════════════"
echo "🧠 THINK AI KNOWLEDGE TRANSFER SYSTEM 🧠"
echo "Transfer Claude's knowledge and thinking patterns to Think AI"
echo "════════════════════════════════════════════════════════════"

# Check if we're in the right directory
if [ ! -f "Cargo.toml" ]; then
    echo "❌ Error: Please run this script from the think_ai root directory"
    exit 1
fi

# Parse command line arguments
ITERATIONS=${1:-1000}
RESUME_FLAG=""
CHECKPOINT=""

if [ "$2" = "--resume" ] && [ -n "$3" ]; then
    RESUME_FLAG="--resume"
    CHECKPOINT="--checkpoint $3"
fi

echo ""
echo "🔄 Training Configuration:"
echo "  Iterations: $ITERATIONS"
if [ -n "$RESUME_FLAG" ]; then
    echo "  Mode: Resume from checkpoint"
    echo "  Checkpoint: $3"
else
    echo "  Mode: Fresh training"
fi
echo ""

# Build the project in release mode first
echo "🔨 Building Think AI in release mode..."
cargo build --release --bin think-ai

if [ $? -ne 0 ]; then
    echo "❌ Build failed. Please fix compilation errors."
    exit 1
fi

echo "✅ Build successful!"
echo ""

# Run the knowledge transfer
echo "🚀 Starting knowledge transfer training..."
echo "This will train Think AI to think like Claude through $ITERATIONS iterations."
echo ""

# Execute the training command
./target/release/think-ai train --iterations $ITERATIONS $RESUME_FLAG $CHECKPOINT

if [ $? -eq 0 ]; then
    echo ""
    echo "✨ Knowledge transfer completed successfully!"
    echo ""
    echo "📚 Training outputs saved:"
    echo "  - Session data: training_session_*.json"
    echo "  - Knowledge base: knowledge_base_*.json"
    echo "  - Cache data: knowledge_cache_*.json"
    echo ""
    echo "🎯 Next steps:"
    echo "  1. Test the system: ./target/release/think-ai chat"
    echo "  2. Start the server: ./target/release/think-ai server"
    echo "  3. Analyze performance: ./target/release/think-ai info"
else
    echo ""
    echo "❌ Training failed. Check the error messages above."
    exit 1
fi