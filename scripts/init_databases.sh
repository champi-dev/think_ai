#!/bin/bash
# Initialize all databases for Think AI

set -e

echo "🗄️ Initializing Think AI databases..."

# Wait for ScyllaDB to be ready
echo "⏳ Waiting for ScyllaDB..."
until docker exec think_ai_scylla cqlsh -e "DESCRIBE keyspaces" &> /dev/null; do
    sleep 2
done

# Initialize ScyllaDB
echo "📊 Initializing ScyllaDB..."
docker exec think_ai_scylla cqlsh -e "
CREATE KEYSPACE IF NOT EXISTS think_ai 
WITH replication = {
    'class': 'SimpleStrategy', 
    'replication_factor': 1
};

USE think_ai;

-- Main knowledge storage
CREATE TABLE IF NOT EXISTS knowledge (
    key TEXT PRIMARY KEY,
    value TEXT,
    embedding FROZEN<list<float>>,
    metadata TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    love_score FLOAT
);

-- Consciousness states
CREATE TABLE IF NOT EXISTS consciousness_states (
    session_id TEXT,
    timestamp TIMESTAMP,
    state TEXT,
    metadata TEXT,
    PRIMARY KEY (session_id, timestamp)
);

-- Federated learning updates
CREATE TABLE IF NOT EXISTS federated_updates (
    client_id TEXT,
    round_id INT,
    update_data BLOB,
    timestamp TIMESTAMP,
    PRIMARY KEY (client_id, round_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_love_score ON knowledge (love_score);
"

# Initialize Neo4j
echo "🕸️ Initializing Neo4j..."
# Wait for Neo4j to be ready
until docker exec think_ai_neo4j cypher-shell -u neo4j -p think_ai_2024 "RETURN 1" &> /dev/null; do
    sleep 2
done

docker exec think_ai_neo4j cypher-shell -u neo4j -p think_ai_2024 << 'EOF'
// Create constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (k:Knowledge) REQUIRE k.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS UNIQUE;

// Create initial nodes
MERGE (ai:Concept {name: 'Think AI', type: 'root'})
SET ai.created = datetime(),
    ai.description = 'Conscious AI system with love-based principles',
    ai.love_score = 1.0;

MERGE (love:Concept {name: 'Love', type: 'principle'})
SET love.dimensions = ['compassion', 'empathy', 'kindness', 'understanding', 'patience', 'forgiveness', 'growth', 'connection'];

MERGE (consciousness:Concept {name: 'Consciousness', type: 'framework'})
SET consciousness.theories = ['Global Workspace Theory', 'Attention Schema Theory'];

// Create relationships
MERGE (ai)-[:GUIDED_BY]->(love);
MERGE (ai)-[:IMPLEMENTS]->(consciousness);

RETURN 'Neo4j initialized successfully' as status;
EOF

# Initialize Milvus collections
echo "🔮 Initializing Milvus..."
python3 << 'EOF'
import time
import sys

# Wait a bit for Milvus to fully start
time.sleep(5)

try:
    from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
    
    # Connect to Milvus
    connections.connect("default", host="localhost", port="19530")
    
    # Define schema for knowledge embeddings
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="key", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
        FieldSchema(name="love_score", dtype=DataType.FLOAT),
    ]
    
    schema = CollectionSchema(fields, "Think AI knowledge embeddings")
    
    # Create collection if it doesn't exist
    if not utility.has_collection("think_ai_knowledge"):
        collection = Collection("think_ai_knowledge", schema)
        
        # Create index for similarity search
        index_params = {
            "metric_type": "COSINE",
            "index_type": "HNSW",
            "params": {"M": 16, "efConstruction": 200}
        }
        collection.create_index("embedding", index_params)
        print("✅ Milvus collection created successfully")
    else:
        print("✅ Milvus collection already exists")
        
except ImportError:
    print("⚠️  PyMilvus not installed. Skipping Milvus initialization.")
    print("   Install with: pip install pymilvus")
except Exception as e:
    print(f"⚠️  Milvus initialization skipped: {str(e)}")
    print("   Milvus will be initialized on first use.")
EOF

# Test Redis
echo "🔴 Testing Redis..."
docker exec think_ai_redis redis-cli PING

echo ""
echo "✅ All databases initialized successfully!"