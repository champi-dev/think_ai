# Think AI Full Distributed System Setup Guide

## 🚀 Quick Start

### 1. Install Docker Desktop

Since Docker is not installed on your Mac, you need to install it first:

```bash
# Option 1: Download from Docker website
# Visit: https://www.docker.com/products/docker-desktop/
# Download Docker Desktop for Mac (Apple Silicon)

# Option 2: Install via Homebrew (if you have it)
brew install --cask docker
```

After installation:
1. Open Docker Desktop
2. Wait for it to start (you'll see the whale icon in your menu bar)
3. Make sure Docker is running

### 2. Start the Full System

Once Docker is running:

```bash
# Run the installation script
./scripts/install_docker_mac.sh
```

This script will:
- ✅ Check Docker installation
- ✅ Pull all required images (ScyllaDB, Redis, Milvus, Neo4j)
- ✅ Create data directories
- ✅ Start all services
- ✅ Initialize databases

### 3. Install Python Dependencies

Make sure you have all required Python packages:

```bash
pip install -r requirements.txt

# Additional packages for full system
pip install pymilvus neo4j cassandra-driver redis
```

### 4. Test the Full System

```bash
# Run the full system test
python test_full_system.py

# Or use the full system CLI
python full_system_cli.py
```

## 📊 System Architecture

The full distributed Think AI system includes:

1. **ScyllaDB** (Port 9042)
   - O(1) primary storage
   - Handles billions of knowledge entries
   - Distributed, fault-tolerant

2. **Redis** (Port 6379)
   - High-performance caching
   - Real-time data access
   - Session management

3. **Milvus** (Port 19530)
   - Vector database for semantic search
   - 768-dimensional embeddings
   - HNSW indexing for fast similarity search

4. **Neo4j** (Port 7474/7687)
   - Knowledge graph database
   - Relationship mapping
   - Concept clustering

5. **Language Model** (Local)
   - Microsoft Phi-2 (2.7B parameters)
   - Optimized for Apple Silicon
   - No quantization for better quality

## 🧠 Using the Full System

### CLI Commands

```bash
# Start the full system CLI
python full_system_cli.py
```

Available commands:
- `query <text>` - Process with all distributed services
- `health` - Check service health
- `services` - List active services
- `claude <text>` - Direct Claude API query
- `memory` - Show eternal memory status
- `cost` - Show cost tracking
- `exit` - Graceful shutdown

### Example Queries

```
🧠 > query What is consciousness?
🔄 Processing with full distributed system...
📊 Services used: consciousness, language_model, neo4j
...

🧠 > query How does distributed AI work?
🔄 Processing with full distributed system...
📊 Services used: consciousness, language_model, milvus, neo4j
...
```

## 🔧 Configuration

The full system uses `config/full_system.yaml`:

```yaml
system_mode: "full_distributed"
budget_profile: "power_user"

# All services enabled
scylladb:
  enabled: true
redis:
  enabled: true
vector_db:
  enabled: true
neo4j:
  enabled: true
```

## 💾 Memory Usage

With all services running:
- Docker containers: ~4-6GB RAM
- Language model: ~2-3GB RAM
- Total: ~6-8GB RAM (as requested)

## 🛑 Stopping the System

```bash
# Stop all Docker services
docker-compose -f docker-compose.full.yml down

# Stop and remove all data (careful!)
docker-compose -f docker-compose.full.yml down -v
```

## 🐛 Troubleshooting

### Docker Not Running
```
❌ Docker is installed but not running
```
Solution: Open Docker Desktop and wait for it to start

### Service Connection Errors
```
❌ ScyllaDB initialization failed: Connection refused
```
Solution: Wait longer for services to start, or check Docker logs:
```bash
docker-compose -f docker-compose.full.yml logs scylla
```

### Memory Issues
If you run out of memory:
1. Stop other applications
2. Reduce service memory in docker-compose.full.yml
3. Use lightweight mode instead

### Python Import Errors
```bash
# Make sure you're in the Think AI directory
cd /Users/champi/Development/Think_AI

# Install missing packages
pip install -r requirements.txt
```

## 🎯 Next Steps

1. **Populate Knowledge Base**
   ```python
   # Use the full system to add knowledge
   🧠 > query Remember that consciousness emerges from integrated information
   ```

2. **Enable Federated Learning**
   - Register clients for distributed learning
   - Start federated rounds

3. **Build Knowledge Graph**
   - Import existing knowledge
   - Create concept relationships

4. **Integrate Claude as Internal Tool**
   - Claude will be used by Think AI internally
   - Not exposed directly to end users

## 📈 Performance Tips

1. **Warm Up Services**
   - First queries may be slower
   - Services optimize over time

2. **Monitor Resources**
   ```bash
   # Check Docker resource usage
   docker stats
   ```

3. **Optimize Queries**
   - Use specific, focused questions
   - Leverage the knowledge graph

## 🔒 Security Note

- Neo4j password: `think_ai_2024`
- Change this in production!
- All services are localhost-only by default

---

Ready to experience the full power of Think AI! 🚀