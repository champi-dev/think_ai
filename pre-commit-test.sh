#!/bin/bash
# Test the pre-commit hook without actually committing

echo "🧪 Testing Think AI Pre-commit Hook"
echo "==================================="
echo ""
echo "This will run all pre-commit checks without making a commit."
echo ""

# Run the pre-commit hook directly
if [ -f .git/hooks/pre-commit ]; then
    .git/hooks/pre-commit
else
    echo "❌ Pre-commit hook not found!"
    echo "Run this first: chmod +x .git/hooks/pre-commit"
fi