#!/bin/bash

echo "=== Testing Think AI CLI for Coding ==="
echo

# 1. Test the main chat interface
echo "1. Testing interactive chat (press Ctrl+C to exit):"
echo "   Run: ./target/release/think-ai chat"
echo

# 2. Test code generation
echo "2. Testing code generation:"
./target/release/think-ai chat <<EOF
Generate a Python function that implements O(1) hash-based lookup
EOF
echo

# 3. Test code analysis
echo "3. Testing code analysis:"
./target/release/think-ai chat <<EOF
Analyze the time complexity of: for i in range(n): for j in range(n): print(i,j)
EOF
echo

# 4. Test the Python CLI (if installed)
echo "4. Testing Python CLI (if installed):"
if command -v think-ai &> /dev/null; then
    echo "Python CLI found. Testing..."
    think-ai chat <<< "What is O(1) complexity?"
else
    echo "Python CLI not installed. Install with: pip install thinkai-quantum"
fi
echo

# 5. Test the JavaScript CLI (if installed)
echo "5. Testing JavaScript CLI (if available):"
if command -v npx &> /dev/null; then
    echo "Testing with npx..."
    npx thinkai-quantum chat <<< "Explain O(1) algorithms"
else
    echo "npx not available. Install Node.js to test JavaScript CLI"
fi
echo

echo "=== Interactive Testing ==="
echo "For interactive testing, run:"
echo "  ./target/release/think-ai chat"
echo
echo "Then try these prompts:"
echo "  - 'Generate an O(1) cache implementation in Rust'"
echo "  - 'Analyze my code for performance issues'"
echo "  - 'Help me optimize this algorithm to O(1)'"
echo "  - 'Explain hash tables and their O(1) operations'"