#!/bin/bash
set -e

echo "🚨 Emergency Fix: Remove ALL Secrets from History"
echo "=============================================="
echo ""
echo "⚠️  This will REWRITE your git history!"
echo "⚠️  Make sure you have a backup!"
echo ""
echo "Press Enter to continue or Ctrl+C to cancel..."
read

# Save current branch state
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
CURRENT_COMMIT=$(git rev-parse HEAD)

echo "📝 Current state saved: $CURRENT_BRANCH at $CURRENT_COMMIT"
echo ""

# Create backup branch
git branch backup-before-clean-$CURRENT_COMMIT || true

# Reset to before the bad commit
echo "🔄 Resetting to commit before secrets were added..."
git reset --hard d67036de  # This is the commit before ec641fc6

# Now recreate the commits without secrets
echo "📦 Recreating commits without secrets..."

# Create a clean commit with all current changes
git cherry-pick --no-commit ec641fc6..4c1c07e6

# Clean all files of secrets
echo "🧹 Cleaning secrets from all files..."
find . -type f \( -name "*.rs" -o -name "*.md" -o -name "*.sh" -o -name "*.py" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" \) -exec sed -i 's/hf_[A-Za-z0-9]\{32,\}/YOUR_HUGGINGFACE_TOKEN_HERE/g' {} + 2>/dev/null || true

# Remove sensitive files
rm -f test_huggingface_api.sh setup-huggingface-token.sh test-working-models.py find-working-model.py "{}" 2>/dev/null || true

# Stage all changes
git add -A

# Commit with a clean message
git commit -m "Update: Remove TinyLlama, add Qwen integration, remove secrets

- Removed all TinyLlama references
- Added Qwen as the exclusive model for text generation  
- Fixed webapp hanging issue
- Removed all API keys and sensitive data
- Updated documentation"

echo ""
echo "✅ History cleaned!"
echo ""
echo "🚀 Now force push to overwrite remote:"
echo "   git push --force origin main"
echo ""
echo "📝 If something goes wrong, restore from backup:"
echo "   git reset --hard backup-before-clean-$CURRENT_COMMIT"
echo ""