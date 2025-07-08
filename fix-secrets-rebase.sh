#!/bin/bash
set -e

echo "🔐 Fixing Secrets in Git History (Interactive Rebase)"
echo "=================================================="
echo ""
echo "This will help you remove the HuggingFace tokens from commit ec641fc6"
echo ""

# Create a script to clean files during rebase
cat > /tmp/clean_secrets.sh << 'EOF'
#!/bin/bash
# Remove sensitive files
rm -f test_huggingface_api.sh setup-huggingface-token.sh test-working-models.py find-working-model.py "{}"

# Clean any remaining tokens in files
find . -type f -name "*.rs" -o -name "*.md" -o -name "*.sh" -o -name "*.py" -o -name "*.yaml" -o -name "*.yml" | while read file; do
    if [ -f "$file" ]; then
        sed -i 's/hf_[A-Za-z0-9]\{32,\}/YOUR_HUGGINGFACE_TOKEN_HERE/g' "$file" 2>/dev/null || true
    fi
done

# Stage the changes
git add -A
EOF

chmod +x /tmp/clean_secrets.sh

echo "Instructions:"
echo "============="
echo ""
echo "1. Run this command to start interactive rebase:"
echo "   git rebase -i ec641fc6~1"
echo ""
echo "2. In the editor, change 'pick' to 'edit' for commit ec641fc6"
echo ""
echo "3. Save and close the editor"
echo ""
echo "4. When git stops at that commit, run:"
echo "   /tmp/clean_secrets.sh"
echo "   git commit --amend --no-edit"
echo "   git rebase --continue"
echo ""
echo "5. Finally, force push:"
echo "   git push --force-with-lease origin main"
echo ""
echo "Press Enter to see a simpler automated approach..."
read

echo ""
echo "🚀 Automated Approach (Recommended):"
echo "==================================="
echo ""
echo "Run these commands:"
echo ""
echo "# Go back to before the problematic commit"
echo "git reset --hard ec641fc6~1"
echo ""
echo "# Cherry-pick the commits but clean them"
echo "git cherry-pick ec641fc6..HEAD"
echo ""
echo "# Clean the files"
echo "/tmp/clean_secrets.sh"
echo ""
echo "# Amend the commits"
echo "git add -A"
echo "git commit --amend -m 'Remove secrets and update Qwen integration'"
echo ""
echo "# Force push"
echo "git push --force-with-lease origin main"
echo ""