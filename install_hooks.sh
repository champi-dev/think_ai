#!/bin/bash
# Install Git hooks for Think AI v3.1.0

echo "🔧 Installing Git hooks for Think AI..."

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook for Think AI v3.1.0
# Formats code and runs full test suite

echo "🔍 Think AI Pre-Commit Hook Running..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get root directory
ROOT_DIR=$(git rev-parse --show-toplevel)
cd "$ROOT_DIR"

# Track if we made any changes
CHANGES_MADE=0

# 1. Format Python code with black (if available)
echo -e "${BLUE}[1/5]${NC} Formatting Python code..."
if command -v black >/dev/null 2>&1; then
    black think_ai_v3/ --line-length 100 --quiet
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Python code formatted"
        CHANGES_MADE=1
    fi
else
    echo -e "${YELLOW}!${NC} black not installed, skipping Python formatting"
fi

# 2. Sort imports with isort (if available)
echo -e "${BLUE}[2/5]${NC} Sorting imports..."
if command -v isort >/dev/null 2>&1; then
    isort think_ai_v3/ --profile black --line-length 100 --quiet
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Imports sorted"
        CHANGES_MADE=1
    fi
else
    echo -e "${YELLOW}!${NC} isort not installed, skipping import sorting"
fi

# 3. Lint with ruff (if available)
echo -e "${BLUE}[3/5]${NC} Linting code..."
if command -v ruff >/dev/null 2>&1; then
    ruff check think_ai_v3/ --fix --quiet
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Code linted and fixed"
        CHANGES_MADE=1
    fi
else
    echo -e "${YELLOW}!${NC} ruff not installed, skipping linting"
fi

# 4. Check Python syntax
echo -e "${BLUE}[4/5]${NC} Checking Python syntax..."
python_errors=0
for file in $(find think_ai_v3 -name "*.py" -type f); do
    python -m py_compile "$file" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗${NC} Syntax error in $file"
        python_errors=$((python_errors + 1))
    fi
done

if [ $python_errors -gt 0 ]; then
    echo -e "${RED}✗${NC} Found $python_errors syntax errors. Fix them before committing."
    exit 1
else
    echo -e "${GREEN}✓${NC} All Python files have valid syntax"
fi

# 5. Run test suite
echo -e "${BLUE}[5/5]${NC} Running test suite..."

# Create a minimal test if none exists
if [ ! -f "think_ai_v3/test_basic.py" ]; then
    cat > think_ai_v3/test_basic.py << 'TESTEOF'
