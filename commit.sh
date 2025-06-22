#!/bin/bash
# Think AI Commit Wrapper - Shows full progress bar and complex pipeline

# Check if commit message was provided
if [ -z "$1" ]; then
    echo "❌ Please provide a commit message"
    echo "Usage: ./commit.sh \"your commit message\""
    exit 1
fi

# Store commit message
COMMIT_MSG="$1"

echo "🚀 Running Think AI Full Complex Pipeline..."
echo ""

# Run the ultra-fast pre-commit pipeline directly
if ./scripts/ultra-fast-precommit.sh; then
    echo ""
    echo "✅ All checks passed! Committing..."
    
    # Bypass pre-commit hooks for the actual commit
    git commit -m "$COMMIT_MSG" --no-verify
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully committed: $COMMIT_MSG"
        echo ""
        echo "💡 Tip: Use 'git push' to push your changes"
    else
        echo "❌ Commit failed"
        exit 1
    fi
else
    echo ""
    echo "❌ Pipeline failed! Fix the issues and try again."
    exit 1
fi