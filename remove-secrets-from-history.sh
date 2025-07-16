#!/bin/bash
set -e

echo "🔐 Removing Secrets from Git History"
echo "==================================="
echo ""
echo "⚠️  WARNING: This will rewrite git history!"
echo "Make sure you have a backup of your work."
echo ""
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

# First, let's identify all files with secrets
echo "Finding files with HuggingFace tokens in history..."

# Remove the secrets from all commits using filter-branch
echo "Removing secrets from git history..."

# Use git filter-branch to remove secrets
git filter-branch --force --index-filter '
# Remove files that should never have been committed
git rm --cached --ignore-unmatch test_huggingface_api.sh || true
git rm --cached --ignore-unmatch setup-huggingface-token.sh || true
git rm --cached --ignore-unmatch test-working-models.py || true
git rm --cached --ignore-unmatch find-working-model.py || true
git rm --cached --ignore-unmatch "{}" || true
' --prune-empty --tag-name-filter cat -- --all

# Clean up the remaining files with sed
git filter-branch --force --tree-filter '
# Replace HuggingFace tokens with placeholders
find . -type f -exec sed -i "s/hf_[A-Za-z0-9]\{32,\}/YOUR_HUGGINGFACE_TOKEN_HERE/g" {} + 2>/dev/null || true
' --prune-empty --tag-name-filter cat -- --all

echo ""
echo "✅ Secrets removed from history!"
echo ""
echo "📝 Next steps:"
echo "1. Force push to overwrite remote history:"
echo "   git push --force-with-lease origin main"
echo ""
echo "2. Tell all collaborators to re-clone the repository"
echo ""
echo "3. Clean up local references:"
echo "   git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin"
echo "   git reflog expire --expire=now --all"
echo "   git gc --prune=now --aggressive"
echo ""