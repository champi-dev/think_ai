#!/bin/bash

echo "🤖 Testing Think AI's Human-Like Conversations"
echo "=============================================="
echo ""
echo "Notice how the AI now speaks more naturally, like a super smart human!"
echo ""

# Build with latest changes
echo "🔨 Building with human conversation features..."
cargo build --release --bin think-ai 2>/dev/null

echo ""
echo "🎭 Testing conversational responses..."
echo ""

# Test greetings
echo "USER: Hi there!"
echo "THINK AI:"
echo "Hi there!" | ./target/release/think-ai chat --once
echo ""

echo "USER: How are you doing?"
echo "THINK AI:"
echo "How are you doing?" | ./target/release/think-ai chat --once
echo ""

echo "USER: What is consciousness?"
echo "THINK AI:"
echo "What is consciousness?" | ./target/release/think-ai chat --once
echo ""

echo "USER: Can you explain quantum computing in simple terms?"
echo "THINK AI:"
echo "Can you explain quantum computing in simple terms?" | ./target/release/think-ai chat --once
echo ""

echo "USER: Thanks for the explanation!"
echo "THINK AI:"
echo "Thanks for the explanation!" | ./target/release/think-ai chat --once
echo ""

echo "💡 Notice the differences:"
echo "  - More casual language (\"It's\" instead of \"It is\")"
echo "  - Natural transitions (\"So,\" \"Well,\" \"Actually,\")"
echo "  - Friendly endings (\"Hope that helps!\")"
echo "  - Variety in responses (not the same greeting every time)"
echo ""
echo "To chat interactively with the enhanced AI:"
echo "  ./target/release/think-ai chat"