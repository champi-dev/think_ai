#! / usr / bin / env python3

"""Cache all Think AI components for instant startup."""

import asyncio
import json
import os
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from think_ai.core.config import ModelConfig
from think_ai.models.parallel_model_pool import ParallelModelPool


async def cache_model():
"""Cache the Mistral model and parallel instances."""
    print("\n🤖 Caching Mistral - 7B model...")

    cache_dir = Path.home() / ".cache" / "think_ai_models"
    cache_dir.mkdir(parents=True, exist_ok=True)

    model_name = "mistralai / Mistral - 7B - v0.1"

# Check if already cached
    model_files = list(cache_dir.glob(
    "models--mistralai--Mistral - 7B - v0.1/**/*.bin"))
    if model_files:
        print("✅ Model already cached")
    else:
        print("📥 Downloading model (13GB - this is one - time only)...")

# Download tokenizer
        AutoTokenizer.from_pretrained(
        model_name,
        cache_dir=cache_dir
        )

# Download model
        AutoModelForCausalLM.from_pretrained(
        model_name,
        cache_dir=cache_dir,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
        )

        print("✅ Model cached successfully")

# Pre - initialize parallel model pool for faster startup
        print("\n🚀 Pre - initializing parallel model pool...")

# Create config
        config = ModelConfig(
        model_name="mistralai / Mistral - 7B - v0.1",
        device="mps",
        quantization=False,
        max_tokens=2048,
        low_cpu_mem_usage=True,
        torch_dtype="float16"
        )

# Initialize pool
        pool = ParallelModelPool(config, None, pool_size=2)
        await pool.initialize()

        print("✅ Parallel model pool pre - initialized")


        def cache_knowledge_base():
"""Cache the initial knowledge base."""
            print("\n📚 Caching knowledge base...")

            cache_dir = Path.home() / ".cache" / "think_ai"
            cache_dir.mkdir(parents=True, exist_ok=True)

# Cache knowledge entries
            knowledge = {
            "consciousness": [
            "Consciousness involves self - awareness and subjective experience",
            "Global Workspace Theory suggests consciousness emerges from information integration",
            "Attention Schema Theory proposes consciousness is a model of attention",
            "Think AI implements both theories for consciousness simulation"],
            "ai_ethics": [
            "Constitutional AI provides harm prevention through 8 categories",
            "Love - based principles guide ethical decision making",
            "Transparency and explainability are core requirements",
            "User autonomy and consent must be respected"],
            "distributed_systems": [
            "ScyllaDB provides horizontally scalable NoSQL storage",
            "Redis enables sub - millisecond caching and pub / sub",
            "Milvus specializes in billion - scale vector similarity search",
            "Neo4j creates property graphs for relationship mapping"]}

            with open(cache_dir / "knowledge_base.json", "w") as f:
                json.dump(knowledge, f, indent=2)

                print("✅ Knowledge base cached")


                def setup_docker_compose():
