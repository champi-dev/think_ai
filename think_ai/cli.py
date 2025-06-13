"""Command-line interface for Think AI."""

import asyncio
import sys
from typing import Optional
import click
from datetime import datetime

from .core.engine import ThinkAIEngine
from .core.config import Config
from .utils.logging import configure_logging


@click.group()
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.option('--offline', is_flag=True, help='Use offline storage mode')
@click.pass_context
def main(ctx, debug, offline):
    """Think AI - Universal Knowledge Access System"""
    # Configure logging
    log_level = "DEBUG" if debug else "INFO"
    logger = configure_logging(log_level=log_level)
    
    # Create config
    config = Config.from_env()
    config.debug = debug
    
    # Store in context
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['logger'] = logger
    ctx.obj['offline'] = offline


@main.command()
@click.pass_context
def init(ctx):
    """Initialize Think AI system components."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    async def run_init():
        logger.info("Initializing Think AI system...")
        
        async with ThinkAIEngine(config) as engine:
            # Perform health check
            health = await engine.health_check()
            
            if health['status'] == 'healthy':
                logger.info("✓ Think AI system initialized successfully")
                logger.info(f"System health: {health}")
            else:
                logger.error("✗ Think AI system initialization failed")
                logger.error(f"Health check: {health}")
                sys.exit(1)
    
    asyncio.run(run_init())


@main.command()
@click.argument('key')
@click.argument('content')
@click.option('--metadata', '-m', help='JSON metadata')
@click.pass_context
def store(ctx, key, content, metadata):
    """Store knowledge in Think AI."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    async def run_store():
        async with ThinkAIEngine(config) as engine:
            # Parse metadata if provided
            meta = None
            if metadata:
                import json
                try:
                    meta = json.loads(metadata)
                except json.JSONDecodeError:
                    logger.error("Invalid JSON metadata")
                    sys.exit(1)
            
            # Store knowledge
            item_id = await engine.store_knowledge(key, content, meta)
            logger.info(f"✓ Stored knowledge with key: {key}, id: {item_id}")
    
    asyncio.run(run_store())


@main.command()
@click.argument('key')
@click.pass_context
def get(ctx, key):
    """Retrieve knowledge from Think AI."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    async def run_get():
        async with ThinkAIEngine(config) as engine:
            result = await engine.retrieve_knowledge(key)
            
            if result:
                logger.info(f"✓ Found knowledge for key: {key}")
                print(f"\nContent: {result['content']}")
                print(f"Metadata: {result['metadata']}")
                print(f"Created: {result['created_at']}")
                print(f"Updated: {result['updated_at']}")
            else:
                logger.warning(f"✗ No knowledge found for key: {key}")
    
    asyncio.run(run_get())


@main.command()
@click.argument('query')
@click.option('--limit', '-l', default=10, help='Maximum results')
@click.pass_context
def query(ctx, query, limit):
    """Query knowledge in Think AI."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    async def run_query():
        async with ThinkAIEngine(config) as engine:
            result = await engine.query_knowledge(query, limit=limit)
            
            logger.info(f"✓ Query completed in {result.processing_time_ms:.2f}ms")
            print(f"\nFound {len(result.results)} results for: {query}")
            
            for i, item in enumerate(result.results, 1):
                print(f"\n{i}. Key: {item.get('key', 'N/A')}")
                print(f"   Content: {item['content']}")
                print(f"   Created: {item['created_at']}")
    
    asyncio.run(run_query())


@main.command()
@click.pass_context
def stats(ctx):
    """Show system statistics."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    async def run_stats():
        async with ThinkAIEngine(config) as engine:
            stats = await engine.get_system_stats()
            
            print("\n=== Think AI System Statistics ===")
            print(f"Status: {stats['status']}")
            print(f"Version: {stats['config']['version']}")
            
            if 'storage' in stats:
                print("\n--- Storage Stats ---")
                primary = stats['storage'].get('primary', {})
                cache = stats['storage'].get('cache', {})
                
                print(f"Primary (ScyllaDB):")
                print(f"  Items: {primary.get('item_count', 'N/A')}")
                print(f"  Backend: {primary.get('backend', 'N/A')}")
                
                print(f"\nCache (Redis):")
                print(f"  Memory: {cache.get('used_memory_human', 'N/A')}")
                print(f"  Hit Rate: {cache.get('hit_rate', 0):.2f}%")
                print(f"  Ops/sec: {cache.get('instantaneous_ops_per_sec', 0)}")
    
    asyncio.run(run_stats())


@main.command()
@click.pass_context
def health(ctx):
    """Check system health."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    async def run_health():
        async with ThinkAIEngine(config) as engine:
            health = await engine.health_check()
            
            status_icon = "✓" if health['status'] == 'healthy' else "✗"
            print(f"\n{status_icon} System Status: {health['status']}")
            print(f"Timestamp: {health['timestamp']}")
            
            print("\nComponent Health:")
            for component, status in health['components'].items():
                comp_icon = "✓" if status['status'] == 'healthy' else "✗"
                print(f"  {comp_icon} {component}: {status['status']}")
                if 'error' in status:
                    print(f"     Error: {status['error']}")
    
    asyncio.run(run_health())


if __name__ == '__main__':
    main()