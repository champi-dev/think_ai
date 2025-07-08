#!/bin/bash

echo "🧪 Testing Think AI Image Generation API"
echo "======================================="
echo ""

# Wait for server to be ready
echo "Waiting for server to start..."
sleep 2

# Test image generation
echo "Test 1: Generate Image"
echo "---------------------"
curl -X POST http://localhost:8080/api/image/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful sunset over mountains",
    "width": 1280,
    "height": 720
  }' | jq -r '.enhanced_prompt' | head -c 100

echo ""
echo ""

# Test stats endpoint
echo "Test 2: Get Statistics"
echo "---------------------"
curl -X GET http://localhost:8080/api/image/stats | jq '.'

echo ""
echo ""

# Test feedback endpoint
echo "Test 3: Provide Feedback"
echo "-----------------------"
curl -X POST http://localhost:8080/api/image/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful sunset over mountains",
    "rating": "excellent"
  }' | jq '.'

echo ""
echo "✅ API tests complete!"
echo ""
echo "Visit http://localhost:8080/static/image_generator.html in your browser"
echo "to use the full image generation interface!"