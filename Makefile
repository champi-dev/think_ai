# Think AI Makefile - Local Development & CI/CD

.PHONY: help install test lint ci gpu-test clean docker-up docker-down

# Default target
help:
	@echo "🚀 Think AI Local Development Commands"
	@echo "====================================="
	@echo "make install    - Install all dependencies"
	@echo "make test       - Run all tests"
	@echo "make lint       - Run linter"
	@echo "make ci         - Run full local CI/CD pipeline"
	@echo "make gpu-test   - Run GPU-specific tests"
	@echo "make docker-up  - Start local services (Redis, ScyllaDB, Neo4j)"
	@echo "make docker-down- Stop local services"
	@echo "make clean      - Clean cache and temp files"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	python -m pip install --upgrade pip
	pip install -r requirements-fast.txt
	pip install -e .
	@echo "✅ Installation complete!"

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short

# Run linter
lint:
	@echo "🔍 Running linter..."
	python think_ai_linter.py --check

# Full local CI/CD pipeline
ci:
	@echo "🚀 Running local CI/CD pipeline..."
	./run_local_ci.sh

# GPU-specific tests
gpu-test:
	@echo "🎮 Running GPU tests..."
	@if command -v nvidia-smi &> /dev/null; then \
		echo "✅ GPU detected"; \
		CUDA_VISIBLE_DEVICES=0 pytest tests/ -v -k "gpu" --benchmark-only; \
	else \
		echo "❌ No GPU detected"; \
		exit 1; \
	fi

# Start Docker services
docker-up:
	@echo "🐳 Starting Docker services..."
	docker-compose -f docker/docker-compose.local.yml up -d
	@echo "✅ Services started!"
	@echo "   ScyllaDB: localhost:9042"
	@echo "   Redis: localhost:6379"
	@echo "   Neo4j: localhost:7474 (browser), localhost:7687 (bolt)"

# Stop Docker services
docker-down:
	@echo "🛑 Stopping Docker services..."
	docker-compose -f docker/docker-compose.local.yml down
	@echo "✅ Services stopped!"

# Clean cache and temporary files
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	rm -rf build/ dist/ *.egg-info
	@echo "✅ Cleanup complete!"

# Quick test - only fast tests
quick-test:
	@echo "⚡ Running quick tests..."
	pytest tests/unit -v --tb=short -m "not slow"

# Benchmark
benchmark:
	@echo "📊 Running benchmarks..."
	pytest tests/performance -v --benchmark-only

# Install pre-commit hooks
install-hooks:
	@echo "🪝 Installing pre-commit hooks..."
	pre-commit install
	@echo "✅ Hooks installed!"

# Run specific test file
test-file:
	@echo "🧪 Running specific test file..."
	@echo "Usage: make test-file FILE=tests/unit/test_something.py"
	pytest $(FILE) -v --tb=short

# Development server
dev:
	@echo "🚀 Starting development server..."
	python -m think_ai.server --reload --debug

# Build Docker image
docker-build:
	@echo "🏗️ Building Docker image..."
	docker build -t think-ai:local .
	@echo "✅ Image built: think-ai:local"

# Format code
format:
	@echo "🎨 Formatting code..."
	black think_ai tests
	isort think_ai tests
	@echo "✅ Code formatted!"

# Security scan
security:
	@echo "🔒 Running security scan..."
	pip install bandit safety
	bandit -r think_ai -f json -o security-report.json
	safety check --json
	@echo "✅ Security scan complete!"