#!/usr/bin/env python3
"""Basic tests for Think AI v3.1.0"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from think_ai_v3.core.config import Config
        from think_ai_v3.core.engine import ThinkAIEngine
        from think_ai_v3.consciousness.awareness import ConsciousnessFramework
        from think_ai_v3.consciousness.principles import ConstitutionalAI
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_config():
    """Test configuration."""
    try:
        from think_ai_v3.core.config import Config
        config = Config()
        assert config.port == 8080
        assert config.colombian_mode == True
        print("✓ Configuration test passed")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_consciousness():
    """Test consciousness framework."""
    try:
        from think_ai_v3.consciousness.awareness import ConsciousnessFramework
        consciousness = ConsciousnessFramework()
        report = consciousness.get_consciousness_report()
        assert "state" in report
        print("✓ Consciousness test passed")
        return True
    except Exception as e:
        print(f"✗ Consciousness test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running Think AI v3.1.0 tests...")
    tests = [test_imports, test_config, test_consciousness]
    passed = sum(1 for test in tests if test())
    total = len(tests)
    print(f"\nTests: {passed}/{total} passed")
    sys.exit(0 if passed == total else 1)
TESTEOF
fi

# Run the test
python think_ai_v3/test_basic.py
if [ $? -ne 0 ]; then
    echo -e "${RED}✗${NC} Tests failed. Fix the issues before committing."
    exit 1
else
    echo -e "${GREEN}✓${NC} All tests passed"
fi

# If we made changes, add them to the commit
if [ $CHANGES_MADE -eq 1 ]; then
    echo -e "${YELLOW}!${NC} Code was formatted/fixed. Adding changes to commit..."
    git add -u
fi

echo -e "${GREEN}✅ Pre-commit checks passed!${NC}"
exit 0
EOF

# Create pre-push hook
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
# Pre-push hook for Think AI v3.1.0
# Deploys all libraries and creates deployment bundle

echo "🚀 Think AI Pre-Push Hook - Preparing deployment..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get root directory
ROOT_DIR=$(git rev-parse --show-toplevel)
cd "$ROOT_DIR"

# 1. Update all requirements files
echo -e "${BLUE}[1/7]${NC} Updating requirements files..."

# Main requirements
cat > think_ai_v3/requirements-all.txt << 'REQEOF'
# Think AI v3.1.0 Complete Requirements
# Generated by pre-push hook

# Core Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0

# Async Support
aiofiles==23.2.1

# ML Libraries (optional but recommended)
torch>=2.0.0
transformers>=4.36.0
sentence-transformers>=2.2.2
accelerate>=0.24.0
bitsandbytes>=0.41.0

# Storage Backends
redis==5.0.1
aiosqlite==0.19.0
motor==3.3.2  # MongoDB async
cassandra-driver==3.28.0
neo4j==5.14.0

# Vector Databases
chromadb==0.4.18
qdrant-client==1.6.9
pymilvus==2.3.3

# Utilities
python-dotenv==1.0.0
httpx==0.25.2
structlog==23.2.0
orjson==3.9.10

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Code Quality
black==23.11.0
ruff==0.1.6
isort==5.12.0
mypy==1.7.1

# Monitoring
prometheus-client==0.19.0
opentelemetry-api==1.21.0
opentelemetry-sdk==1.21.0

# Documentation
mkdocs==1.5.3
mkdocs-material==9.4.14
REQEOF

# Minimal requirements for Railway
cat > think_ai_v3/requirements-minimal.txt << 'REQEOF'
# Think AI v3.1.0 Minimal Requirements
# For lightweight deployments

fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
aiofiles==23.2.1
python-dotenv==1.0.0
httpx==0.25.2
orjson==3.9.10
REQEOF

echo -e "${GREEN}✓${NC} Requirements files updated"

# 2. Create library wheel
echo -e "${BLUE}[2/7]${NC} Creating Python wheel..."

# Create setup.py if it doesn't exist
if [ ! -f "setup.py" ]; then
    cat > setup.py << 'SETUPEOF'
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="think-ai",
    version="3.1.0",
    author="Champi",
    author_email="champi@think-ai.co",
    description="Conscious AI with Colombian Flavor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/think-ai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
    ],
    entry_points={
        "console_scripts": [
            "think-ai=think_ai_v3.app:main",
        ],
    },
)
SETUPEOF
fi

# Build wheel
python -m pip install --quiet build
python -m build --wheel --outdir dist/ .
echo -e "${GREEN}✓${NC} Python wheel created"

# 3. Bundle webapp
echo -e "${BLUE}[3/7]${NC} Bundling webapp..."
if [ -d "webapp" ]; then
    cd webapp
    npm run build --quiet
    cd ..
    tar -czf webapp_bundle.tar.gz webapp/.next webapp/public webapp/package.json
    echo -e "${GREEN}✓${NC} Webapp bundled"
else
    echo -e "${YELLOW}!${NC} Webapp directory not found"
fi

# 4. Create Docker images list
echo -e "${BLUE}[4/7]${NC} Listing Docker configurations..."
cat > DOCKER_IMAGES.md << 'DOCKEREOF'
# Think AI v3.1.0 Docker Images

## Available Dockerfiles

1. **Dockerfile.railway** - Optimized for Railway deployment
   - Minimal size
   - Fast build times
   - Production ready

2. **Dockerfile.v3** - Full featured image
   - All ML libraries included
   - Development tools
   - Larger size

## Build Commands

```bash
# Railway optimized
docker build -f Dockerfile.railway -t think-ai:railway .

# Full featured
docker build -f Dockerfile.v3 -t think-ai:full .

# Minimal
docker build -f Dockerfile.minimal -t think-ai:minimal .
```

## Push to Registry

```bash
# Tag for Docker Hub
docker tag think-ai:railway YOUR_USERNAME/think-ai:v3.1.0

# Push
docker push YOUR_USERNAME/think-ai:v3.1.0
```
DOCKEREOF

# 5. Create deployment scripts
echo -e "${BLUE}[5/7]${NC} Creating deployment scripts..."

# Railway deploy script
cat > deploy_railway.sh << 'DEPLOYEOF'
#!/bin/bash
# Deploy to Railway

echo "Deploying Think AI v3.1.0 to Railway..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Railway CLI not found. Install it from: https://docs.railway.app/develop/cli"
    exit 1
fi

# Deploy
railway up

echo "Deployment complete! Check Railway dashboard for status."
DEPLOYEOF
chmod +x deploy_railway.sh

# Docker deploy script
cat > deploy_docker.sh << 'DEPLOYEOF'
#!/bin/bash
# Deploy with Docker

echo "Building and running Think AI v3.1.0 with Docker..."

# Build
docker build -f Dockerfile.railway -t think-ai:latest .

# Run
docker run -d \
  --name think-ai \
  -p 8080:8080 \
  -e PORT=8080 \
  -e THINK_AI_COLOMBIAN=true \
  --restart unless-stopped \
  think-ai:latest

echo "Think AI is running at http://localhost:8080"
DEPLOYEOF
chmod +x deploy_docker.sh

echo -e "${GREEN}✓${NC} Deployment scripts created"

# 6. Generate deployment manifest
echo -e "${BLUE}[6/7]${NC} Generating deployment manifest..."
cat > DEPLOYMENT_MANIFEST.json << MANIFESTEOF
{
  "version": "3.1.0",
  "generated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "git_commit": "$(git rev-parse HEAD)",
  "git_branch": "$(git rev-parse --abbrev-ref HEAD)",
  "components": {
    "api": {
      "path": "think_ai_v3/",
      "entry": "app.py",
      "port": 8080,
      "endpoints": [
        "/health",
        "/api/v1/generate",
        "/api/v1/chat",
        "/api/v1/knowledge/*",
        "/api/v1/intelligence",
        "/api/v1/ws"
      ]
    },
    "webapp": {
      "path": "webapp/",
      "framework": "Next.js",
      "port": 3000
    },
    "models": {
      "default": "Qwen/Qwen2.5-Coder-1.5B",
      "supported": [
        "Qwen/Qwen2.5-Coder-*",
        "microsoft/phi-2",
        "mistralai/Mistral-7B-*"
      ]
    }
  },
  "deployment_files": [
    "railway.json",
    "Dockerfile.railway",
    "deploy_railway.sh",
    "deploy_docker.sh"
  ],
  "bundles": [
    "dist/think_ai-3.1.0-py3-none-any.whl",
    "webapp_bundle.tar.gz",
    "deployment_bundle.tar.gz"
  ]
}
MANIFESTEOF
echo -e "${GREEN}✓${NC} Deployment manifest generated"

# 7. Create final deployment bundle
echo -e "${BLUE}[7/7]${NC} Creating deployment bundle..."

mkdir -p deployment_bundle
cp -r think_ai_v3 deployment_bundle/
cp Dockerfile.* deployment_bundle/ 2>/dev/null
cp railway.json deployment_bundle/
cp deploy_*.sh deployment_bundle/
cp DEPLOYMENT_MANIFEST.json deployment_bundle/
cp DOCKER_IMAGES.md deployment_bundle/
cp -r dist deployment_bundle/ 2>/dev/null

tar -czf think_ai_v3.1.0_deployment_$(date +%Y%m%d_%H%M%S).tar.gz deployment_bundle/
rm -rf deployment_bundle

echo -e "${GREEN}✓${NC} Deployment bundle created"

# Summary
echo ""
echo -e "${GREEN}✅ Pre-push deployment preparation complete!${NC}"
echo ""
echo "Created:"
echo "  📦 Python wheel in dist/"
echo "  📦 Webapp bundle"
echo "  📦 Deployment bundle"
echo "  📄 Deployment scripts"
echo "  📄 Docker configurations"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Review DEPLOYMENT_MANIFEST.json"
echo "  2. Run ./deploy_railway.sh for Railway"
echo "  3. Run ./deploy_docker.sh for Docker"
echo ""

exit 0
EOF

# Make hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push

echo "✅ Git hooks installed successfully!"
echo ""
echo "Hooks installed:"
echo "  - pre-commit: Formats code and runs tests"
echo "  - pre-push: Prepares deployment bundle and libraries"
echo ""
echo "To skip hooks temporarily, use:"
echo "  git commit --no-verify"
echo "  git push --no-verify"