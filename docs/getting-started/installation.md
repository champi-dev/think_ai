# Installation Guide

[← Back to Home](../index.md) | [Next: Quick Start →](./quickstart.md)

> **Feynman Explanation**: Installing Think AI is like setting up a new app on your phone - just a few simple steps!

## 📋 Table of Contents
- [Requirements](#requirements)
- [Quick Install](#quick-install)
- [Detailed Installation](#detailed-installation)
- [Verify Installation](#verify-installation)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## 🎯 Requirements

Think of these as the "ingredients" you need:

### Minimum Requirements
- **Python 3.8+** (the language Think AI speaks)
- **4GB RAM** (memory for thinking)
- **2GB disk space** (room for knowledge)
- **Internet connection** (for downloading)

### Optional but Recommended
- **GPU with CUDA** (turbo boost for thinking)
- **Docker** (easy deployment container)
- **Node.js 16+** (for JavaScript features)

## 🚀 Quick Install

### The "Just Make It Work" Method

```bash
# For Python users (most common)
pip install think-ai-consciousness

# For JavaScript users
npm install think-ai-js
```

That's it! You now have Think AI installed. 🎉

## 📦 Detailed Installation

### Method 1: Python Package (Recommended)

Think of this as the standard installation - like installing from an app store:

```bash
# Step 1: Create a safe space for Think AI (virtual environment)
python -m venv think-ai-env

# Step 2: Enter the safe space
# On Mac/Linux:
source think-ai-env/bin/activate
# On Windows:
think-ai-env\Scripts\activate

# Step 3: Install Think AI
pip install think-ai-consciousness

# Step 4: Install optional extras for more features
pip install think-ai-consciousness[full]  # All features
```

### Method 2: JavaScript Package

For web developers who prefer JavaScript:

```bash
# Using npm (comes with Node.js)
npm install think-ai-js

# Or using yarn (alternative package manager)
yarn add think-ai-js

# For command-line tools
npm install -g @think-ai/cli
```

### Method 3: From Source (Advanced)

Like building furniture from scratch - more control, but more work:

```bash
# Step 1: Get the code
git clone https://github.com/champi-dev/think_ai.git
cd think_ai

# Step 2: Install in development mode
pip install -e .

# Step 3: Install development dependencies
pip install -r requirements-dev.txt
```

### Method 4: Docker (Easiest for Deployment)

Think of Docker as a pre-built house - everything's already set up:

```bash
# Pull the image (download pre-built Think AI)
docker pull thinkaiorg/think-ai:latest

# Run it
docker run -p 8000:8000 thinkaiorg/think-ai:latest
```

## ✅ Verify Installation

Let's make sure everything works - like testing a new toy:

### Python Verification

```python
# Test 1: Can we import Think AI?
python -c "import think_ai; print('✅ Think AI imported successfully!')"

# Test 2: Check the version
python -c "import think_ai; print(f'Version: {think_ai.__version__}')"

# Test 3: Quick functionality test
python -c "
from think_ai import ThinkAI
ai = ThinkAI()
response = ai.chat('Hello!')
print(f'AI says: {response}')
"
```

### JavaScript Verification

```javascript
// test-think-ai.js
const { ThinkAI } = require('think-ai-js');

const ai = new ThinkAI();
console.log('✅ Think AI loaded successfully!');

// Test a simple chat
ai.chat('Hello!').then(response => {
  console.log('AI says:', response);
});
```

Run with: `node test-think-ai.js`

### Command Line Verification

```bash
# Check if CLI is installed
think-ai --version

# Get help
think-ai --help

# Quick test
think-ai chat "Hello, are you working?"
```

## 🔧 Troubleshooting

### Common Issues and Simple Solutions

#### "Module not found" Error
**Problem**: Python can't find Think AI
**Solution**: Make sure you're in the right environment
```bash
# Activate your virtual environment first
source think-ai-env/bin/activate  # Mac/Linux
# OR
think-ai-env\Scripts\activate  # Windows
```

#### Installation Fails with "Permission denied"
**Problem**: No permission to install
**Solution**: Use `--user` flag or virtual environment
```bash
pip install --user think-ai-consciousness
```

#### "No matching distribution found"
**Problem**: Your Python version might be too old
**Solution**: Check Python version and upgrade if needed
```bash
python --version  # Should be 3.8 or higher
```

#### GPU Not Detected
**Problem**: Think AI isn't using your GPU
**Solution**: Install CUDA support
```bash
pip install think-ai-consciousness[gpu]
```

### Still Having Issues?

1. Check our [detailed troubleshooting guide](../deployment/troubleshooting.md)
2. Search [existing issues](https://github.com/champi-dev/think_ai/issues)
3. Ask for help in [discussions](https://github.com/champi-dev/think_ai/discussions)

## 🎊 Next Steps

Congratulations! Think AI is installed. Here's what to do next:

### 1. **Try Your First Conversation**
   → [Quick Start Tutorial](./quickstart.md)

### 2. **Understand How It Works**
   → [Core Concepts](./concepts.md)

### 3. **Explore Features**
   → [Basic Usage Guide](../guides/basic-usage.md)

### 4. **Join the Community**
   → [GitHub Discussions](https://github.com/champi-dev/think_ai/discussions)

## 📚 Related Documentation

- [System Requirements Details](../deployment/requirements.md)
- [Docker Deployment Guide](../deployment/docker.md)
- [Building from Source](../developer/building.md)
- [Environment Variables](../deployment/configuration.md)

---

[← Back to Home](../index.md) | [Next: Quick Start →](./quickstart.md)

**Questions?** Check the [FAQ](../guides/faq.md) or [ask the community](https://github.com/champi-dev/think_ai/discussions) 💬