"""Ensure docker - compose.yml is optimized."""
                    print("\n🐳 Optimizing Docker services...")

                    compose_content = """version: '3.8'

                    services:
                        scylla:
                            image: scylladb / scylla:5.2
                            container_name: think_ai_scylla
                            command: - - seeds = scylla - - smp 2 - - memory 2G
                            ports:
                                - "9042:9042"
                                volumes:
                                    - scylla_data: / var / lib / scylla
                                    restart: unless - stopped
                                    healthcheck:
                                        test: ["CMD - SHELL", "nodetool status || exit 1"]
                                        interval: 30s
                                        timeout: 10s
                                        retries: 3

                                        redis:
                                            image: redis:7 - alpine
                                            container_name: think_ai_redis
                                            command: redis - server - - appendonly yes - - maxmemory 512mb - - maxmemory - policy allkeys - lru
                                            ports:
                                                - "6379:6379"
                                                volumes:
                                                    - redis_data: / data
                                                    restart: unless - stopped
                                                    healthcheck:
                                                        test: ["CMD", "redis - cli", "ping"]
                                                        interval: 10s
                                                        timeout: 5s
                                                        retries: 3

                                                        milvus:
                                                            image: milvusdb / milvus:2.3 - cpu - latest
                                                            container_name: think_ai_milvus
                                                            environment:
                                                                ETCD_ENDPOINTS: etcd:2379
                                                                MINIO_ADDRESS: minio:9000
                                                                ports:
                                                                    - "19530:19530"
                                                                    volumes:
                                                                        - milvus_data: / var / lib / milvus
                                                                        depends_on:
                                                                            - etcd
                                                                            - minio
                                                                            restart: unless - stopped

                                                                            etcd:
                                                                                image: quay.io / coreos / etcd:v3.5.5
                                                                                container_name: think_ai_etcd
                                                                                environment:
                                                                                    ETCD_LISTEN_CLIENT_URLS: http:/ / 0.0.0.0:2379
                                                                                    ETCD_ADVERTISE_CLIENT_URLS: http:/ / etcd:2379
                                                                                    volumes:
                                                                                        - etcd_data: / etcd
                                                                                        restart: unless - stopped

                                                                                        minio:
                                                                                            image: minio / minio:latest
                                                                                            container_name: think_ai_minio
                                                                                            environment:
                                                                                                MINIO_ROOT_USER: minioadmin
                                                                                                MINIO_ROOT_PASSWORD: minioadmin
                                                                                                command: server / data
                                                                                                volumes:
                                                                                                    - minio_data: / data
                                                                                                    restart: unless - stopped

                                                                                                    volumes:
                                                                                                        scylla_data:
                                                                                                            redis_data:
                                                                                                                milvus_data:
                                                                                                                    etcd_data:
                                                                                                                        minio_data:
"""

                                                                                                                            with open("docker - compose.yml", "w") as f:
                                                                                                                                f.write(compose_content)

                                                                                                                                print("✅ Docker compose optimized")


                                                                                                                                def create_fast_launcher():
