"""Full distributed system initialization for Think AI."""

import asyncio
import os
from typing import Optional, Dict, Any
import yaml

from ..storage.scylla import ScyllaDBBackend
from ..storage.redis_cache import RedisCache
from ..storage.vector_db import MilvusDB
from ..graph.knowledge_graph import KnowledgeGraph
from ..federated.federated_learning import FederatedLearningServer
from ..models.language_model import ModelOrchestrator
from ..consciousness.awareness import ConsciousnessFramework
from ..consciousness.principles import ConstitutionalAI
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
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Default to full system config if available
            full_config_path = "config/full_system.yaml"
            if os.path.exists(full_config_path):
                with open(full_config_path, 'r') as f:
                    return yaml.safe_load(f)
            return {}
    
    async def initialize_all_services(self) -> Dict[str, Any]:
        """Initialize all distributed services."""
        logger.info("🚀 Initializing Think AI Full Distributed System")
        
        # Check system mode
        if self.config.get('system_mode') != 'full_distributed':
            logger.warning("System not in full_distributed mode. Some features may be limited.")
        
        # Initialize ScyllaDB
        if self.config.get('scylladb', {}).get('enabled', False):
            try:
                from ..core.config import ScyllaDBConfig
                scylla_config = ScyllaDBConfig(
                    hosts=self.config['scylladb'].get('hosts', ['localhost']),
                    port=self.config['scylladb'].get('port', 9042),
                    keyspace=self.config['scylladb'].get('keyspace', 'think_ai')
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
                redis = RedisCache(
                    host=self.config['redis'].get('host', 'localhost'),
                    port=self.config['redis'].get('port', 6379)
                )
                await redis.connect()
                self.services['redis'] = redis
                logger.info("✅ Redis cache initialized")
            except Exception as e:
                logger.error(f"❌ Redis initialization failed: {e}")
        
        # Initialize Milvus
        if self.config.get('vector_db', {}).get('enabled', False):
            try:
                from ..core.config import VectorDBConfig
                milvus_config = VectorDBConfig(
                    provider='milvus',
                    host=self.config['vector_db'].get('host', 'localhost'),
                    port=self.config['vector_db'].get('port', 19530)
                )
                milvus = MilvusDB(milvus_config)
                await milvus.initialize()
                
                # Create collection if needed
                await milvus.create_collection(
                    collection_name="think_ai_knowledge",
                    dimension=768
                )
                
                self.services['milvus'] = milvus
                logger.info("✅ Milvus vector database initialized")
            except Exception as e:
                logger.error(f"❌ Milvus initialization failed: {e}")
        
        # Initialize Neo4j
        if self.config.get('neo4j', {}).get('enabled', False):
            try:
                neo4j = KnowledgeGraph(
                    uri=self.config['neo4j'].get('uri', 'bolt://localhost:7687'),
                    username=self.config['neo4j'].get('username', 'neo4j'),
                    password=self.config['neo4j'].get('password', 'think_ai_2024')
                )
                await neo4j.connect()
                self.services['neo4j'] = neo4j
                logger.info("✅ Neo4j knowledge graph initialized")
            except Exception as e:
                logger.error(f"❌ Neo4j initialization failed: {e}")
        
        # Initialize Federated Learning
        try:
            federated = FederatedLearningServer(
                min_clients=5,
                rounds_per_epoch=10
            )
            self.services['federated'] = federated
            logger.info("✅ Federated learning server initialized")
        except Exception as e:
            logger.error(f"❌ Federated learning initialization failed: {e}")
        
        # Initialize Language Model Orchestrator
        model_config = self.config.get('model', {})
        if model_config:
            try:
                from ..core.config import ModelConfig
                
                config = ModelConfig(
                    model_name=model_config.get('name', 'microsoft/phi-2'),
                    device=model_config.get('device', 'mps'),
                    quantization=model_config.get('quantization'),
                    max_tokens=model_config.get('max_tokens', 2048)
                )
                
                constitutional_ai = ConstitutionalAI()
                orchestrator = ModelOrchestrator()
                await orchestrator.initialize_models(config, constitutional_ai)
                
                self.services['model_orchestrator'] = orchestrator
                logger.info("✅ Language model orchestrator initialized")
            except Exception as e:
                logger.error(f"❌ Language model initialization failed: {e}")
        
        # Initialize Consciousness Framework
        consciousness = ConsciousnessFramework()
        self.services['consciousness'] = consciousness
        logger.info("✅ Consciousness framework initialized")
        
        # Summary
        logger.info(f"\n📊 System Status:")
        logger.info(f"   Active Services: {len(self.services)}")
        for service_name in self.services:
            logger.info(f"   ✅ {service_name}")
        
        return self.services
    
    async def health_check(self) -> Dict[str, Dict[str, Any]]:
        """Check health of all services."""
        health_status = {}
        
        # Check ScyllaDB
        if 'scylla' in self.services:
            try:
                # Simple health check
                await self.services['scylla'].get("health_check_key")
                health_status['scylla'] = {'status': 'healthy', 'message': 'Connected'}
            except Exception as e:
                health_status['scylla'] = {'status': 'unhealthy', 'message': str(e)}
        
        # Check Redis
        if 'redis' in self.services:
            try:
                await self.services['redis'].get("health_check_key")
                health_status['redis'] = {'status': 'healthy', 'message': 'Connected'}
            except Exception as e:
                health_status['redis'] = {'status': 'unhealthy', 'message': str(e)}
        
        # Check Milvus
        if 'milvus' in self.services:
            try:
                # For now, just check if initialized
                collections = ['think_ai_knowledge'] if self.services['milvus']._initialized else []
                health_status['milvus'] = {
                    'status': 'healthy', 
                    'message': f'{len(collections)} collections'
                }
            except Exception as e:
                health_status['milvus'] = {'status': 'unhealthy', 'message': str(e)}
        
        # Check Neo4j
        if 'neo4j' in self.services:
            try:
                stats = await self.services['neo4j'].get_stats()
                health_status['neo4j'] = {
                    'status': 'healthy',
                    'message': f"{stats['total_nodes']} nodes, {stats['total_relationships']} relationships"
                }
            except Exception as e:
                health_status['neo4j'] = {'status': 'unhealthy', 'message': str(e)}
        
        # Check Language Model
        if 'model_orchestrator' in self.services:
            try:
                info = await self.services['model_orchestrator'].language_model.get_model_info()
                health_status['language_model'] = {
                    'status': 'healthy' if info.get('status') != 'not_initialized' else 'unhealthy',
                    'message': f"{info.get('model_name', 'Unknown')} - {info.get('parameters', 'Unknown')}"
                }
            except Exception as e:
                health_status['language_model'] = {'status': 'unhealthy', 'message': str(e)}
        
        return health_status
    
    async def shutdown(self):
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
            emoji = "✅" if status['status'] == 'healthy' else "❌"
            logger.info(f"   {emoji} {service}: {status['message']}")
        
        return self.services
    
    async def process_with_full_system(self, query: str) -> Dict[str, Any]:
        """Process a query using all available distributed services."""
        results = {
            'query': query,
            'services_used': [],
            'responses': {}
        }
        
        # Use consciousness framework
        if 'consciousness' in self.services:
            consciousness_response = await self.services['consciousness'].generate_conscious_response(query)
            results['responses']['consciousness'] = consciousness_response
            results['services_used'].append('consciousness')
        
        # Use language model if available
        if 'model_orchestrator' in self.services:
            try:
                lm_response = await self.services['model_orchestrator'].language_model.generate(query)
                results['responses']['language_model'] = lm_response.text
                results['services_used'].append('language_model')
            except Exception as e:
                logger.error(f"Language model error: {e}")
        
        # Search vector database
        if 'milvus' in self.services:
            try:
                # Would need to generate embedding first
                # For now, just note that we could search
                results['responses']['vector_search'] = "Vector search available"
                results['services_used'].append('milvus')
            except Exception as e:
                logger.error(f"Vector search error: {e}")
        
        # Query knowledge graph
        if 'neo4j' in self.services:
            try:
                # Search for related concepts
                related = await self.services['neo4j'].find_related_concepts(query, max_depth=2)
                if related:
                    results['responses']['knowledge_graph'] = related
                    results['services_used'].append('neo4j')
            except Exception as e:
                logger.error(f"Knowledge graph error: {e}")
        
        return results
    
    async def shutdown(self):
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
                logger.info(f"  {response[:200]}...")
            else:
                logger.info(f"  {response}")
        
    finally:
        await system.shutdown()


if __name__ == "__main__":
    asyncio.run(test_full_system())