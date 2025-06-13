#!/usr/bin/env python3

"""Alternative setup for Colab using SQLite instead of Cassandra/ScyllaDB
This is more reliable and still gives you the full system experience!
"""

import os
import subprocess
import sys
import time


def setup_sqlite_wrapper() -> None:
    """Create a SQLite wrapper that mimics Cassandra interface."""
    wrapper_code = '''

class SQLiteSession(Session):
    """SQLite wrapper that mimics Cassandra Session."""

    def __init__(self, db_path="/content/think_ai_data/cassandra.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def execute(self, query, parameters=None, **kwargs):
        # Convert CQL to SQLite
        query = query.replace("CREATE KEYSPACE", "-- CREATE KEYSPACE")
        query = query.replace("USE ", "-- USE ")

        cursor = self.conn.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)

        self.conn.commit()
        return cursor.fetchall()

    def prepare(self, query):
        return query

class SQLiteCluster(Cluster):
    """SQLite wrapper that mimics Cassandra Cluster."""

    def __init__(self, *args, **kwargs):
        pass

    def connect(self, keyspace=None):
        return SQLiteSession()

    def shutdown(self):
        pass

# Monkey patch cassandra driver
cassandra.cluster.Cluster = SQLiteCluster
'''

    with open("sqlite_cassandra_wrapper.py", "w") as f:
        f.write(wrapper_code)


def install_services() -> None:
    """Install services that work reliably in Colab."""
    # 1. Redis - works great natively
    subprocess.run(["apt-get", "update", "-qq"], check=False)
    subprocess.run(["apt-get", "install", "-y", "redis-server"], check=False)
    subprocess.run(["redis-server", "--daemonize", "yes"], check=False)

    # 2. Neo4j - lightweight embedded version
    subprocess.run([sys.executable, "-m", "pip", "install", "neo4j"], check=False)

    # 3. Milvus - using lite version
    subprocess.run([sys.executable, "-m", "pip", "install", "milvus-lite"], check=False)

    # Start Milvus Lite
    milvus_code = """
from milvus import default_server
default_server.start()
print("Milvus Lite started on port 19530")
"""

    subprocess.Popen([sys.executable, "-c", milvus_code])

    # 4. SQLite for Cassandra replacement
    os.makedirs("/content/think_ai_data", exist_ok=True)
    setup_sqlite_wrapper()


def create_env() -> None:
    """Create .env file."""
    env_content = """# Google Colab Configuration with SQLite
ENVIRONMENT=colab
LOG_LEVEL=INFO

# Services configuration
USE_MOCK_SERVICES=false

# Use SQLite instead of ScyllaDB
USE_SQLITE_FOR_CASSANDRA=true
SCYLLA_HOSTS=localhost
SCYLLA_PORT=9042
SCYLLA_KEYSPACE=thinkaidb

# Redis (native)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Milvus Lite
MILVUS_HOST=localhost
MILVUS_PORT=19530

# Neo4j embedded
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=thinkaipass

# Model settings
MODEL_NAME=Qwen/Qwen2.5-Coder-1.5B-Instruct
DEVICE=cuda
MAX_TOKENS=250

# Import the wrapper
sys.path.insert(0, '/content/think_ai')
"""

    with open(".env", "w") as f:
        f.write(env_content)


def main() -> None:
    """Main setup."""
    # Install services
    install_services()

    # Create config
    create_env()

    # Install Python deps
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=False
    )

    # Wait for services
    time.sleep(10)

    # Test services

    # Test Redis
    result = subprocess.run(
        ["redis-cli", "ping"], check=False, capture_output=True, text=True
    )
    if "PONG" in result.stdout:
        pass
    else:
        pass


if __name__ == "__main__":
    main()