"""Create optimized launcher script."""
                                                                                                                                    print("\n🚀 Creating fast launcher...")

                                                                                                                                    launcher_content = '''#!/bin / bash

                                                                                                                                    echo "🧠 THINK AI - CONSCIOUSNESS LAUNCHER"
                                                                                                                                    echo " == == == == == == == == == == == == == == == == == == "
                                                                                                                                    echo ""

# Check for command line arguments
                                                                                                                                    if [ "$1" = "--monitor" ] || [ "$1" = "-m" ]; then
                                                                                                                                    echo "📊 Starting Self - Training Monitor..."
                                                                                                                                    echo "Press Ctrl + C to stop"
                                                                                                                                    echo ""
                                                                                                                                    python3 self_training_monitor.py
                                                                                                                                    exit 0
                                                                                                                                    fi

                                                                                                                                    if [ "$1" = "--keep - data" ] || [ "$1" = "-k" ]; then
                                                                                                                                    echo "📂 Keeping existing data and knowledge..."
                                                                                                                                    KEEP_DATA = true
                                                                                                                                    else
                                                                                                                                    KEEP_DATA = false
                                                                                                                                    fi

# Check if model is cached
                                                                                                                                    if [ ! - d "$HOME/.cache / think_ai_models / models--mistralai--Mistral - 7B - v0.1" ]; then
                                                                                                                                    echo "🤖 First time setup - caching model for faster startup..."
                                                                                                                                    python3 cache_all.py
                                                                                                                                    fi

# Ensure Docker services are running
                                                                                                                                    echo "🐳 Checking services..."
                                                                                                                                    docker - compose up - d - - quiet - pull 2 > / dev / null

# Wait for services to be ready
                                                                                                                                    echo "⏳ Waiting for services..."
                                                                                                                                    sleep 2

# Check if we're in an interactive terminal
                                                                                                                                    if [ - t 0 ]; then
                                                                                                                                    echo "✅ Interactive terminal detected"
                                                                                                                                    else
                                                                                                                                    echo "⚠️ Not in interactive terminal - launching in new terminal window"

# For macOS
                                                                                                                                    if [[ "$OSTYPE" = = "darwin" * ]]; then
                                                                                                                                    osascript - e "tell app "Terminal" to do script "cd ""$(pwd)"" && python3 full_architecture_chat.py""
                                                                                                                                    echo "✅ Launched in new Terminal window"
                                                                                                                                    else
# For Linux
                                                                                                                                    if command - v gnome - terminal & > / dev / null; then
                                                                                                                                    gnome - terminal - - bash - c "cd $(pwd) && python3 full_architecture_chat.py; exec bash"
                                                                                                                                elif command - v xterm & > / dev / null; then
                                                                                                                                xterm - e "cd $(pwd) && python3 full_architecture_chat.py; bash"
                                                                                                                                else
                                                                                                                                echo "❌ Could not find a suitable terminal emulator"
                                                                                                                                echo "Please run: python3 full_architecture_chat.py"
                                                                                                                                fi
                                                                                                                                fi
                                                                                                                                exit 0
                                                                                                                                fi

# If we're in an interactive terminal, run directly
                                                                                                                                echo "🚀 Starting consciousness chat..."

# Clean data if not keeping
                                                                                                                                if [ "$KEEP_DATA" = false ]; then
                                                                                                                                echo ""
                                                                                                                                echo "🧹 Cleaning previous data for fresh start..."

# Clear Redis
                                                                                                                                docker exec think_ai_redis redis - cli FLUSHALL > / dev / null 2 > &1

# Clear ScyllaDB
                                                                                                                                docker exec think_ai_scylla cqlsh - e "DROP KEYSPACE IF EXISTS think_ai;" > / dev / null 2 > &1

# Clear Neo4j
                                                                                                                                docker exec neo4j cypher - shell - u neo4j - p thinkaipass "MATCH (n) DETACH DELETE n" > / dev / null 2 > &1

# Clear Milvus
                                                                                                                                python3 clear_milvus_simple.py > / dev / null 2 > &1

# Clear local files
                                                                                                                                rm - f self_training_progress.json neural_pathways_intelligence.json training_output.log > / dev / null 2 > &1

                                                                                                                                echo "✨ Fresh start initialized!"
                                                                                                                                echo ""
                                                                                                                                fi

                                                                                                                                echo ""
                                                                                                                                echo "💡 Tips:"
                                                                                                                                echo " • Use ". / launch_consciousness.sh - - keep - data" to preserve knowledge"
                                                                                                                                echo " • Use ". / launch_consciousness.sh - - monitor" to see training progress"
                                                                                                                                echo ""

# Set environment for fast startup
                                                                                                                                export PYTORCH_ENABLE_MPS_FALLBACK = 1
                                                                                                                                export TOKENIZERS_PARALLELISM = false

# Run the consciousness chat
                                                                                                                                exec python3 full_architecture_chat.py
'''

                                                                                                                                with open("launch_consciousness.sh", "w") as f:
                                                                                                                                    f.write(launcher_content)

                                                                                                                                    os.chmod("launch_consciousness.sh", 0o755)
                                                                                                                                    print("✅ Fast launcher created")


                                                                                                                                    async def main():
"""Run all caching operations."""
                                                                                                                                        print("🚀 THINK AI - STARTUP OPTIMIZER")
                                                                                                                                        print(" == == == == == == == == == == == == == == == == ")
                                                                                                                                        print("This will cache everything for instant startup.")
                                                                                                                                        print("")

# Cache model
                                                                                                                                        await cache_model()

# Cache knowledge
                                                                                                                                        cache_knowledge_base()

# Setup Docker
                                                                                                                                        setup_docker_compose()

# Create launcher
                                                                                                                                        create_fast_launcher()

                                                                                                                                        print("\n✨ ALL COMPONENTS CACHED!")
                                                                                                                                        print("Think AI will now start in seconds instead of minutes.")
                                                                                                                                        print("\nRun ./launch_consciousness.sh to start!")

                                                                                                                                        if __name__ = = "__main__":
                                                                                                                                            asyncio.run(main())
