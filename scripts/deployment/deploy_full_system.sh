#!/bin/bash
# Deploy Full Think AI System

echo "🚀 Think AI Full Deployment"
echo "=========================="

# Build the system
echo "📦 Building system..."
python build_full_system.py

# Publish Python package
echo ""
echo "🐍 Publishing Python package..."
cd dist/python-package
python -m pip install --upgrade build twine
python -m build
# Uncomment to publish to PyPI:
# python -m twine upload dist/*
cd ../..

# Publish JS package
echo ""
echo "📚 Publishing JS package..."
cd dist/js-package
npm version patch
# Uncomment to publish to npm:
# npm publish --access public
cd ../..

# Deploy to Render
echo ""
echo "☁️  Deploying to Render..."
cd dist/render-deploy

# Initialize git if needed
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Deploy Think AI with full system"
fi

echo ""
echo "✅ Deployment package ready!"
echo ""
echo "📁 Render deployment: dist/render-deploy/"
echo "📦 Python package: dist/python-package/"
echo "📚 JS package: dist/js-package/"
echo ""
echo "Next steps:"
echo "1. cd dist/render-deploy"
echo "2. git remote add render <your-render-git-url>"
echo "3. git push render main"
echo ""
echo "Or use GitHub and connect Render to your repo!"