#!/bin/bash
# Test CI dependency installation

echo "Testing dependency installation in CI environment..."

# Create a temporary virtual environment
TEMP_VENV=$(mktemp -d)/venv
python3 -m venv $TEMP_VENV
source $TEMP_VENV/bin/activate

# Install dependencies from requirements-fast.txt
echo "Installing dependencies from requirements-fast.txt..."
pip install --upgrade pip
pip install -r requirements-fast.txt

# Test imports
echo "Testing imports..."
python -c "
import sys
try:
    import numpy
    print('✓ numpy imported')
except ImportError as e:
    print(f'✗ numpy import failed: {e}')
    sys.exit(1)

try:
    import torch
    print('✓ torch imported')
except ImportError as e:
    print(f'✗ torch import failed: {e}')
    sys.exit(1)

try:
    import transformers
    print('✓ transformers imported')
except ImportError as e:
    print(f'✗ transformers import failed: {e}')
    sys.exit(1)

try:
    import chromadb
    print('✓ chromadb imported')
except ImportError as e:
    print(f'✗ chromadb import failed: {e}')
    sys.exit(1)

try:
    import faiss
    print('✓ faiss available')
except ImportError:
    print('ℹ faiss not available (expected)')

print('\\n✅ All required dependencies imported successfully!')
"

# Clean up
deactivate
rm -rf $(dirname $TEMP_VENV)

echo "Test completed successfully!"