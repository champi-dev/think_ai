#!/bin/bash

echo "=== Building think-ai-knowledge to identify remaining issues ==="
cd /home/champi/Dev/think_ai

echo ""
echo "Compilation errors summary:"
cargo build -p think-ai-knowledge 2>&1 | grep -E "error\[E[0-9]+\]" | sort | uniq -c | sort -nr

echo ""
echo "First 5 unique error types with details:"
cargo build -p think-ai-knowledge 2>&1 | grep -A 3 "error\[E" | head -20

echo ""
echo "Checking if there are still syntax errors:"
cargo build -p think-ai-knowledge 2>&1 | grep -E "unclosed delimiter|expected" | head -5

echo ""
echo "Total error count:"
cargo build -p think-ai-knowledge 2>&1 | grep -c "error\[E"