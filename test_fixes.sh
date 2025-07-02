#!/bin/bash

# Think AI - Test Template Corruption Fixes
# Tests the fixes for corrupted template responses

echo "🧠 Think AI - Testing Template Corruption Fixes"
echo "================================================"
echo ""

# Build the system
echo "🔨 Building Think AI..."
cargo build --release
echo ""

echo "📝 Testing questions that were giving corrupted responses:"
echo ""

# Test 1: Universe question (was returning thermodynamics content)
echo "🌌 Question 1: 'what is the universe'"
echo "Expected: Proper universe/cosmology content"
echo "Previous broken response: Thermodynamics content"
echo "Response:"
timeout 15s ./target/release/think-ai chat <<< "what is the universe"
echo ""
echo "---"
echo ""

# Test 2: Fermi Paradox (was returning generic cross-domain response)
echo "👽 Question 2: 'explain me the fermi paradox'"
echo "Expected: Proper Fermi Paradox explanation"
echo "Previous broken response: Cross-domain insight connecting 2 domains"  
echo "Response:"
timeout 15s ./target/release/think-ai chat <<< "explain me the fermi paradox"
echo ""
echo "---"
echo ""

# Test 3: Simple greeting to ensure basic functionality
echo "👋 Question 3: 'hello'"
echo "Expected: Proper greeting response"
echo "Response:"
timeout 15s ./target/release/think-ai chat <<< "hello"
echo ""

echo "✅ Test completed!"
echo ""
echo "✅ Expected improvements:"
echo "- No more meaningless filler text like 'This concept has profound implications'"
echo "- No more generic templates like 'encompasses X while reaching beyond traditional boundaries'"
echo "- Universe question should return actual astronomy content"
echo "- Fermi Paradox should return proper explanation (not cross-domain gibberish)"
echo "- Responses should be relevant to the actual questions asked"