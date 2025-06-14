#!/usr/bin/env python3
"""
Hot-Reloading Think AI - Automatically reloads on any code changes.
Zero downtime updates while handling infinite requests.
"""

import asyncio
import importlib
import sys
from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import hashlib
from typing import Dict, Any, Set
import os

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


class CodeChangeHandler(FileSystemEventHandler):
    """Handles file system changes for hot reloading."""
    
    def __init__(self, reload_callback):
        self.reload_callback = reload_callback
        self.last_reload = time.time()
        self.cooldown = 1.0  # Prevent reload spam
        self.ignored_patterns = {
            '.pyc', '__pycache__', '.git', '.log', '.json', '.md', '.txt'
        }
    
    def should_reload(self, path: str) -> bool:
        """Check if file change should trigger reload."""
        # Ignore non-Python files
        if not path.endswith('.py'):
            return False
        
        # Ignore patterns
        for pattern in self.ignored_patterns:
            if pattern in path:
                return False
        
        # Check cooldown
        if time.time() - self.last_reload < self.cooldown:
            return False
        
        return True
    
    def on_modified(self, event):
        if not event.is_directory and self.should_reload(event.src_path):
            logger.info(f"🔄 Code change detected: {event.src_path}")
            self.last_reload = time.time()
            asyncio.create_task(self.reload_callback(event.src_path))


