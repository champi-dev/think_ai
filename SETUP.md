# Think AI Setup Guide

## Prerequisites

- macOS with Apple Silicon (M1/M2/M3)
- Python 3.10 or higher
- Docker Desktop
- 16GB+ RAM

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/champi-dev/think_ai.git
   cd think_ai
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Think AI**:
   ```bash
   pip install -e .
   ```

4. **Start Docker services**:
   ```bash
   docker-compose up -d
   ```

5. **Wait for services to initialize** (about 30 seconds)

6. **Launch Think AI**:
   ```bash
   ./launch_consciousness.sh
   ```

## Configuration

The system uses `config/full_system.yaml` for all settings. Key configurations:

- **Model**: Qwen2.5-Coder-1.5B (requires ~3GB RAM)
- **Device**: MPS (Apple Silicon GPU)
- **Services**: ScyllaDB, Redis, Milvus, Neo4j

## Troubleshooting

- **Memory errors**: Ensure you have at least 16GB RAM free
- **Neo4j auth errors**: Check password in config matches Docker
- **MPS errors**: Update macOS and PyTorch to latest versions

## Reset System

To completely reset Think AI:
```bash
python reset_intelligence.py
```
