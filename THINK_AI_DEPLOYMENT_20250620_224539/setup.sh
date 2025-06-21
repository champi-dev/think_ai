#!/bin/bash
# Think AI Quick Setup Script

echo "🚀 Setting up Think AI..."

# Create virtual environment
python -m venv think_ai_env
source think_ai_env/bin/activate

# Install Python packages
pip install ./python_packages/think-ai-consciousness/*.whl
pip install ./python_packages/think-ai-cli/*.whl
pip install ./python_packages/o1-vector-search/*.whl

# Install Node packages
npm install ./javascript_packages/think-ai-js/*.tgz
npm install ./javascript_packages/@think-ai/cli/*.tgz
npm install ./javascript_packages/o1-js/*.tgz

echo "✅ Setup complete!"
echo "Run 'source think_ai_env/bin/activate' to activate the environment"
