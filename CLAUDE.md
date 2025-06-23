# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Key Commands

**Development:**
- `make install` - Install all dependencies including webapp and npm packages
- `make format` - Format Python code with Black & isort, JS/TS with Prettier
- `make lint` - Run linting checks with flake8
- `make test` - Run pytest with coverage reporting
- `make coverage` - Generate detailed coverage report in htmlcov/
- `python think_ai_linter.py . --fix` - Auto-format all Python files with Think AI's O(1) linter

**Testing:**
- `pytest tests/unit/` - Run unit tests only
- `pytest tests/integration/` - Run integration tests
- `python think_ai_1000_iterations_cpu.py` - Verify O(1) performance with 1000 iterations
- `python performance_test.py` - Run performance benchmarks

**Deployment:**
- `python process_manager.py` - Start full system locally with all services
- `make docker` - Build Docker image (tries Dockerfile.railway first)
- `railway up` - Deploy to Railway (uses process_manager.py for orchestration)

## Architecture Overview

**Package Structure:**
- `think_ai/` - Main Python package
  - `api/` - FastAPI endpoints and bridge components
  - `core/` - Core engine, config, and background services
  - `consciousness/` - AI consciousness framework
  - `intelligence/` - Self-training and optimization
  - `storage/` - Vector DBs (ChromaDB, Qdrant) and storage backends
  - `models/` - Language models, embeddings, caching
  - `coding/` - Code generation and autonomous coding
  - `cli/` - Command-line interface
  - `utils/` - Logging, GPU detection, complexity analysis

**Key Services:**
- `process_manager.py` - Orchestrates API server (port 8080) and webapp (port 3000)
- `railway_server.py` - Minimal FastAPI server for Railway deployment
- `think_ai_simple_chat.py` - Interactive CLI with O(1) hash-based responses

**Performance Core:**
- `o1_vector_search.py` - O(1) vector search using LSH (Locality-Sensitive Hashing)
- `o1_think_ai_core.py` - Core O(1) performance implementation
- Average search time: 0.18ms (verified with 1000 iterations)
- 88.8 iterations/second sustained throughput

**Testing Strategy:**
- Use pytest with coverage reporting (configured in pyproject.toml)
- Test files follow pattern: test_*.py
- Coverage target: 80%+ (set in pyproject.toml)
- Performance tests verify O(1) guarantees

**Code Quality:**
- Python formatting: Black with 120 line length
- Import sorting: isort with Black profile
- Linting: flake8, ruff, mypy
- Pre-commit hooks installed via `make install`
- Think AI Linter provides O(1) performance linting

**Deployment Notes:**
- Railway: Uses process_manager.py to handle multi-service deployment
- Docker: Optimized base image with requirements-fast.txt
- No GPU required - 100% CPU-based with NumPy fallback
- Automatic FAISS to NumPy fallback when FAISS unavailable