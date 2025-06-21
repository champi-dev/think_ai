# 🚀 Think AI Deployment Guide

## Overview

This guide covers deploying Think AI packages to PyPI and npm registries.

## 📦 Available Packages

### Python Packages
- **think-ai** - Main Think AI framework
- **think-ai-cli** - Command-line interface
- **o1-vector-search** - O(1) vector search implementation

### JavaScript Packages
- **think-ai** - JavaScript/TypeScript SDK
- **think-ai-cli** - CLI for Node.js
- **o1-js** - O(1) vector search for JavaScript

## 🛠️ Prerequisites

1. **Python Requirements**:
   ```bash
   pip install twine wheel
   ```

2. **Node.js Requirements**:
   ```bash
   npm install -g npm@latest
   ```

3. **Authentication**:
   - PyPI: Set `PYPI_TOKEN` or configure `~/.pypirc`
   - npm: Run `npm login`

## 🚀 Quick Deployment

### Deploy All Packages
```bash
./scripts/deploy-all-libs.sh
```

### Dry Run (Test Without Publishing)
```bash
./scripts/deploy-all-libs.sh --dry-run
```

### Deploy Only Python Packages
```bash
./scripts/deploy-all-libs.sh --python-only
```

### Deploy Only JavaScript Packages  
```bash
./scripts/deploy-all-libs.sh --js-only
```

## 📈 Version Management

### Bump Version (Patch)
```bash
./scripts/deploy-all-libs.sh --bump all patch
```

### Bump Version (Minor)
```bash
./scripts/deploy-all-libs.sh --bump all minor
```

### Bump Version (Major)
```bash
./scripts/deploy-all-libs.sh --bump all major
```

## 🔒 Security

1. **Never commit credentials** to the repository
2. Use environment variables for tokens:
   ```bash
   export PYPI_TOKEN="pypi-xxxxxxxxxxxx"
   ```
3. Use 2FA on PyPI and npm accounts

## 📋 Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Version bumped appropriately
- [ ] CHANGELOG.md updated
- [ ] Documentation updated
- [ ] Git tag created
- [ ] Clean working directory

## 🔧 Manual Deployment

### Python Package
```bash
cd think-ai-cli/python
python setup.py sdist bdist_wheel
twine upload dist/*
```

### JavaScript Package
```bash
cd npm
npm run build
npm publish --access public
```

## 🐛 Troubleshooting

### "Package already exists" Error
The deployment script uses `--skip-existing` for Python packages. For npm, bump the version.

### Authentication Failed
- PyPI: Check `PYPI_TOKEN` or `~/.pypirc`
- npm: Run `npm login` again

### Build Errors
```bash
# Clean all build artifacts
find . -type d -name "dist" -exec rm -rf {} +
find . -type d -name "build" -exec rm -rf {} +
find . -type d -name "*.egg-info" -exec rm -rf {} +
```

## 📊 Post-Deployment

1. **Verify on PyPI**: https://pypi.org/project/think-ai/
2. **Verify on npm**: https://www.npmjs.com/package/think-ai
3. **Test installation**:
   ```bash
   # Python
   pip install think-ai --upgrade
   
   # JavaScript
   npm install think-ai@latest
   ```

## 🚄 CI/CD Integration

For automated deployments, add to your CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Deploy to PyPI
  env:
    PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
  run: |
    pip install twine
    ./scripts/deploy-all-libs.sh --python-only
```

## 💡 Best Practices

1. **Always test with `--dry-run` first**
2. **Tag releases in Git**:
   ```bash
   git tag -a v2.0.0 -m "Release version 2.0.0"
   git push origin v2.0.0
   ```
3. **Update changelog before deploying**
4. **Test packages after deployment**
5. **Monitor download statistics**

## 🎯 Quick Reference

```bash
# Full deployment
./scripts/deploy-all-libs.sh

# Test deployment
./scripts/deploy-all-libs.sh --dry-run

# Python only
./scripts/deploy-all-libs.sh --python-only

# JavaScript only  
./scripts/deploy-all-libs.sh --js-only

# Bump version and deploy
./scripts/deploy-all-libs.sh --bump all minor
./scripts/deploy-all-libs.sh
```