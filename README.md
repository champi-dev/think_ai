# Think AI

A comprehensive AI system for universal knowledge access with O(1) performance, offline capabilities, and consciousness-aware design.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)
![Status](https://img.shields.io/badge/status-alpha-orange.svg)

## Features

- **O(1) Performance**: ScyllaDB primary storage with Redis caching layer
- **Semantic Search**: Vector similarity search using Milvus/Qdrant with transformer embeddings
- **Beautiful Terminal UI**: Rich interactive interface built with Textual framework
- **Offline Operation**: SQLite-based local storage with full-text search
- **Consciousness-Aware**: Love-based design with harm prevention
- **Open Source**: Apache 2.0 licensed core infrastructure

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Terminal UI (Textual)              │
├─────────────────────────────────────────────────────┤
│                  Knowledge Query API                 │
├─────────────────────────────────────────────────────┤
│      Redis Cache     │    Vector DB    │   Graph DB │
├─────────────────────────────────────────────────────┤
│                ScyllaDB Primary Storage             │
├─────────────────────────────────────────────────────┤
│                Offline Storage (SQLite)             │
└─────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/think-ai/think-ai.git
cd think-ai

# Run the setup script (starts Docker services)
./scripts/setup.sh

# Or manually:
# 1. Start services
docker-compose up -d

# 2. Install dependencies
pip install -e ".[dev]"
```

### Configuration

Create a `.env` file:

```env
# ScyllaDB Configuration
SCYLLA_HOSTS=localhost
SCYLLA_KEYSPACE=think_ai

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Vector DB Configuration
VECTOR_DB_PROVIDER=milvus
VECTOR_DB_HOST=localhost

# Model Configuration
MODEL_NAME=EleutherAI/pythia-2.8b
```

### Usage

#### Command Line Interface

```bash
# Initialize the system
think-ai init

# Store knowledge
think-ai store "quantum_computing" "Quantum computing uses quantum phenomena..."
think-ai store "machine_learning" "Machine learning is a subset of AI..." -m '{"category": "AI"}'

# Retrieve knowledge
think-ai get "quantum_computing"

# Semantic search (searches by meaning)
think-ai query "artificial intelligence concepts"

# Prefix search
think-ai query "prefix:machine"

# Check system health
think-ai health

# View statistics
think-ai stats
```

#### Terminal User Interface

```bash
# Launch the beautiful TUI
think-ai tui

# Or run the example
python example_tui.py
```

The TUI provides:
- 🔍 Interactive knowledge search with semantic similarity
- 💾 Easy knowledge storage with metadata
- 📊 Real-time system statistics
- ⌨️ Keyboard shortcuts for efficiency
- 🎨 Beautiful dark theme with colors

## Development Roadmap

### Phase 1: Foundation (Completed ✅)
- ✅ Project structure and configuration
- ✅ ScyllaDB integration for O(1) storage
- ✅ Redis caching layer
- ✅ Vector database integration (Milvus/Qdrant)
- ✅ Semantic search with transformer embeddings
- ✅ Beautiful Terminal UI with Textual
- ✅ Offline SQLite storage with FTS5
- ✅ Basic CLI interface

### Phase 2: Core Development (Current)
- [ ] Knowledge graph with Neo4j
- [ ] Model integration (3B parameter quantized)
- [ ] Constitutional AI principles
- [ ] Federated learning infrastructure
- [ ] Advanced offline sync capabilities

### Phase 3: Ecosystem Growth
- [ ] Plugin architecture
- [ ] Developer documentation
- [ ] Community governance model
- [ ] Performance benchmarks

### Phase 4: Global Scale
- [ ] Learned index structures
- [ ] Memory-centric computing
- [ ] Multi-modal support
- [ ] Production deployment

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

Think AI is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## Support

- Documentation: [docs.think-ai.org](https://docs.think-ai.org)
- Issues: [GitHub Issues](https://github.com/think-ai/think-ai/issues)
- Community: [Discord](https://discord.gg/think-ai)

## Acknowledgments

Built with love by the Think AI Foundation, inspired by principles of universal knowledge access and compassionate AI design.