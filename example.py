#!/usr/bin/env python3
"""Example usage of Think AI system."""

import asyncio
import json
from datetime import datetime

from think_ai import ThinkAIEngine, Config
from think_ai.utils.logging import configure_logging


async def main():
    """Demonstrate Think AI capabilities."""
    
    # Configure logging
    logger = configure_logging(log_level="INFO")
    
    # Create configuration
    config = Config.from_env()
    
    # Initialize engine
    async with ThinkAIEngine(config) as engine:
        logger.info("=== Think AI Example ===")
        
        # 1. Store some knowledge
        logger.info("\n1. Storing knowledge...")
        
        knowledge_items = {
            "ai_definition": {
                "content": "Artificial Intelligence is the simulation of human intelligence in machines.",
                "metadata": {"category": "definition", "field": "AI"}
            },
            "ai_history": {
                "content": "AI research began in 1956 at the Dartmouth Conference.",
                "metadata": {"category": "history", "field": "AI"}
            },
            "quantum_computing": {
                "content": "Quantum computing leverages quantum mechanical phenomena like superposition.",
                "metadata": {"category": "definition", "field": "quantum"}
            },
            "quantum_applications": {
                "content": "Quantum computers excel at cryptography, drug discovery, and optimization.",
                "metadata": {"category": "applications", "field": "quantum"}
            }
        }
        
        for key, item in knowledge_items.items():
            item_id = await engine.store_knowledge(
                key, 
                item["content"], 
                item["metadata"]
            )
            logger.info(f"  ✓ Stored: {key} (ID: {item_id})")
        
        # 2. Retrieve specific knowledge
        logger.info("\n2. Retrieving specific knowledge...")
        
        result = await engine.retrieve_knowledge("ai_definition")
        if result:
            logger.info(f"  ✓ Found: {result['key']}")
            logger.info(f"    Content: {result['content']}")
            logger.info(f"    Category: {result['metadata'].get('category')}")
        
        # 3. Query by prefix
        logger.info("\n3. Querying by prefix...")
        
        query_result = await engine.query_knowledge("prefix:quantum", limit=5)
        logger.info(f"  ✓ Found {len(query_result.results)} results")
        logger.info(f"    Query time: {query_result.processing_time_ms:.2f}ms")
        
        for item in query_result.results:
            logger.info(f"    - {item['key']}: {item['content'][:50]}...")
        
        # 4. Batch operations
        logger.info("\n4. Performing batch operations...")
        
        batch_items = {
            f"ml_concept_{i}": f"Machine Learning concept {i}: {concept}"
            for i, concept in enumerate([
                "Supervised learning uses labeled data",
                "Unsupervised learning finds patterns in unlabeled data",
                "Reinforcement learning learns through rewards"
            ])
        }
        
        ids = await engine.batch_store_knowledge(
            batch_items,
            metadata={"category": "machine_learning", "type": "concept"}
        )
        logger.info(f"  ✓ Batch stored {len(ids)} items")
        
        # 5. System statistics
        logger.info("\n5. System Statistics...")
        
        stats = await engine.get_system_stats()
        storage_stats = stats.get('storage', {})
        
        if 'primary' in storage_stats:
            primary = storage_stats['primary']
            logger.info(f"  Primary Storage (ScyllaDB):")
            logger.info(f"    - Items: {primary.get('item_count', 'N/A')}")
            logger.info(f"    - Status: {primary.get('initialized', False)}")
        
        if 'cache' in storage_stats:
            cache = storage_stats['cache']
            logger.info(f"  Cache (Redis):")
            logger.info(f"    - Memory: {cache.get('used_memory_human', 'N/A')}")
            logger.info(f"    - Hit Rate: {cache.get('hit_rate', 0):.2f}%")
        
        # 6. Health check
        logger.info("\n6. Health Check...")
        
        health = await engine.health_check()
        logger.info(f"  System Status: {health['status']}")
        
        for component, status in health['components'].items():
            status_icon = "✓" if status['status'] == 'healthy' else "✗"
            logger.info(f"  {status_icon} {component}: {status['status']}")
        
        logger.info("\n=== Example Complete ===")


if __name__ == "__main__":
    asyncio.run(main())