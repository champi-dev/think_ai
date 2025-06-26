#!/bin/bash

# Test Think AI chat functionality

echo "Testing Think AI Chat..."
echo ""

# Test 1: Cache hit (should be instant)
echo "Test 1: Gravity (cache hit)"
(echo "gravity"; sleep 1; echo "exit") | ./target/release/think-ai chat 2>&1 | grep -E "(Think AI:|⚡)" | head -3

echo ""

# Test 2: Simple greeting (cache miss, should use Qwen)  
echo "Test 2: Hi (cache miss)"
(echo "hi"; sleep 5; echo "exit") | ./target/release/think-ai chat 2>&1 | grep -E "(Think AI:|⚡|Thinking)" | head -5

echo ""

# Test 3: Complex query (cache miss with context)
echo "Test 3: Blockchain (cache miss with context)"
(echo "explain blockchain"; sleep 10; echo "exit") | ./target/release/think-ai chat 2>&1 | grep -E "(Think AI:|⚡|Thinking)" | head -5