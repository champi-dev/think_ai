#!/bin/bash

# Quick test for Think AI chat responses

echo "🧪 Quick Test - Think AI Chat"
echo "=============================="
echo ""

# Test queries
echo -e "what is love\nwhat is friendship\nwhat is happiness\nexit" | ./target/release/think-ai chat | grep -E "(Think AI:|You:)" | sed 's/You: /\n❓ Query: /'

echo ""
echo "✅ Test complete!"