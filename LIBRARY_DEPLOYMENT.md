# Think AI Library Deployment Guide

## 📦 Current Versions
- **npm (thinkai-quantum)**: v1.0.6
- **PyPI (thinkai-quantum)**: v1.0.3

## 🚀 Quick Deployment Steps

### 1. Prepare for Deployment
```bash
# Ensure you're in the project root
cd ~/Dev/think_ai

# Check that versions were updated
grep version think-ai-js/package.json
grep version think-ai-py/pyproject.toml
```

### 2. Deploy to npm

```bash
cd think-ai-js

# Build the TypeScript code
npm run build

# Test locally
npm test

# Login to npm (if not already logged in)
npm login

# Publish the package
npm publish --access public

# Verify deployment
npm view thinkai-quantum
```

### 3. Deploy to PyPI

```bash
cd ../think-ai-py

# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Install build tools
pip install --upgrade build twine

# Build the package
python3 -m build

# Test the package
python3 -m pytest tests/ -v

# Upload to PyPI
python3 -m twine upload dist/*
# Username: __token__
# Password: <your-pypi-token>

# Verify deployment
pip install --upgrade thinkai-quantum
```

## 🧪 Test Deployed Libraries

### Test npm Package
```bash
# Install globally
npm install -g thinkai-quantum@latest

# Test CLI
think-ai --version
think-ai chat

# Or use npx
npx thinkai-quantum chat
```

### Test PyPI Package
```bash
# Install/upgrade
pip install --upgrade thinkai-quantum

# Test CLI
think-ai --version
think-ai chat
```

## 📝 Post-Deployment

1. **Commit version changes**:
```bash
git add think-ai-js/package.json think-ai-py/pyproject.toml
git commit -m "Bump library versions: npm v1.0.6, PyPI v1.0.3"
git push
```

2. **Create release notes** (optional):
```bash
# Create a GitHub release with the new versions
# Tag: v1.0.6-js-v1.0.3-py
```

3. **Update documentation**:
- Update README with new version numbers
- Update installation instructions if needed

## 🔐 API Tokens

### npm Token
1. Go to https://www.npmjs.com/settings/YOUR_USERNAME/tokens
2. Create a new "Publish" token
3. Save it securely

### PyPI Token
1. Go to https://pypi.org/manage/account/token/
2. Create a new API token (scope: entire account or project-specific)
3. Save it securely

## 🤖 Automated Deployment

To enable automated deployment:
```bash
# Set environment variables
export NPM_TOKEN="your-npm-token"
export PYPI_TOKEN="your-pypi-token"

# Run automated deployment
./scripts/deploy-all-libs.sh
```

## 📊 Check Deployment Status

- npm: https://www.npmjs.com/package/thinkai-quantum
- PyPI: https://pypi.org/project/thinkai-quantum/

## ⚠️ Troubleshooting

### npm Issues
- Ensure you're logged in: `npm whoami`
- Check registry: `npm config get registry`
- Clear cache: `npm cache clean --force`

### PyPI Issues
- Ensure twine is updated: `pip install --upgrade twine`
- Test upload first: `python3 -m twine upload --repository testpypi dist/*`
- Check package metadata: `python3 -m twine check dist/*`