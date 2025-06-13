# Think AI

A comprehensive AI system for universal knowledge access with O(1) performance, offline capabilities, and consciousness-aware design.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)
![Status](https://img.shields.io/badge/status-alpha-orange.svg)

## Features

- **O(1) Performance**: ScyllaDB primary storage with Redis caching layer
- **Semantic Search**: Vector similarity search using Milvus/Qdrant with transformer embeddings
- **Knowledge Graph**: Neo4j-powered semantic relationships and concept mapping
- **Beautiful Terminal UI**: Rich interactive interface built with Textual framework
- **Offline Operation**: SQLite-based local storage with full-text search
- **Consciousness-Aware**: Global Workspace Theory and Attention Schema implementation
- **Constitutional AI**: Multi-layered harm prevention with love-based metrics
- **Open Source**: Apache 2.0 licensed core infrastructure

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Terminal UI (Textual)              │
├─────────────────────────────────────────────────────┤
│     Consciousness Framework │ Constitutional AI      │
├─────────────────────────────────────────────────────┤
│                  Knowledge Query API                 │
├─────────────────────────────────────────────────────┤
│   Redis Cache │ Vector DB │ Neo4j Graph │ SQLite    │
├─────────────────────────────────────────────────────┤
│           ScyllaDB Primary Storage (O(1))           │
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

# Neo4j Graph Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# Model Configuration
MODEL_NAME=EleutherAI/pythia-2.8b

# Consciousness Settings
ENABLE_COMPASSION_METRICS=true
LOVE_BASED_DESIGN=true
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

#### Consciousness Examples

```bash
# Run consciousness-aware features demo
python example_consciousness.py
```

This demonstrates:
- 🛡️ Multi-layered harm prevention
- ❤️ Love-based content enhancement
- 🧠 Consciousness state management
- 🌐 Knowledge graph relationships
- 🧘 AI meditation and reflection

#### Advanced Features

```bash
# Performance benchmarking
think-ai benchmark --quick  # Run quick benchmark
think-ai benchmark --full   # Run comprehensive benchmark

# Offline sync management
think-ai offline status              # Check offline storage status
think-ai offline sync               # Basic sync to online
think-ai offline smart-sync         # Sync with conflict resolution
think-ai offline enable-offline     # Enable offline-first mode

# Federated learning
think-ai federated start-server                    # Start FL server
think-ai federated register-client --client-id alice  # Register client
think-ai federated submit-update --client-id alice    # Submit update
```

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

### Phase 2: Core Development (Completed ✅)
- ✅ Knowledge graph with Neo4j
- ✅ Constitutional AI principles with harm prevention
- ✅ Love-based metrics and compassionate AI
- ✅ Consciousness framework (GWT + AST)
- ✅ Multi-layered ethical evaluation

### Phase 3: Advanced Features (Completed ✅)
- ✅ Model integration (3B parameter quantized with INT4/INT8)
- ✅ Federated learning infrastructure with differential privacy
- ✅ Advanced offline sync with conflict resolution
- ✅ Performance benchmarking suite
- ✅ Love-based federated learning metrics

### Phase 4: Future Innovations (Current)
- [ ] Learned index structures for true O(1)
- [ ] Memory-centric computing integration
- [ ] Plugin architecture for extensibility
- [ ] Multi-modal support (vision, audio)
- [ ] Quantum-classical hybrid algorithms

### Phase 5: Ecosystem Growth
- [ ] Developer documentation
- [ ] Community governance model
- [ ] Global benchmarks leaderboard
- [ ] Educational resources

### Phase 6: Global Scale
- [ ] Production deployment at scale
- [ ] Distributed knowledge federation
- [ ] Global community network
- [ ] Universal access achievement

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