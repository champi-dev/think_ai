#!/bin/bash

# Script to test if trainer.rs compiles correctly after fixing delimiter errors

echo "Testing trainer.rs compilation..."
echo "================================"

# Change to the think-ai-knowledge directory
cd /home/champi/Dev/think_ai/think-ai-knowledge

# Run cargo check to verify syntax without full compilation
echo "Running cargo check..."
cargo check --lib 2>&1 | head -50

echo ""
echo "Running cargo clippy for linting..."
cargo clippy --lib -- -D warnings 2>&1 | head -50

echo ""
echo "Test complete!"