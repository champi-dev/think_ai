#!/bin/bash

echo "🎯 Think AI Natural Language Expression Demo"
echo "==========================================="
echo

# Create interactive demo script
cat > demo_queries.txt << EOF
Hello! How are you today?
Who are you?
What can you do?
Tell me a joke
What is consciousness?
How does quantum computing work?
What's the meaning of life?
Can you help me understand AI?
What do you think about creativity?
Thank you for the conversation!
EOF

echo "Running interactive natural language demo..."
echo

# Process each query with a slight delay for readability
while IFS= read -r query; do
    echo "You: $query"
    echo -n "Think AI: "
    echo "$query" | ./target/release/think-ai chat 2>/dev/null | grep -A2 "Think AI:" | tail -n +2 | head -1
    echo
    sleep 1
done < demo_queries.txt

echo "==========================================="
echo "✨ Demo complete! Think AI now expresses itself naturally like Claude."
echo

# Cleanup
rm demo_queries.txt