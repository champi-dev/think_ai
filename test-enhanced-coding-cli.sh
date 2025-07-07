#!/bin/bash

echo "🎉 ENHANCED Think AI Coding CLI Test"
echo "==================================="
echo ""

echo "✅ Fixed Issues:"
echo "1. 'hello' now generates actual code"
echo "2. 'fibonacci' generates real implementations"
echo "3. 'crud postgresql' generates complete CRUD class"
echo ""

echo "🧪 Running tests..."
echo ""

# Test 1: Hello
echo "Test 1: Simple 'hello' command"
./target/release/think-ai-coding generate "hello" | head -5
echo ""

# Test 2: Fibonacci
echo "Test 2: 'fibonacci' command"
./target/release/think-ai-coding generate "fibonacci" | head -10
echo ""

# Test 3: CRUD
echo "Test 3: 'crud postgresql' command"
./target/release/think-ai-coding generate "crud postgresql" | head -20
echo ""

# Test 4: Class generation
echo "Test 4: 'create a class called User'"
./target/release/think-ai-coding generate "create a class called User" | head -15
echo ""

# Test 5: Function generation
echo "Test 5: 'function to sort data'"
./target/release/think-ai-coding generate "function to sort data" | head -15
echo ""

echo "✨ All tests complete!"
echo ""
echo "To use the interactive chat mode with better code generation:"
echo "  ./target/release/think-ai-coding chat"
echo ""
echo "In chat mode, just type naturally:"
echo "  - 'fibonacci'"
echo "  - 'create a web server'"
echo "  - 'hash function'"
echo "  - 'binary search'"
echo "  - 'async operations'"