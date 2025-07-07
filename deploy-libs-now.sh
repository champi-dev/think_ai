#!/bin/bash
# Deploy Think AI libraries to npm and PyPI

set -e  # Exit on any error

echo "🚀 Think AI Library Deployment"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -f "Cargo.toml" ]; then
    echo "❌ Error: Please run this script from the Think AI root directory"
    exit 1
fi

# Deploy Python package to PyPI
echo "🐍 Deploying Python package to PyPI..."
echo "--------------------------------------"
cd think-ai-py

# Install twine if not already installed
echo "📦 Installing twine..."
pip install --upgrade twine

# Check the distribution files
echo ""
echo "📋 Distribution files:"
ls -la dist/

# Upload to PyPI
echo ""
echo "📤 Uploading to PyPI..."
echo "Note: Use __token__ as username and your PyPI token as password"
python3 -m twine upload dist/*

cd ..
echo ""
echo "✅ Python package deployed!"
echo ""

# Deploy npm package
echo "📦 Deploying JavaScript package to npm..."
echo "-----------------------------------------"
cd think-ai-js

# Check if logged in to npm
if ! npm whoami &>/dev/null; then
    echo "📝 Please log in to npm:"
    npm login
fi

# Publish to npm
echo ""
echo "📤 Publishing to npm..."
npm publish --access public

cd ..
echo ""
echo "✅ JavaScript package deployed!"
echo ""

# Summary
echo "🎉 Deployment Complete!"
echo "======================"
echo ""
echo "📊 Deployed versions:"
echo "  - npm (thinkai-quantum): v1.0.6"
echo "  - PyPI (thinkai-quantum): v1.0.3"
echo ""
echo "🧪 Test the deployments:"
echo "  - npm:  npx thinkai-quantum@latest chat"
echo "  - PyPI: pip install --upgrade thinkai-quantum && think-ai chat"
echo ""
echo "📍 Package URLs:"
echo "  - npm:  https://www.npmjs.com/package/thinkai-quantum"
echo "  - PyPI: https://pypi.org/project/thinkai-quantum/"