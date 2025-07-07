#!/bin/bash
# Update library versions for redeployment

echo "🔄 Updating Think AI Library Versions"
echo "====================================="

# Function to bump patch version
bump_patch() {
    local current=$1
    IFS='.' read -r major minor patch <<< "$current"
    new_patch=$((patch + 1))
    echo "$major.$minor.$new_patch"
}

# Update npm version
echo ""
echo "📦 Updating npm package version..."
cd think-ai-js
current_npm=$(node -p "require('./package.json').version")
new_npm=$(bump_patch "$current_npm")
echo "   Current: v$current_npm"
echo "   New:     v$new_npm"

# Update package.json
sed -i "s/\"version\": \"$current_npm\"/\"version\": \"$new_npm\"/" package.json

# Update Python version
echo ""
echo "🐍 Updating PyPI package version..."
cd ../think-ai-py
current_py=$(grep "version = " pyproject.toml | sed 's/version = "\(.*\)"/\1/')
new_py=$(bump_patch "$current_py")
echo "   Current: v$current_py"
echo "   New:     v$new_py"

# Update pyproject.toml
sed -i "s/version = \"$current_py\"/version = \"$new_py\"/" pyproject.toml

cd ..
echo ""
echo "✅ Versions updated!"
echo ""
echo "Next steps:"
echo "1. Review the changes"
echo "2. Commit the version updates"
echo "3. Run deployment commands"