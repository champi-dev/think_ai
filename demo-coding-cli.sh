#!/bin/bash

echo "🚀 Think AI Coding CLI Demo"
echo "=========================="
echo ""
echo "This demo showcases the new Think AI Coding Assistant with O(1) code generation!"
echo ""
echo "Press Enter to continue..."
read

# Show help
echo "📚 1. Let's see what the coding CLI can do:"
./target/release/think-ai-coding --help
echo ""
echo "Press Enter to continue..."
read

# Generate Hello World
echo "💻 2. Generate a Hello World program in Python:"
./target/release/think-ai-coding generate "hello world" --language python
echo ""
echo "Press Enter to continue..."
read

# Generate a REST API
echo "🌐 3. Generate a REST API in Python:"
./target/release/think-ai-coding generate "rest api" --language python
echo ""
echo "Press Enter to continue..."
read

# Generate a hash function
echo "🔐 4. Generate an O(1) hash function:"
./target/release/think-ai-coding generate "hash function" --language python
echo ""
echo "Press Enter to continue..."
read

# Generate JavaScript code
echo "📦 5. Generate a React component:"
./target/release/think-ai-coding generate "react component" --language javascript
echo ""
echo "Press Enter to continue..."
read

# Generate Rust code
echo "🦀 6. Generate a Rust web server:"
./target/release/think-ai-coding generate "web server" --language rust
echo ""
echo "Press Enter to continue..."
read

# Explain a concept
echo "📖 7. Explain O(1) complexity:"
./target/release/think-ai-coding explain "O(1) complexity"
echo ""
echo "Press Enter to continue..."
read

# Interactive mode teaser
echo "🎮 8. Interactive Mode Available!"
echo ""
echo "To start interactive coding session, run:"
echo "  ./target/release/think-ai-coding chat"
echo ""
echo "In chat mode you can:"
echo "  - Type any coding request"
echo "  - Change languages with 'lang <language>'"
echo "  - Get explanations with 'explain <concept>'"
echo "  - Type 'help' for all commands"
echo ""
echo "Try it out!"
echo ""