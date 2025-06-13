#!/bin/bash
# Install pre-commit hooks

echo "🔧 Installing Pre-commit Hooks for Think AI..."
echo "============================================="

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ Error: pip is not installed"
    exit 1
fi

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "📦 Installing pre-commit..."
    pip install pre-commit
fi

# Install the git hooks
echo "🔗 Installing git hooks..."
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install -e ".[dev]"

# Run pre-commit on all files to check
echo "🏃 Running pre-commit checks on all files..."
pre-commit run --all-files || true

echo ""
echo "✅ Pre-commit hooks installed successfully!"
echo ""
echo "The following checks will run automatically:"
echo "  - On commit: code formatting, linting, unit tests"
echo "  - On push: integration tests, coverage check"
echo ""
echo "To run all checks manually: pre-commit run --all-files"
echo "To run tests manually: ./run_tests.sh"