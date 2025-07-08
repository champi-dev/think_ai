#!/bin/bash

# Test Think AI Art - Open Source Image Generation with Learning

echo "🎨 Think AI Art - Open Source Image Generation Test"
echo "=================================================="
echo ""
echo "This demonstrates AI-powered image generation that learns"
echo "and improves based on feedback."
echo ""

# Test 1: Basic generation
echo "Test 1: Basic AI Art Generation"
echo "------------------------------"
./target/release/think-ai-art generate "a majestic mountain landscape at sunrise" -o ai_art_mountain.png
echo ""

# Test 2: Different style
echo "Test 2: Abstract Art Generation"
echo "-------------------------------"
./target/release/think-ai-art generate "abstract colorful shapes representing joy and energy" \
    --width 768 \
    --height 768 \
    --output ai_art_abstract.png
echo ""

# Test 3: Portrait
echo "Test 3: Portrait Generation"
echo "---------------------------"
./target/release/think-ai-art generate "portrait of a wise elderly person with kind eyes" \
    --width 512 \
    --height 768 \
    --output ai_art_portrait.png
echo ""

# Show statistics
echo "📊 AI Learning Statistics"
echo "------------------------"
./target/release/think-ai-art stats
echo ""

# Test cache hit
echo "Test 4: Cache Hit Test (O(1) Performance)"
echo "----------------------------------------"
./target/release/think-ai-art generate "a majestic mountain landscape at sunrise" -o ai_art_mountain_cached.png
echo ""

echo "✅ AI Art generation tests complete!"
echo ""
echo "🎯 Notice how the AI enhances prompts automatically!"
echo ""
echo "💡 To help the AI learn and improve:"
echo "   - Rate images: ./target/release/think-ai-art feedback \"prompt\" excellent"
echo "   - Interactive mode: ./target/release/think-ai-art interactive"
echo ""
echo "📁 Generated images:"
ls -la ai_art_*.png 2>/dev/null || echo "No images found yet"