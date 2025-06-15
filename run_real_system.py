#!/usr/bin/env python3
"""Run Think AI with REAL services (Redis + SQLite hybrid)."""

import asyncio
import os
import sys
from pathlib import Path
import sqlite3
import redis.asyncio as redis
from datetime import datetime
import json
import numpy as np
from typing import Dict, Any, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.consciousness.awareness import ConsciousnessFramework
from think_ai.consciousness.principles import ConstitutionalAI
from think_ai.models.language_model import LanguageModel
from think_ai.storage.redis_cache import RedisCache
from think_ai.storage.offline import OfflineStorage
from think_ai.storage.base import StorageItem
from think_ai.core.config import RedisConfig, ModelConfig
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


class InMemoryVectorDB:
    """Simple in-memory vector database."""
    
    def __init__(self):
        self.vectors = {}
        self.dimension = 384  # For sentence-transformers
        
    async def insert(self, key: str, vector: np.ndarray, metadata: Dict[str, Any] = None):
        """Insert a vector."""
        self.vectors[key] = {
            'vector': vector,
            'metadata': metadata or {}
        }
    
    async def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors using cosine similarity."""
        if not self.vectors:
            return []
        
        results = []
        for key, data in self.vectors.items():
            # Cosine similarity
            similarity = np.dot(query_vector, data['vector']) / (
                np.linalg.norm(query_vector) * np.linalg.norm(data['vector'])
            )
            results.append({
                'key': key,
                'similarity': float(similarity),
                'metadata': data['metadata']
            })
        
        # Sort by similarity
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]


class RealThinkAI:
    """Think AI using real services where available."""
    
    def __init__(self):
        self.services = {}
        self.initialized = False
        
    async def initialize(self):
        """Initialize all real services."""
        logger.info("🚀 Initializing REAL Think AI Services")
        
        # 1. Redis Cache (REAL)
        try:
            redis_config = RedisConfig(host='localhost', port=6379)
            self.redis = RedisCache(redis_config)
            await self.redis.initialize()
            self.services['redis'] = self.redis
            logger.info("✅ Redis (REAL) initialized")
        except Exception as e:
            logger.error(f"❌ Redis failed: {e}")
            self.redis = None
        
        # 2. SQLite Storage (REAL)
        try:
            self.sqlite = OfflineStorage("think_ai_real.db")
            await self.sqlite.initialize()
            self.services['sqlite'] = self.sqlite
            logger.info("✅ SQLite (REAL) initialized")
        except Exception as e:
            logger.error(f"❌ SQLite failed: {e}")
        
        # 3. In-Memory Vector DB
        self.vector_db = InMemoryVectorDB()
        self.services['vector_db'] = self.vector_db
        logger.info("✅ Vector DB (in-memory) initialized")
        
        # 4. Consciousness Framework
        self.consciousness = ConsciousnessFramework()
        self.services['consciousness'] = self.consciousness
        logger.info("✅ Consciousness framework initialized")
        
        # 5. Language Model
        try:
            model_config = ModelConfig(
                model_name='gpt2',
                device='cpu',
                max_tokens=512
            )
            self.language_model = LanguageModel()
            constitutional_ai = ConstitutionalAI()
            await self.language_model.initialize(model_config, constitutional_ai)
            self.services['language_model'] = self.language_model
            logger.info("✅ Language Model (GPT-2) initialized")
        except Exception as e:
            logger.error(f"❌ Language model failed: {e}")
            self.language_model = None
        
        # Populate some initial data
        await self._populate_knowledge_base()
        
        self.initialized = True
        logger.info(f"\n📊 Active REAL Services: {len(self.services)}")
        for name in self.services:
            logger.info(f"   ✅ {name}")
    
    async def _populate_knowledge_base(self):
        """Add some initial knowledge."""
        knowledge_items = [
            ("consciousness", "Consciousness is the state of being aware of and able to think about one's existence, sensations, thoughts, and surroundings."),
            ("distributed_ai", "Distributed AI refers to artificial intelligence systems that operate across multiple nodes or components, sharing computation and data."),
            ("neural_networks", "Neural networks are computing systems inspired by biological neural networks that constitute animal brains."),
            ("redis", "Redis is an in-memory data structure store, used as a distributed, in-memory key-value database, cache, and message broker."),
            ("think_ai", "Think AI is a distributed consciousness system that combines multiple AI components for enhanced intelligence and ethical reasoning.")
        ]
        
        for key, content in knowledge_items:
            # Store in SQLite
            await self.sqlite.put(
                f"knowledge_{key}",
                StorageItem.create(
                    content=content,
                    metadata={'type': 'knowledge', 'topic': key}
                )
            )
            
            # Cache in Redis if available
            if self.redis:
                try:
                    await self.redis.set(
                        f"knowledge_{key}",
                        content,
                        ttl=3600
                    )
                except:
                    pass
            
            # Create simple vector (random for demo)
            vector = np.random.randn(self.vector_db.dimension)
            vector = vector / np.linalg.norm(vector)  # Normalize
            await self.vector_db.insert(
                f"knowledge_{key}",
                vector,
                {'content': content, 'topic': key}
            )
        
        logger.info(f"✅ Populated knowledge base with {len(knowledge_items)} items")
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process query using all available real services."""
        logger.info(f"\n❓ Processing: {query}")
        responses = {}
        services_used = []
        
        # 1. Check Redis cache first
        cache_key = f"query_{hash(query) % 10**9}"
        cached = None
        
        if self.redis:
            try:
                cached = await self.redis.get(cache_key)
                if cached:
                    logger.info("   ✅ Cache hit!")
                    return json.loads(cached)
            except Exception as e:
                logger.debug(f"Cache check failed: {e}")
        
        # 2. Search SQLite knowledge base
        knowledge_results = []
        try:
            # Simple keyword search
            all_items = await self.sqlite.list_keys(limit=100)
            for key in all_items:
                if key.startswith("knowledge_"):
                    item = await self.sqlite.get(key)
                    if item and any(word.lower() in item.content.lower() for word in query.split()):
                        knowledge_results.append(item.content)
            
            if knowledge_results:
                responses['knowledge_base'] = knowledge_results[:3]
                services_used.append('sqlite')
                logger.info(f"   ✅ Found {len(knowledge_results)} knowledge items")
        except Exception as e:
            logger.error(f"Knowledge search failed: {e}")
        
        # 3. Vector similarity search
        try:
            # Create a simple query vector (random for demo)
            query_vector = np.random.randn(self.vector_db.dimension)
            query_vector = query_vector / np.linalg.norm(query_vector)
            
            similar = await self.vector_db.search(query_vector, top_k=3)
            if similar:
                responses['vector_search'] = [
                    f"{item['metadata'].get('topic', 'unknown')}: {item['similarity']:.2f}"
                    for item in similar
                ]
                services_used.append('vector_db')
                logger.info(f"   ✅ Found {len(similar)} similar vectors")
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
        
        # 4. Consciousness framework
        try:
            conscious_response = await self.consciousness.generate_conscious_response(query)
            responses['consciousness'] = conscious_response
            services_used.append('consciousness')
            logger.info("   ✅ Consciousness response generated")
        except Exception as e:
            logger.error(f"Consciousness failed: {e}")
        
        # 5. Language model generation
        if self.language_model:
            try:
                # Build context from knowledge
                context = ""
                if knowledge_results:
                    context = "Context: " + " ".join(knowledge_results[:2]) + "\n\n"
                
                prompt = f"{context}Question: {query}\nAnswer:"
                model_response = await self.language_model.generate(prompt, max_tokens=150)
                responses['language_model'] = model_response
                services_used.append('gpt2')
                logger.info("   ✅ Language model response generated")
            except Exception as e:
                logger.error(f"Language model failed: {e}")
        
        # Build final result
        result = {
            'query': query,
            'responses': responses,
            'services_used': services_used,
            'timestamp': datetime.now().isoformat(),
            'cached': False
        }
        
        # Cache the result
        if self.redis and services_used:
            try:
                await self.redis.set(
                    cache_key,
                    json.dumps(result),
                    ttl=300  # 5 minutes
                )
                logger.info("   ✅ Result cached")
            except:
                pass
        
        return result
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all services."""
        health = {}
        
        # Redis
        if self.redis:
            try:
                await self.redis.get("health_check")
                health['redis'] = {'status': 'healthy', 'type': 'REAL'}
            except:
                health['redis'] = {'status': 'unhealthy', 'type': 'REAL'}
        
        # SQLite
        if hasattr(self, 'sqlite'):
            try:
                stats = await self.sqlite.get_stats()
                health['sqlite'] = {
                    'status': 'healthy',
                    'type': 'REAL',
                    'items': stats.get('item_count', 0)
                }
            except:
                health['sqlite'] = {'status': 'unhealthy', 'type': 'REAL'}
        
        # Vector DB
        health['vector_db'] = {
            'status': 'healthy',
            'type': 'in-memory',
            'vectors': len(self.vector_db.vectors)
        }
        
        # Language Model
        if self.language_model:
            try:
                info = await self.language_model.get_model_info()
                health['language_model'] = {
                    'status': 'healthy' if info.get('status') != 'not_initialized' else 'unhealthy',
                    'type': 'REAL',
                    'model': info.get('model_name', 'unknown')
                }
            except:
                health['language_model'] = {'status': 'unhealthy', 'type': 'REAL'}
        
        return health
    
    async def shutdown(self):
        """Shutdown all services."""
        logger.info("\n🔄 Shutting down services...")
        
        if self.redis:
            await self.redis.close()
        
        if hasattr(self, 'sqlite'):
            await self.sqlite.close()
        
        logger.info("✅ All services shut down")


async def main():
    """Main entry point."""
    print("\n🧠 THINK AI - REAL SERVICES SYSTEM")
    print("=" * 50)
    print("Using: Redis (REAL) • SQLite (REAL) • In-Memory Vector DB")
    print("=" * 50)
    
    system = RealThinkAI()
    
    try:
        # Initialize
        await system.initialize()
        
        # Health check
        print("\n🏥 Health Check:")
        health = await system.health_check()
        for service, status in health.items():
            emoji = "✅" if status['status'] == 'healthy' else "❌"
            print(f"   {emoji} {service}: {status['type']} - {status['status']}")
        
        # Run test queries
        print("\n📝 Running test queries...\n")
        
        test_queries = [
            "What is consciousness?",
            "How does Redis work?",
            "Explain distributed AI systems",
        ]
        
        for query in test_queries:
            result = await system.process_query(query)
            
            print(f"\n{'='*50}")
            print(f"Query: {query}")
            print(f"Services used: {', '.join(result['services_used'])}")
            
            for service, response in result['responses'].items():
                print(f"\n{service}:")
                if isinstance(response, list):
                    for item in response:
                        print(f"  • {item[:100]}...")
                elif isinstance(response, dict):
                    content = response.get('content', str(response))
                    print(f"  {content[:150]}...")
                else:
                    print(f"  {str(response)[:150]}...")
        
        print("\n" + "="*50)
        print("✅ REAL system demonstration complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await system.shutdown()


if __name__ == "__main__":
    asyncio.run(main())