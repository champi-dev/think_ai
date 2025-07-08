#!/bin/bash

# Demonstrate AI Learning through Feedback

echo "🤖 Think AI Art - Learning Demonstration"
echo "======================================="
echo ""
echo "This demonstrates how Think AI learns from feedback"
echo "to improve its image generation over time."
echo ""

# Generate an initial image
echo "Step 1: Initial Generation"
echo "-------------------------"
./target/release/think-ai-art generate "a futuristic city with flying cars" -o learning_test_1.png
echo ""

# Provide positive feedback
echo "Step 2: Providing Positive Feedback"
echo "----------------------------------"
./target/release/think-ai-art feedback "a futuristic city with flying cars" excellent \
    -s "neon lights" \
    -s "cyberpunk aesthetic" \
    -s "rain effect"
echo ""

# Generate a similar prompt to see improvement
echo "Step 3: Testing Learned Patterns"
echo "--------------------------------"
./target/release/think-ai-art generate "a futuristic metropolis at night" -o learning_test_2.png
echo ""
echo "Notice how the AI now includes elements it learned from feedback!"
echo ""

# Try interactive mode
echo "Step 4: Interactive Learning Session"
echo "-----------------------------------"
echo "Try the interactive mode to:"
echo "- Generate multiple images"
echo "- Provide immediate feedback"
echo "- Watch the AI improve in real-time"
echo ""
echo "Run: ./target/release/think-ai-art interactive"
echo ""

# Show final statistics
echo "📊 AI Learning Progress"
echo "----------------------"
./target/release/think-ai-art stats
echo ""

echo "🎓 Key Learning Features:"
echo "- O(1) caching for instant retrieval"
echo "- Prompt enhancement based on successful patterns"
echo "- Style combination learning"
echo "- Negative prompt generation to avoid common issues"
echo "- Continuous improvement through feedback"
echo ""

echo "💡 Tips for Training the AI:"
echo "1. Be specific in your feedback"
echo "2. Provide suggestions for what worked well"
echo "3. Rate consistently to help the AI understand preferences"
echo "4. The more feedback, the better it gets!"