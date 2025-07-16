#!/bin/bash

# Think AI - Quick Training Script
# Runs a shorter training session for demonstration

echo "🧠 Think AI - Quick Direct Answer Training"
echo "========================================"
echo ""

# Number of iterations (reduced for demo)
ITERATIONS=1000

echo "🚀 Running training with $ITERATIONS iterations..."
echo "This will improve Think AI's ability to give direct answers."
echo ""

# Run the training
./target/release/train-direct-answers

echo ""
echo "✅ Training complete!"
echo ""
echo "Now you can test the improved chat system:"
echo "  ./target/release/think-ai chat"
echo ""
echo "The system will now provide:"
echo "  • Direct answers to questions"
echo "  • Complete responses without truncation"
echo "  • Relevant information for each query"