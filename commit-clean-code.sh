#!/bin/bash
set -e

echo "📦 Staging Clean Changes"
echo "======================="
echo ""

# Stage all modified and deleted files
echo "Staging changes..."
git add -u

# Add the updated .gitignore and .env.example
git add .gitignore .env.example

# Show what will be committed
echo ""
echo "Files to be committed:"
git status --short | grep -E "^[AMD]"

echo ""
echo "✅ All changes staged!"
echo ""
echo "📝 Ready to commit with:"
echo "   git commit -m 'Remove API keys and sensitive data from tracked files'"
echo ""
echo "Then push with:"
echo "   git push"
echo ""
echo "⚠️  From now on, use environment variables for API keys:"
echo "   export HUGGINGFACE_TOKEN='your_actual_token'"
echo "   Or create a .env file (never commit it!)"
echo ""