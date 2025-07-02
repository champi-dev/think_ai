#!/bin/bash

echo "🧠 Testing Think AI Knowledge Fixes"
echo "==================================="
echo ""

# Test universe question
echo "🌌 Testing: 'what is the universe'"
echo "Expected: Proper universe/cosmology content"
echo "Response:"
timeout 15s ./target/release/think-ai chat <<< "what is the universe"
echo ""
echo "---"
echo ""

# Test celestial objects question  
echo "⭐ Testing: 'what are celestial objects'"
echo "Expected: Proper astronomy content, not literature"
echo "Response:"
timeout 15s ./target/release/think-ai chat <<< "what are celestial objects"
echo ""
echo "---"
echo ""

# Test love question (verify no abstract principles)
echo "❤️ Testing: 'what is love'"
echo "Expected: Proper love definition, NOT abstract principles"
echo "Response:"
timeout 15s ./target/release/think-ai chat <<< "what is love"
echo ""

echo "✅ Test completed!"
echo ""
echo "✅ Expected fixes:"
echo "- 'what is the universe' should return universe information (Big Bang, galaxies, etc.)"
echo "- 'what are celestial objects' should return astronomy content (stars, planets, etc.)"
echo "- 'what is love' should NOT return 'Abstract principle derived from...'"
echo "- All responses should be relevant and complete (not truncated)"