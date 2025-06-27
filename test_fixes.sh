#!/bin/bash

# Think AI - Test Knowledge Integration Fixes
# Tests the fixes for universe query matching and content truncation

echo "🧠 Think AI - Testing Knowledge Integration Fixes"
echo "================================================"
echo ""

# Build the system
echo "🔨 Building Think AI..."
cargo build --release
echo ""

# Test universe query
echo "🌌 Testing universe query (should show cosmology content):"
echo "what is the universe" | ./target/release/think-ai chat
echo ""

# Test dark energy query  
echo "⚡ Testing dark energy query (should use enhanced knowledge):"
echo "dark energy" | ./target/release/think-ai chat
echo ""

# Test consciousness query
echo "🧠 Testing consciousness query:"
echo "what is consciousness" | ./target/release/think-ai chat
echo ""

echo "✅ Test completed!"
echo ""
echo "Expected results:"
echo "- Universe query should return astronomy/cosmology content (not APOD)"
echo "- Responses should show full content without '...' truncation"
echo "- Knowledge indicators: [📚 Knowledge Base] or [📚 Enhanced Knowledge]"
echo "- System should load 341 items from enhanced knowledge"