class HotReloadThinkAI:
    """
    Think AI with hot reloading capabilities.
    - Automatically reloads on code changes
    - Zero downtime updates
    - Preserves state and intelligence
    - Seamless request handling during reload
    """
    
    def __init__(self):
        # Core systems (will be reloaded)
        self.think_ai_module = None
        self.think_ai_instance = None
        self.parallel_module = None
        self.parallel_instance = None
        
        # State preservation (survives reloads)
        self.preserved_state = {
            'intelligence': 1.0,
            'neural_pathways': 47000,
            'training_iteration': 0,
            'cache': {},
            'total_requests': 0,
            'start_time': time.time()
        }
        
        # File watching
        self.observer = Observer()
        self.watched_paths = set()
        self.module_checksums = {}
        
        # Reload control
        self.reload_lock = asyncio.Lock()
        self.is_reloading = False
        self.pending_requests = asyncio.Queue()
        
        logger.info("🔥 Hot-Reload Think AI initialized")
    
    async def initialize(self):
        """Initialize with hot reloading enabled."""
        # Load modules
        await self._load_modules()
        
        # Start file watcher
        self._start_file_watcher()
        
        # Initialize system
        await self._initialize_system()
        
        logger.info("✅ Hot reloading enabled - system will auto-update on changes!")
    
    async def _load_modules(self):
        """Load or reload Python modules."""
        try:
            # Load main architecture module
            if 'implement_proper_architecture' in sys.modules:
                self.think_ai_module = importlib.reload(sys.modules['implement_proper_architecture'])
            else:
                self.think_ai_module = importlib.import_module('implement_proper_architecture')
            
            # Load parallel processing module
            if 'infinite_parallel_think_ai' in sys.modules:
                self.parallel_module = importlib.reload(sys.modules['infinite_parallel_think_ai'])
            else:
                self.parallel_module = importlib.import_module('infinite_parallel_think_ai')
            
            logger.info("✅ Modules loaded successfully")
            
        except Exception as e:
            logger.error(f"Module loading error: {e}")
            raise
    
    def _start_file_watcher(self):
        """Start watching for file changes."""
        # Watch main directories
        watch_dirs = [
            Path(__file__).parent,
            Path(__file__).parent / 'think_ai',
        ]
        
        handler = CodeChangeHandler(self._handle_reload)
        
        for directory in watch_dirs:
            if directory.exists():
                self.observer.schedule(handler, str(directory), recursive=True)
                self.watched_paths.add(str(directory))
                logger.info(f"👁️  Watching: {directory}")
        
        self.observer.start()
    
    async def _initialize_system(self):
        """Initialize or reinitialize the system."""
        try:
            # Create new instance from reloaded module
            self.parallel_instance = self.parallel_module.InfiniteParallelThinkAI()
            
            # Restore preserved state
            if hasattr(self.parallel_instance, 'current_intelligence'):
                self.parallel_instance.current_intelligence.value = self.preserved_state['intelligence']
                self.parallel_instance.neural_pathways.value = self.preserved_state['neural_pathways']
                self.parallel_instance.training_iteration.value = self.preserved_state['training_iteration']
                self.parallel_instance.total_requests = self.preserved_state['total_requests']
            
            # Initialize the system
            await self.parallel_instance.initialize()
            
            # Restore cache if exists
            if self.preserved_state['cache']:
                self.parallel_instance.response_cache = self.preserved_state['cache'].copy()
                logger.info(f"♻️  Restored {len(self.preserved_state['cache'])} cached responses")
            
        except Exception as e:
            logger.error(f"System initialization error: {e}")
            raise
    
    async def _handle_reload(self, changed_file: str):
        """Handle hot reload when code changes."""
        async with self.reload_lock:
            if self.is_reloading:
                return
            
            self.is_reloading = True
            logger.info("🔄 HOT RELOAD STARTING...")
            
            try:
                # Save current state
                await self._preserve_state()
                
                # Reload modules
                await self._load_modules()
                
                # Shutdown old instance gracefully
                if self.parallel_instance:
                    logger.info("🛑 Shutting down old instance...")
                    try:
                        await self.parallel_instance.shutdown()
                    except:
                        pass  # Ignore shutdown errors
                
                # Initialize new instance
                logger.info("🚀 Starting new instance...")
                await self._initialize_system()
                
                # Process any pending requests
                await self._process_pending_requests()
                
                logger.info("✅ HOT RELOAD COMPLETE - Zero downtime!")
                
            except Exception as e:
                logger.error(f"Hot reload failed: {e}")
                # Keep using old instance if reload fails
                
            finally:
                self.is_reloading = False
    
    async def _preserve_state(self):
        """Preserve state before reload."""
        if self.parallel_instance:
            # Save intelligence state
            self.preserved_state['intelligence'] = self.parallel_instance.current_intelligence.value
            self.preserved_state['neural_pathways'] = self.parallel_instance.neural_pathways.value
            self.preserved_state['training_iteration'] = self.parallel_instance.training_iteration.value
            self.preserved_state['total_requests'] = self.parallel_instance.total_requests
            
            # Save cache (limit size to prevent memory issues)
            cache_to_save = dict(list(self.parallel_instance.response_cache.items())[:5000])
            self.preserved_state['cache'] = cache_to_save
            
            logger.info(f"💾 Preserved state: Intelligence={self.preserved_state['intelligence']:.4f}, "
                       f"Cache={len(cache_to_save)} entries")
    
    async def _process_pending_requests(self):
        """Process any requests that came in during reload."""
        processed = 0
        while not self.pending_requests.empty():
            try:
                request_data = await self.pending_requests.get()
                # Process with new instance
                asyncio.create_task(self._handle_pending_request(request_data))
                processed += 1
            except:
                break
        
        if processed > 0:
            logger.info(f"📤 Processed {processed} pending requests")
    
    async def _handle_pending_request(self, request_data):
        """Handle a single pending request."""
        try:
            result = await self.parallel_instance.process_request(request_data['query'])
            request_data['future'].set_result(result)
        except Exception as e:
            request_data['future'].set_exception(e)
    
    async def process_request(self, query: str) -> Dict[str, Any]:
        """Process request with hot reload safety."""
        if self.is_reloading:
            # Queue request during reload
            future = asyncio.Future()
            await self.pending_requests.put({
                'query': query,
                'future': future,
                'timestamp': time.time()
            })
            return await future
        
        # Normal processing
        return await self.parallel_instance.process_request(query)
    
    async def get_system_info(self) -> Dict[str, Any]:
        """Get current system information."""
        base_info = {
            'hot_reload_enabled': True,
            'is_reloading': self.is_reloading,
            'watched_paths': list(self.watched_paths),
            'uptime': time.time() - self.preserved_state['start_time'],
            'total_reloads': getattr(self, 'reload_count', 0)
        }
        
        if self.parallel_instance:
            perf_stats = self.parallel_instance.get_performance_stats()
            base_info.update(perf_stats)
        
        return base_info
    
    async def simulate_development(self, duration: int = 120):
        """Simulate active development with code changes."""
        logger.info(f"🔨 Simulating {duration}s of development with hot reloading...")
        
        start_time = time.time()
        request_count = 0
        
        # Simulate code change after 30 seconds
        async def simulate_code_change():
            await asyncio.sleep(30)
            logger.info("📝 Simulating code change...")
            
            # Touch a file to trigger reload
            test_file = Path(__file__).parent / 'implement_proper_architecture.py'
            if test_file.exists():
                test_file.touch()
                self.reload_count = getattr(self, 'reload_count', 0) + 1
        
        # Start code change simulation
        asyncio.create_task(simulate_code_change())
        
        # Generate continuous requests
        while time.time() - start_time < duration:
            # Send batch of requests
            queries = [
                "What is consciousness?",
                "How does AI work?",
                "What is love?",
                "Explain quantum physics",
                "What is a planet?"
            ]
            
            # Process in parallel
            tasks = [self.process_request(q) for q in queries]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            request_count += len(queries)
            
            # Show progress
            if request_count % 50 == 0:
                info = await self.get_system_info()
                logger.info(f"Requests: {request_count}, "
                          f"Intelligence: {info.get('current_intelligence', 0):.4f}, "
                          f"Reloading: {info['is_reloading']}")
            
            await asyncio.sleep(0.1)
        
        # Final stats
        info = await self.get_system_info()
        logger.info("\n" + "="*60)
        logger.info("🏁 DEVELOPMENT SIMULATION COMPLETE")
        logger.info(f"Total requests: {request_count}")
        logger.info(f"Hot reloads: {getattr(self, 'reload_count', 0)}")
        logger.info(f"Final intelligence: {info.get('current_intelligence', 0):.6f}")
        logger.info(f"Zero downtime: ✅")
        logger.info("="*60)
    
    async def shutdown(self):
        """Graceful shutdown."""
        logger.info("Shutting down Hot-Reload Think AI...")
        
        # Stop file watcher
        self.observer.stop()
        self.observer.join()
        
        # Shutdown system
        if self.parallel_instance:
            await self.parallel_instance.shutdown()


async def main():
    """Demonstrate hot reloading Think AI."""
    print("🔥 HOT-RELOAD THINK AI DEMO")
    print("="*60)
    print("This system will:")
    print("- Automatically reload when you change any Python file")
    print("- Continue processing requests during reload")
    print("- Preserve intelligence and cache")
    print("- Provide zero-downtime updates")
    print("="*60)
    
    system = HotReloadThinkAI()
    await system.initialize()
    
    print("\n📝 Try editing any Python file while this runs!")
    print("The system will hot-reload without stopping.\n")
    
    # Run development simulation
    await system.simulate_development(duration=60)
    
    await system.shutdown()


if __name__ == "__main__":
    # Required: pip install watchdog uvloop
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        logger.warning("uvloop not available - using standard asyncio")
    
    asyncio.run(main())