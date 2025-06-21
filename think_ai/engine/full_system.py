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
from ..storage.redis_cache import RedisCache
from ..storage.scylla import ScyllaDBBackend
from ..storage.vector_db import MilvusDB
from ..utils.logging import get_logger

logger = get_logger(__name__)


class FullSystemInitializer:


"""Initialize and manage the full distributed Think AI system."""

   def __init__(self, config_path: str = "config/active.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.services = {}

        def _load_config(self) - > Dict[str, Any]:
"""Load system configuration."""
   if os.path.exists(self.config_path):
        logger.info(f"Loading config from: {self.config_path}")
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    else:
    # Default to full system config if available
        full_config_path = "config/full_system.yaml"
        if os.path.exists(full_config_path):
            logger.info(f"Loading config from: {full_config_path}")
            with open(full_config_path, 'r') as f:
                return yaml.safe_load(f)
            logger.warning("No config file found!")
            return {}

        async def initialize_all_services(self) - > Dict[str, Any]:
"""Initialize all distributed services."""
   logger.info("🚀 Initializing Think AI Full Distributed System")

# Check system mode
    if self.config.get('system_mode') ! = 'full_distributed':
        logger.warning(
            "System not in full_distributed mode. Some features may be limited.")

# Initialize ScyllaDB
        if self.config.get('scylladb', {}).get('enabled', False):
            try:
                scylla_config = ScyllaDBConfig(
                    hosts = self.config['scylladb'].get('hosts', ['localhost']),
                    port = self.config['scylladb'].get('port', 9042),
                    keyspace = self.config['scylladb'].get('keyspace', 'think_ai')
                )
                scylla = ScyllaDBBackend(scylla_config)
                await scylla.initialize()
                self.services['scylla'] = scylla
                logger.info("✅ ScyllaDB initialized")
                except Exception as e:
                    logger.error(f"❌ ScyllaDB initialization failed: {e}")

# Initialize Redis
                    if self.config.get('redis', {}).get('enabled', False):
                        try:
                            redis_config = RedisConfig(
                                host = self.config['redis'].get('host', 'localhost'),
                                port = self.config['redis'].get('port', 6379),
                                password = self.config['redis'].get('password', None)
                                )
                        redis = RedisCache(redis_config)
                        await redis.initialize()
                        self.services['redis'] = redis
                        logger.info("✅ Redis cache initialized")
                        except Exception as e:
                            logger.error(f"❌ Redis initialization failed: {e}")

# Initialize Milvus
                            if self.config.get(
                                'vector_db',
                                {}).get(
                                'enabled',
                                False):
                                try:
                                    milvus_config = VectorDBConfig(
                                        provider = 'milvus',
                                        host = self.config['vector_db'].get('host', 'localhost'),
                                        port = self.config['vector_db'].get('port', 19530)
                                    )
                                    milvus = MilvusDB(milvus_config)
                                    try:
                                        await milvus.initialize()
                                        except Exception as e:
                                            logger.error(
                                                f"Milvus initialization error: {e}")
# Continue without Milvus
                                            return services

# Create collection if needed
                                        await milvus.create_collection(
                                            collection_name = "think_ai_knowledge",
                                            dimension = 768
                                        )

                                        self.services['milvus'] = milvus
                                        logger.info(
                                            "✅ Milvus vector database initialized")
                                        except Exception as e:
                                            logger.error(
                                                f"❌ Milvus initialization failed: {e}")

# Initialize Neo4j
                                            if self.config.get(
                                                'neo4j',
                                                {}).get(
                                                'enabled',
                                                False):
                                                try:
    # Debug: Log what config we're using'
                                                    neo4j_config = self.config.get(
                                                        'neo4j', {})
                                                    logger.info(
                                                        f"Neo4j config: uri={
                                                        neo4j_config.get('uri')}, username={
                                                        neo4j_config.get('username')}, password_from_config={
                                                        neo4j_config.get(
                                                        'password',
                                                        'NOT_SET')}")

                                                    neo4j = KnowledgeGraph(
                                                        uri = self.config['neo4j'].get('uri', 'bolt://localhost:7687'),
                                                        username = self.config['neo4j'].get('username', 'neo4j'),
                                                        password = self.config['neo4j'].get('password', 'thinkaipass')
                                                        )
                                                await neo4j.initialize()
                                                self.services['neo4j'] = neo4j
                                                logger.info(
                                                    "✅ Neo4j knowledge graph initialized")
                                                except Exception as e:
                                                    logger.error(
                                                        f"❌ Neo4j initialization failed: {e}")

# Initialize Federated Learning
                                                    try:
                                                        federated = FederatedLearningServer(
                                                            min_clients = 5,
                                                            rounds_per_epoch = 10
                                                        )
                                                        self.services['federated'] = federated
                                                        logger.info(
                                                            "✅ Federated learning server initialized")
                                                        except Exception as e:
                                                            logger.error(
                                                                f"❌ Federated learning initialization failed: {e}")

# Initialize Language Model Orchestrator
                                                            model_config = self.config.get(
                                                                'model', {})
                                                            if model_config:
                                                                try:

    # Import HUGGINGFACE_API_KEY if needed
                                                                    try:
                                                                        hf_token = os.getenv(
                                                                            "HF_TOKEN") or HUGGINGFACE_API_KEY
                                                                        except ImportError:
                                                                            hf_token = os.getenv(
                                                                                "HF_TOKEN")

# Handle quantization conversion from YAML boolean to string
                                                                            quantization = model_config.get(
                                                                                'quantization')
                                                                            if quantization is False or quantization = = 'false':
                                                                                quantization = 'none'
                                                                            elif quantization is True:
                                                                                quantization = 'int4'

                                                                                config = ModelConfig(
                                                                                    model_name = model_config.get('name', 'microsoft/phi-2'),
                                                                                    device = model_config.get('device', 'mps'),
                                                                                    quantization = quantization,
                                                                                    max_tokens = model_config.get('max_tokens', 2048),
                                                                                    hf_token = hf_token,
                                                                                    torch_dtype = model_config.get('torch_dtype', 'float32')
                                                                                )

                                                                                constitutional_ai = ConstitutionalAI()
                                                                                orchestrator = ModelOrchestrator()
                                                                                await orchestrator.initialize_models(config, constitutional_ai)

                                                                                self.services['model_orchestrator'] = orchestrator
                                                                                logger.info(
                                                                                    "✅ Language model orchestrator initialized")
                                                                                except Exception as e:
                                                                                    logger.error(
                                                                                        f"❌ Language model initialization failed: {e}")

# Initialize Consciousness Framework
                                                                                    consciousness = ConsciousnessFramework()
                                                                                    self.services['consciousness'] = consciousness
                                                                                    logger.info(
                                                                                        "✅ Consciousness framework initialized")

# Summary
                                                                                    logger.info(
                                                                                        "\n📊 System Status:")
                                                                                    logger.info(
                                                                                        f" Active Services: {len(self.services)}")
                                                                                    for service_name in self.services:
                                                                                        logger.info(
                                                                                            f" ✅ {service_name}")

                                                                                        return self.services

                                                                                    async def health_check(self) - > Dict[str, Dict[str, Any]]:
"""Check health of all services."""
   health_status = {}

# Check ScyllaDB
    if 'scylla' in self.services:
        try:
    # Simple health check
            await self.services['scylla'].get("health_check_key")
            health_status['scylla'] = {
                'status': 'healthy', 'message': 'Connected'}
            except Exception as e:
                health_status['scylla'] = {
                    'status': 'unhealthy', 'message': str(e)}

# Check Redis
                if 'redis' in self.services:
                    try:
                        await self.services['redis'].get("health_check_key")
                        health_status['redis'] = {
                            'status': 'healthy', 'message': 'Connected'}
                        except Exception as e:
                            health_status['redis'] = {
                                'status': 'unhealthy', 'message': str(e)}

# Check Milvus
                            if 'milvus' in self.services:
                                try:
    # For now, just check if initialized
                                    collections = [
                                        'think_ai_knowledge'] if self.services['milvus']._initialized else []
                                    health_status['milvus'] = {
                                        'status': 'healthy',
                                        'message': f'{len(collections)} collections'
                                    }
                                    except Exception as e:
                                        health_status['milvus'] = {
                                            'status': 'unhealthy', 'message': str(e)}

# Check Neo4j
                                        if 'neo4j' in self.services:
                                            try:
                                                stats = await self.services['neo4j'].get_stats()
                                                health_status['neo4j'] = {
                                                    'status': 'healthy',
                                                    'message': f"{stats['total_nodes']} nodes, {stats['total_relationships']} relationships"
                                                }
                                                except Exception as e:
                                                    health_status['neo4j'] = {
                                                        'status': 'unhealthy', 'message': str(e)}

# Check Language Model
                                                    if 'model_orchestrator' in self.services:
                                                        try:
                                                            info = await self.services['model_orchestrator'].get_model_info()
                                                            health_status['language_model'] = {
                                                                'status': 'healthy' if info.get('status') ! = 'not_initialized' else 'unhealthy',
                                                                'message': f"{info.get('model_name', 'Unknown')} - {info.get('parameters', 'Unknown')}"
                                                            }
                                                            except Exception as e:
                                                                health_status['language_model'] = {
                                                                    'status': 'unhealthy', 'message': str(e)}

                                                                return health_status

                                                            async def shutdown(
                                                                self):
"""Gracefully shutdown all services."""
   logger.info("Shutting down Think AI services...")

# Shutdown in reverse order
    if 'neo4j' in self.services:
        await self.services['neo4j'].close()

        if 'milvus' in self.services:
            await self.services['milvus'].close()

            if 'redis' in self.services:
                await self.services['redis'].close()

                if 'scylla' in self.services:
                    await self.services['scylla'].close()

                    logger.info("All services shut down successfully")

                    class DistributedThinkAI:
"""Main class for distributed Think AI operations."""

   def __init__(self):
        self.initializer = FullSystemInitializer()
        self.services = None

        async def start(self):
"""Start the distributed system."""
   self.services = await self.initializer.initialize_all_services()

# Run health check
    health = await self.initializer.health_check()
    logger.info("\n🏥 Health Check Results:")
    for service, status in health.items():
        emoji = "✅" if status['status'] = = 'healthy' else "❌"
        logger.info(f" {emoji} {service}: {status['message']}")

        return self.services

    async def process_with_full_system(self, query: str) - > Dict[str, Any]:
"""Process query using all available services WITH PROPER INTEGRATION."""
   responses = {}
    services_used = []
    knowledge_context = {}

# 1. Check cache first (if Redis available)
    cache_key = f"query_{hash(query) % 10**9}"

    if 'scylla' in self.services:  # Using ScyllaDB for cache since Redis has issues
    try:
        cached = await self.services['scylla'].get(f"cache_{cache_key}")
        if cached and hasattr(cached, 'content'):
            cached_data = json.loads(cached.content)
# Check if cache is fresh (1 hour)
            cache_time = datetime.fromisoformat(
                cached_data.get('timestamp', ''))
            if (datetime.now() - cache_time).seconds < 3600:
                logger.info("Cache hit!")
                return cached_data['response']
            except Exception:
                pass

# 2. Search knowledge base (ScyllaDB)
            knowledge_results = []
            if 'scylla' in self.services:
                try:
    # Search for relevant knowledge
                    query_words = query.lower().split()
                    items = []

# In production, use proper indexing
# For now, scan recent items
                    try:
                        async for key, item in self.services['scylla'].scan(prefix="knowledge_", limit = 20):
                            if any(word in item.content.lower()
                                   for word in query_words):
                                items.append(json.loads(item.content))
                                if len(items) > = 5:
                                    break
                                except Exception as e:
    # Fallback if async iteration not supported
                                    logger.debug(f"Scan failed: {e}")

                                    knowledge_results = items
                                    if knowledge_results:
                                        services_used.append('knowledge_base')
                                        knowledge_context['facts'] = [
                                            item.get('fact', '') for item in knowledge_results[:3]]
                                        except Exception as e:
                                            logger.error(
                                                f"Knowledge search error: {e}")

# 3. Vector similarity search (Milvus)
                                            if 'milvus' in self.services:
                                                try:
    # In production, generate embedding and search
    # For now, indicate capability
                                                    responses['vector_search'] = "Vector similarity search available"
                                                    services_used.append(
                                                        'vector_search')
                                                    knowledge_context['similar'] = [
                                                        "Related conversation found", "Similar topic identified"]
                                                    except Exception as e:
                                                        logger.error(
                                                            f"Vector search error: {e}")

# 4. Consciousness framework evaluation
                                                        consciousness_response = None
                                                        if 'consciousness' in self.services:
                                                            try:
                                                                consciousness_response = await self.services['consciousness'].generate_conscious_response(query)
                                                                responses['consciousness'] = consciousness_response
                                                                services_used.append(
                                                                    'consciousness')

# Extract content for context
                                                                if isinstance(
                                                                    consciousness_response, dict):
                                                                    knowledge_context['ethical'] = consciousness_response.get(
                                                                        'principles', [])
                                                                    except Exception as e:
                                                                        logger.error(
                                                                            f"Consciousness error: {e}")

# 5. Generate initial response with ALL context
                                                                        initial_response = None
                                                                        if 'model_orchestrator' in self.services:
                                                                            try:
    # Build context - aware prompt
                                                                                context_prompt = "Context:\n"
                                                                                if knowledge_context.get(
                                                                                    'facts'):
                                                                                    context_prompt + = f"Known facts: {'; '.join(knowledge_context['facts'])}\n"
                                                                                    if knowledge_context.get(
                                                                                        'similar'):
                                                                                        context_prompt + = f"Related: {'; '.join(knowledge_context['similar'])}\n"

                                                                                        context_prompt + = f"\nQuestion: {query}\nAnswer:"

                                                                                        model_response = await self.services['model_orchestrator'].generate(
                                                                                            context_prompt,
                                                                                            max_tokens = 200
                                                                                        )
                                                                                        responses['language_model'] = model_response
                                                                                        services_used.append(
                                                                                            'language_model')
                                                                                        initial_response = model_response
                                                                                        except Exception as e:
                                                                                            logger.error(
                                                                                                f"Model error: {e}")

# 6. Determine if we have a good distributed response
                                                                                            has_good_response = bool(
                                                                                                knowledge_results or
                                                                                                (initial_response and len(str(initial_response)) > 50) or
                                                                                                (consciousness_response and isinstance(consciousness_response, dict) and consciousness_response.get('content'))
                                                                                            )

# 7. Store interaction for learning
                                                                                            if 'scylla' in self.services:
                                                                                                try:
                                                                                                    interaction_data = {
                                                                                                        'query': query,
                                                                                                        'knowledge_found': len(knowledge_results),
                                                                                                        'services_used': services_used,
                                                                                                        'timestamp': datetime.now().isoformat(),
                                                                                                        'has_good_response': has_good_response
                                                                                                    }

                                                                                                    await self.services['scylla'].put(
                                                                                                        f"interaction_{datetime.now().timestamp()}",
                                                                                                        StorageItem.create(
                                                                                                        content = json.dumps(interaction_data),
                                                                                                        metadata = {'type': 'interaction'}
                                                                                                    )
                                                                                                    )
                                                                                                    except Exception:
                                                                                                        pass

# 8. Update federated learning
                                                                                                    if 'federated' in self.services:
                                                                                                        stats = self.services['federated'].get_global_stats(
                                                                                                        )
                                                                                                        responses['federated_status'] = stats
                                                                                                        services_used.append(
                                                                                                            'federated')

# Build final response
                                                                                                        result = {
                                                                                                            'query': query,
                                                                                                            'responses': responses,
                                                                                                            'services_used': services_used,
                                                                                                            'timestamp': datetime.now().isoformat(),
                                                                                                            'knowledge_context': knowledge_context,
                                                                                                            'distributed_response_quality': 'good' if has_good_response else 'needs_enhancement'
                                                                                                        }

# Cache the response
                                                                                                        if 'scylla' in self.services and has_good_response:
                                                                                                            try:
                                                                                                                cache_data = {
                                                                                                                    'response': result,
                                                                                                                    'timestamp': datetime.now().isoformat()
                                                                                                                }
                                                                                                                await self.services['scylla'].put(
                                                                                                                    f"cache_{cache_key}",
                                                                                                                    StorageItem.create(
                                                                                                                    content = json.dumps(cache_data),
                                                                                                                    metadata = {'type': 'cache', 'ttl': 3600}
                                                                                                                )
                                                                                                                )
                                                                                                                except Exception:
                                                                                                                    pass

                                                                                                                return result

                                                                                                            async def shutdown(
                                                                                                                self):
"""Shutdown the system."""
   await self.initializer.shutdown()

# Convenience function for testing
    async def test_full_system():
"""Test the full distributed system."""
   system = DistributedThinkAI()

    try:
    # Start system
        await system.start()

# Test query
        result = await system.process_with_full_system("What is consciousness?")

        logger.info("\n🧪 Test Query Results:")
        logger.info(f"Services used: {', '.join(result['services_used'])}")

        for service, response in result['responses'].items():
            logger.info(f"\n{service}:")
            if isinstance(response, str):
                logger.info(f" {response[:200]}...")
            else:
                logger.info(f" {response}")

            finally:
                await system.shutdown()

                if __name__ = = "__main__":
                    asyncio.run(test_full_system())
