#!/bin/bash

echo "🧠 THINK AI COMPREHENSIVE TRAINING SYSTEM"
echo "========================================"
echo ""
echo "This will:"
echo "1. Load comprehensive deep knowledge about everything"
echo "2. Train with 1,000,000 iterations"
echo "3. Enable exponential self-learning"
echo "4. Run parallel background learning threads"
echo ""
echo "Press Enter to begin training..."
read

# Build the training binary
echo "🔨 Building training system..."
cargo build --release --bin train-comprehensive

if [ $? -ne 0 ]; then
    echo "❌ Build failed. Please check the code."
    exit 1
fi

# Clear any old training data
echo "🧹 Clearing old training data..."
rm -rf trained_knowledge/*
mkdir -p trained_knowledge/checkpoints

# Run the comprehensive training
echo "🚀 Starting comprehensive training with 1,000,000 iterations..."
echo "This will take some time. Progress will be shown every 1000 iterations."
echo ""

./target/release/train-comprehensive

echo ""
echo "✅ Training complete!"
echo ""
echo "To use the trained system:"
echo "1. Run: ./target/release/think-ai chat"
echo "2. Ask any question about any topic!"
echo "3. The system will continue learning in the background"
echo ""
echo "Examples to try:"
echo "- 'What is the relationship between quantum mechanics and consciousness?'"
echo "- 'How does machine learning relate to neuroscience?'"
echo "- 'Explain the connection between music theory and mathematics'"
echo "- 'What are the philosophical implications of artificial intelligence?'"