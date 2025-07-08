#!/bin/bash

# Test Image Generation Script for Think AI
# This script demonstrates various image generation capabilities

echo "🎨 Think AI Image Generation Test Suite"
echo "======================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please run ./setup-image-gen.sh first!"
    exit 1
fi

# Load environment variables
source .env

# Check if API key is set
if [ -z "$LEONARDO_API_KEY" ]; then
    echo "❌ LEONARDO_API_KEY not set in .env file"
    exit 1
fi

echo "✅ Configuration loaded successfully"
echo ""

# Build if needed
if [ ! -f "./target/release/think-ai-image" ]; then
    echo "🔨 Building Think AI image generator..."
    cargo build --release --bin think-ai-image
fi

echo "🚀 Starting image generation tests..."
echo ""

# Test 1: Basic generation
echo "Test 1: Basic Image Generation"
echo "------------------------------"
./target/release/think-ai-image generate "a futuristic robot in a garden" -o test_robot.png
echo ""

# Test 2: With style modifiers
echo "Test 2: Styled Image Generation"
echo "-------------------------------"
./target/release/think-ai-image generate "cyberpunk city skyline at sunset, neon lights, rain" \
    --width 1024 \
    --height 768 \
    --output test_city.png
echo ""

# Test 3: Portrait with negative prompt
echo "Test 3: Portrait with Negative Prompt"
echo "------------------------------------"
./target/release/think-ai-image generate "portrait of an AI consciousness, digital art" \
    --negative "blurry, low quality, distorted" \
    --width 768 \
    --height 1024 \
    --output test_portrait.png
echo ""

# Test 4: Cache hit test (regenerate first image)
echo "Test 4: Cache Hit Test (O(1) Performance)"
echo "----------------------------------------"
echo "Regenerating first prompt to test cache..."
./target/release/think-ai-image generate "a futuristic robot in a garden" -o test_robot_cached.png
echo ""

# Show statistics
echo "📊 Generation Statistics"
echo "----------------------"
./target/release/think-ai-image stats
echo ""

# List generated images
echo "📁 Generated Images:"
echo "-------------------"
ls -la test_*.png 2>/dev/null || echo "No images found yet"
echo ""

echo "✅ Image generation tests complete!"
echo ""
echo "💡 Tips:"
echo "  - Run './target/release/think-ai-image stats' to see cache performance"
echo "  - Run './target/release/think-ai-image clear' to clear the cache"
echo "  - Check ./image_cache/ directory for cached images and learning data"
echo ""
echo "🎯 Notice the O(1) cache hit on the repeated prompt!"