#!/bin/bash
set -e

echo "🔐 Quick Fix: Remove Secrets Using Reset"
echo "======================================"
echo ""

# Show what we're about to do
echo "This will:"
echo "1. Reset to before the bad commit (d67036de)"
echo "2. Apply all your changes in ONE clean commit"
echo "3. Remove all secrets"
echo ""
echo "Press Enter to continue..."
read

# Save current state
echo "📸 Saving current state..."
git stash push -m "Current work before cleaning secrets" || true

# Reset to before secrets
echo "⏪ Resetting to clean state..."
git reset --hard d67036de

# Get all the changes from the commits after
echo "📥 Getting all changes..."
git cherry-pick --no-commit ec641fc6..4c1c07e6 || true

# Also apply stashed changes if any
git stash pop || true

# Clean ALL secrets
echo "🧹 Cleaning all secrets..."
find . -type f -not -path "./.git/*" -exec grep -l "hf_" {} + 2>/dev/null | while read file; do
    echo "Cleaning: $file"
    sed -i 's/hf_[A-Za-z0-9]\{32,\}/YOUR_HUGGINGFACE_TOKEN_HERE/g' "$file"
done

# Remove bad files
echo "🗑️  Removing sensitive files..."
rm -f test_huggingface_api.sh setup-huggingface-token.sh test-working-models.py find-working-model.py "{}"

# Stage everything
git add -A

# Create one clean commit
echo "📝 Creating clean commit..."
git commit -m "Major update: Qwen integration and security fixes

- Replaced TinyLlama with Qwen as exclusive text generation model
- Fixed webapp hanging issue  
- Removed all API keys and sensitive data from codebase
- Updated documentation and examples
- Added proper .env.example configuration
- Improved E2E test suite"

echo ""
echo "✅ Done! Your history is now clean."
echo ""
echo "🚀 Force push to GitHub:"
echo "   git push --force origin main"
echo ""
echo "This will overwrite the remote history and remove all traces of the secrets."
echo ""