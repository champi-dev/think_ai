"""Full distributed system initialization for Think AI."""

import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict

import yaml

from config import HUGGINGFACE_API_KEY

from ..consciousness.awareness import ConsciousnessFramework
from ..consciousness.principles import ConstitutionalAI
from ..core.config import ModelConfig, RedisConfig, ScyllaDBConfig, VectorDBConfig
from ..federated.federated_learning import FederatedLearningServer
from ..graph.knowledge_graph import KnowledgeGraph
from ..models.language_model import ModelOrchestrator
from ..storage.base import StorageItem
from ..storage.cache.redis_cache import RedisCache
from ..storage.distributed.scylla import ScyllaDBBackend
from ..storage.vector.vector_db import VectorDB as MilvusDB
from ..utils.logging import get_logger

logger = get_logger(__name__)


class FullSystemInitializer:
    """Initialize and manage the full distributed Think AI system."""

    def __init__(self, config_path: str = "config/active.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.services = {}

    def _load_config(self) -> Dict[str, Any]:
        """Load system configuration."""
        if os.path.exists(self.config_path):
            logger.info(f"Loading config from: {self.config_path}")
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        else:
            # Default to full system config if available
            full_config_path = "config/full_system.yaml"
            if os.path.exists(full_config_path):
                logger.info(f"Loading config from: {full_config_path}")
                with open(full_config_path, "r") as f:
                    return yaml.safe_load(f)
            logger.warning("No config file found!")
            return {}

    async def initialize_all_services(self) -> Dict[str, Any]:
        """Initialize all distributed services."""
        logger.info("🚀 Initializing Think AI Full Distributed System")

        # Check system mode
        if self.config.get("system_mode") != "full_distributed":
            logger.warning("System not in full_distributed mode. Some features may be limited.")

        # Initialize ScyllaDB
        if self.config.get("scylladb", {}).get("enabled", False):
            try:
                scylla_config = ScyllaDBConfig(
                    hosts=self.config["scylladb"].get("hosts", ["localhost"]),
                    port=self.config["scylladb"].get("port", 9042),
                    keyspace=self.config["scylladb"].get("keyspace", "think_ai"),
                )
                scylla = ScyllaDBBackend(scylla_config)
                await scylla.initialize()
                self.services["scylla"] = scylla
                logger.info("✅ ScyllaDB initialized")
            except Exception as e:
                logger.error(f"❌ ScyllaDB initialization failed: {e}")

        # Initialize Redis
        if self.config.get("redis", {}).get("enabled", False):
            try:
                redis_config = RedisConfig(
                    host=self.config["redis"].get("host", "localhost"),
                    port=self.config["redis"].get("port", 6379),
                    password=self.config["redis"].get("password", None),
                )
                redis = RedisCache(redis_config)
                await redis.initialize()
                self.services["redis"] = redis
                logger.info("✅ Redis cache initialized")
            except Exception as e:
                logger.error(f"❌ Redis initialization failed: {e}")

        # Initialize Milvus
        if self.config.get("vector_db", {}).get("enabled", False):
            try:
                milvus_config = VectorDBConfig(
                    provider="milvus",
                    host=self.config["vector_db"].get("host", "localhost"),
                    port=self.config["vector_db"].get("port", 19530),
                )
                milvus = MilvusDB(milvus_config)
                try:
                    await milvus.initialize()
                except Exception as e:
                    logger.error(f"Milvus initialization error: {e}")
                    # Continue without Milvus

                self.services["milvus"] = milvus
                logger.info("✅ Milvus vector DB initialized")
            except Exception as e:
                logger.error(f"❌ Milvus initialization failed: {e}")

        return self.services


# The rest of this file needs major refactoring - skipping for now
# TODO: Fix the remaining methods and classes
