"""Command-line interface for Think AI."""

import asyncio
import sys
from typing import Optional
import click
from datetime import datetime

from .core.engine import ThinkAIEngine
from .core.config import Config
from .utils.logging import configure_logging
from .storage.offline import OfflineStorage, OfflineSyncManager, AdvancedOfflineManager
from .benchmarks.performance import PerformanceBenchmark
from .federated.federated_learning import FederatedLearningServer, FederatedLearningClient


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


@main.command()
@click.option('--quick', is_flag=True, help='Run quick benchmark (100 ops)')
@click.option('--full', is_flag=True, help='Run full benchmark (1000 ops)')
@click.pass_context
def benchmark(ctx, quick, full):
    """Run performance benchmarks."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    async def run_benchmark():
        async with ThinkAIEngine(config) as engine:
            benchmark = PerformanceBenchmark(engine)
            
            num_ops = 100 if quick else 1000 if full else 100
            logger.info(f"Running benchmark with {num_ops} operations...")
            
            results = await benchmark.run_all_benchmarks(num_ops)
            print(benchmark.generate_report())
    
    asyncio.run(run_benchmark())


@main.command()
@click.argument('action', type=click.Choice(['status', 'sync', 'enable-offline', 'smart-sync']))
@click.option('--batch-size', default=100, help='Batch size for sync')
@click.pass_context
def offline(ctx, action, batch_size):
    """Manage offline storage and sync."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    async def run_offline():
        # Initialize components
        offline_storage = OfflineStorage(config.offline_storage)
        await offline_storage.initialize()
        
        if action == 'status':
            # Show offline storage status
            stats = await offline_storage.get_stats()
            print(f"\nOffline Storage Status:")
            print(f"  Total items: {stats['total_items']:,}")
            print(f"  Unsynced items: {stats['unsynced_items']:,}")
            print(f"  Database size: {stats['database_size_mb']:.2f} MB")
            print(f"  FTS enabled: {'Yes' if stats['fts_enabled'] else 'No'}")
            
        elif action in ['sync', 'smart-sync']:
            # Initialize online storage
            async with ThinkAIEngine(config) as engine:
                sync_manager = OfflineSyncManager(
                    offline_storage,
                    engine.storage,
                    engine.vector_db,
                    engine.embedding_model
                )
                
                if action == 'sync':
                    # Basic sync
                    logger.info("Starting offline to online sync...")
                    result = await sync_manager.sync_to_online(batch_size)
                    
                    print(f"\nSync completed:")
                    print(f"  Items synced: {result['items_synced']}")
                    print(f"  Duration: {result.get('duration_seconds', 0):.2f}s")
                    if result.get('errors'):
                        print(f"  Errors: {len(result['errors'])}")
                        
                else:  # smart-sync
                    # Advanced sync with conflict resolution
                    advanced_manager = AdvancedOfflineManager(offline_storage, sync_manager)
                    
                    logger.info("Starting smart sync with conflict resolution...")
                    result = await advanced_manager.smart_sync()
                    
                    print(f"\nSmart sync completed:")
                    print(f"  Items uploaded: {result['items_uploaded']}")
                    print(f"  Items downloaded: {result['items_downloaded']}")
                    print(f"  Conflicts resolved: {result['conflicts_resolved']}")
                    print(f"  Success: {'Yes' if result['success'] else 'No'}")
                    
        elif action == 'enable-offline':
            # Enable offline mode
            async with ThinkAIEngine(config) as engine:
                sync_manager = OfflineSyncManager(offline_storage, engine.storage)
                advanced_manager = AdvancedOfflineManager(offline_storage, sync_manager)
                
                await advanced_manager.enable_offline_mode()
                print("✓ Offline mode enabled - all operations will be local-first")
        
        await offline_storage.close()
    
    asyncio.run(run_offline())


@main.command()
@click.argument('action', type=click.Choice(['start-server', 'register-client', 'submit-update']))
@click.option('--client-id', help='Client ID for federated learning')
@click.option('--min-clients', default=3, help='Minimum clients for aggregation')
@click.pass_context
def federated(ctx, action, client_id, min_clients):
    """Manage federated learning."""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    async def run_federated():
        if action == 'start-server':
            # Start federated learning server
            server = FederatedLearningServer(min_clients=min_clients)
            
            print(f"Federated Learning Server Started")
            print(f"  Minimum clients: {min_clients}")
            print(f"  Model version: {server.global_model_version}")
            print("\nWaiting for clients to register...")
            
            # In production, this would run as a service
            
        elif action == 'register-client':
            if not client_id:
                print("Error: --client-id required")
                return
                
            # Register as federated client
            server = FederatedLearningServer()  # Connect to existing server
            success = await server.register_client(client_id)
            
            if success:
                print(f"✓ Client '{client_id}' registered successfully")
            else:
                print(f"✗ Failed to register client '{client_id}'")
                
        elif action == 'submit-update':
            if not client_id:
                print("Error: --client-id required")
                return
                
            # Submit model update
            client = FederatedLearningClient(client_id, local_data_size=1000)
            
            # Compute update (in production, use actual local data)
            update = await client.compute_update(None, None, epochs=1)
            
            print(f"Update computed by client '{client_id}':")
            print(f"  Data size: {update.data_size}")
            print(f"  Metrics: {update.metrics}")
            print(f"  Privacy budget remaining: {client.privacy_budget_remaining()}")
    
    asyncio.run(run_federated())


if __name__ == '__main__':
    main()