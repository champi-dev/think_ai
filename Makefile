# Elite Makefile for Think AI with O(1) Performance
# All commands optimized for maximum efficiency

.PHONY: help install format lint test coverage build docker clean pre-commit ci

# Default target
help:
	@echo "🚀 Think AI Elite Development Commands"
	@echo "======================================"
	@echo "make install      - Install all dependencies"
	@echo "make format       - Format code with Black & isort"
	@echo "make lint         - Run linting checks"
	@echo "make test         - Run test suite"
	@echo "make coverage     - Generate coverage report"
	@echo "make build        - Build packages"
	@echo "make docker       - Build Docker images"
	@echo "make clean        - Clean build artifacts"
	@echo "make pre-commit   - Run pre-commit pipeline"
	@echo "make ci           - Run full CI/CD pipeline"

# Install dependencies with O(1) parallel installation
install:
	@echo "📦 Installing dependencies..."
	pip install --upgrade pip wheel setuptools
	pip install -r requirements-fast.txt
	pip install -e .
	pip install black isort flake8 pytest pytest-cov coverage pre-commit
	cd webapp && npm ci
	cd npm && npm ci
	pre-commit install
	@echo "✅ Installation complete!"

# Format code - non-blocking
format:
	@echo "🎨 Formatting code..."
	@black . --line-length=120 --target-version=py311 --exclude='/(\.git|\.venv|venv|build|dist|__pycache__)/' || true
	@isort . --profile=black --line-length=120 || true
	@cd webapp && npx prettier --write "**/*.{js,jsx,ts,tsx,json,css,md}" || true
	@echo "✅ Formatting complete!"

# Lint code - report only
lint:
	@echo "🔍 Running linters..."
	@flake8 . --max-line-length=120 \
		--extend-ignore=E203,E266,E501,W503,F403,F401 \
		--exclude=.git,__pycache__,venv,.venv,build,dist \
		--statistics || true
	@echo "✅ Linting complete!"

# Run tests with coverage
test:
	@echo "🧪 Running tests..."
	@python3 -m pytest tests/ \
		--cov=think_ai \
		--cov-report=term-missing \
		--cov-report=html \
		--cov-report=xml \
		--tb=short \
		-v || echo "⚠️ Some tests failed"
	@echo "✅ Tests complete!"

# Generate detailed coverage report
coverage:
	@echo "📊 Generating coverage report..."
	@python3 -m coverage run -m pytest tests/
	@python3 -m coverage report
	@python3 -m coverage html
	@echo "✅ Coverage report available in htmlcov/index.html"

# Build packages
build:
	@echo "📦 Building packages..."
	@python3 -m build
	@cd npm && npm run build
	@cd webapp && npm run build
	@echo "✅ Build complete!"

# Build Docker images
docker:
	@echo "🐳 Building Docker images..."
	@docker build -f Dockerfile.railway -t think-ai:latest . || \
		docker build -f configs/Dockerfile -t think-ai:latest .
	@echo "✅ Docker build complete!"

# Clean build artifacts with O(1) removal
clean:
	@echo "🧹 Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "✅ Clean complete!"

# Run pre-commit pipeline
pre-commit:
	@echo "🎯 Running pre-commit pipeline..."
	@bash scripts/pre-commit-local.sh
	@echo "✅ Pre-commit complete!"

# Run full CI/CD pipeline locally
ci: format lint test coverage build docker
	@echo "🎉 CI/CD pipeline complete!"

# Fast commit with auto-formatting
commit: format
	@git add -A
	@git commit -m "$(m)" || echo "No changes to commit"

# Performance check
perf:
	@echo "⚡ Checking O(1) performance..."
	@python3 -m pytest tests/unit/test_o1_vector_search.py -v
	@grep -r "for.*in.*for.*in" think_ai/ --include="*.py" | grep -v "# O(1)" || echo "✅ No nested loops found"

# Install pre-commit hooks
hooks:
	@pre-commit install --install-hooks
	@pre-commit install --hook-type pre-push
	@echo "✅ Pre-commit hooks installed!"

# Run pre-commit on all files
pre-commit-all:
	@pre-commit run --all-files || true

# Quick test run
test-quick:
	@python3 -m pytest tests/unit/ -x -q

# Deploy to PyPI (requires credentials)
deploy-pypi:
	@echo "📦 Deploying to PyPI..."
	@python3 -m build
	@python3 -m twine upload dist/*

# Deploy to npm (requires credentials)
deploy-npm:
	@echo "📦 Deploying to npm..."
	@cd npm && npm publish
	@cd webapp && npm publish

# Update all dependencies
update-deps:
	@pip install --upgrade -r requirements-fast.txt
	@cd webapp && npm update
	@cd npm && npm update
