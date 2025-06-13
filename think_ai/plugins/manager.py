"""Plugin manager for Think AI."""

import importlib
import inspect
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Type, Any, Set
import json
import asyncio

from .base import (
    Plugin, PluginMetadata, PluginCapability, PluginContext,
    PluginLoadError, PluginExecutionError
)
from ..consciousness.principles import ConstitutionalAI
from ..utils.logging import get_logger


logger = get_logger(__name__)


class PluginManager:
    """Manages plugin lifecycle and execution."""
    
    def __init__(
        self,
        plugin_dir: Optional[Path] = None,
        constitutional_ai: Optional[ConstitutionalAI] = None
    ):
        self.plugin_dir = plugin_dir or Path.home() / ".think_ai" / "plugins"
        self.constitutional_ai = constitutional_ai
        self.plugins: Dict[str, Plugin] = {}
        self.capabilities: Dict[PluginCapability, List[str]] = {}
        self._hooks: Dict[str, List[Plugin]] = {}
        
        # Create plugin directory if it doesn't exist
        self.plugin_dir.mkdir(parents=True, exist_ok=True)
    
    async def discover_plugins(self) -> List[PluginMetadata]:
        """Discover available plugins."""
        discovered = []
        
        # Check built-in plugins
        discovered.extend(await self._discover_builtin_plugins())
        
        # Check plugin directory
        discovered.extend(await self._discover_directory_plugins())
        
        # Check installed packages
        discovered.extend(await self._discover_package_plugins())
        
        logger.info(f"Discovered {len(discovered)} plugins")
        return discovered
    
    async def load_plugin(
        self,
        plugin_name: str,
        context: PluginContext,
        force: bool = False
    ) -> Plugin:
        """Load and initialize a plugin."""
        if plugin_name in self.plugins and not force:
            logger.warning(f"Plugin {plugin_name} already loaded")
            return self.plugins[plugin_name]
        
        try:
            # Find plugin class
            plugin_class = await self._find_plugin_class(plugin_name)
            
            if not plugin_class:
                raise PluginLoadError(f"Plugin {plugin_name} not found")
            
            # Get metadata
            metadata = await self._get_plugin_metadata(plugin_class)
            
            # Ethical check
            if self.constitutional_ai and metadata.love_aligned:
                if not await self._check_plugin_ethics(metadata):
                    raise PluginLoadError(
                        f"Plugin {plugin_name} failed ethical review"
                    )
            
            # Create instance
            plugin = plugin_class(metadata)
            
            # Initialize
            await plugin.initialize(context)
            
            # Register
            self.plugins[plugin_name] = plugin
            self._register_capabilities(plugin_name, metadata.capabilities)
            
            logger.info(f"Loaded plugin: {plugin_name} v{metadata.version}")
            return plugin
            
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}")
            raise PluginLoadError(f"Failed to load {plugin_name}: {e}")
    
    async def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin."""
        if plugin_name not in self.plugins:
            logger.warning(f"Plugin {plugin_name} not loaded")
            return False
        
        try:
            plugin = self.plugins[plugin_name]
            
            # Shutdown
            await plugin.shutdown()
            
            # Unregister
            self._unregister_capabilities(plugin_name)
            del self.plugins[plugin_name]
            
            logger.info(f"Unloaded plugin: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_name}: {e}")
            return False
    
    async def reload_plugin(self, plugin_name: str, context: PluginContext) -> Plugin:
        """Reload a plugin."""
        await self.unload_plugin(plugin_name)
        return await self.load_plugin(plugin_name, context, force=True)
    
    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """Get a loaded plugin."""
        return self.plugins.get(plugin_name)
    
    def get_plugins_by_capability(self, capability: PluginCapability) -> List[Plugin]:
        """Get all plugins providing a capability."""
        plugin_names = self.capabilities.get(capability, [])
        return [self.plugins[name] for name in plugin_names if name in self.plugins]
    
    async def execute_hook(self, hook_name: str, data: Any = None) -> List[Any]:
        """Execute a hook on all plugins that implement it."""
        results = []
        
        for plugin in self.plugins.values():
            if hook_name in plugin.hooks:
                try:
                    result = await plugin.emit_event(hook_name, data)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Hook {hook_name} failed in {plugin.metadata.name}: {e}")
        
        return results
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all loaded plugins."""
        health_reports = {}
        
        for name, plugin in self.plugins.items():
            try:
                health = await plugin.health_check()
                health_reports[name] = health
            except Exception as e:
                health_reports[name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Overall health
        unhealthy = sum(
            1 for report in health_reports.values()
            if report.get("status") != "healthy"
        )
        
        return {
            "total_plugins": len(self.plugins),
            "healthy_plugins": len(self.plugins) - unhealthy,
            "unhealthy_plugins": unhealthy,
            "plugin_reports": health_reports
        }
    
    async def install_plugin(self, plugin_path: str) -> bool:
        """Install a plugin from a file or URL."""
        try:
            # In production, this would:
            # 1. Download/copy plugin files
            # 2. Verify signatures
            # 3. Install dependencies
            # 4. Run security checks
            
            logger.info(f"Installing plugin from {plugin_path}")
            
            # For now, just copy to plugin directory
            import shutil
            dest = self.plugin_dir / Path(plugin_path).name
            shutil.copy2(plugin_path, dest)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to install plugin: {e}")
            return False
    
    def list_loaded_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins with info."""
        return [
            {
                "name": plugin.metadata.name,
                "version": plugin.metadata.version,
                "author": plugin.metadata.author,
                "capabilities": [c.value for c in plugin.metadata.capabilities],
                "love_aligned": plugin.metadata.love_aligned,
                "status": "loaded"
            }
            for plugin in self.plugins.values()
        ]
    
    async def _discover_builtin_plugins(self) -> List[PluginMetadata]:
        """Discover built-in plugins."""
        # This would scan the plugins directory for built-in plugins
        return []
    
    async def _discover_directory_plugins(self) -> List[PluginMetadata]:
        """Discover plugins in plugin directory."""
        discovered = []
        
        for file_path in self.plugin_dir.glob("*.py"):
            if file_path.name.startswith("_"):
                continue
            
            try:
                # Load module
                spec = importlib.util.spec_from_file_location(
                    file_path.stem,
                    file_path
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find plugin classes
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, Plugin) and 
                        obj != Plugin):
                        metadata = await self._get_plugin_metadata(obj)
                        discovered.append(metadata)
                        
            except Exception as e:
                logger.error(f"Error discovering plugin {file_path}: {e}")
        
        return discovered
    
    async def _discover_package_plugins(self) -> List[PluginMetadata]:
        """Discover plugins from installed packages."""
        discovered = []
        
        # Look for packages with think_ai_plugin entry point
        try:
            import pkg_resources
            
            for entry_point in pkg_resources.iter_entry_points('think_ai_plugin'):
                try:
                    plugin_class = entry_point.load()
                    metadata = await self._get_plugin_metadata(plugin_class)
                    discovered.append(metadata)
                except Exception as e:
                    logger.error(f"Error loading plugin {entry_point.name}: {e}")
                    
        except ImportError:
            pass  # pkg_resources not available
        
        return discovered
    
    async def _find_plugin_class(self, plugin_name: str) -> Optional[Type[Plugin]]:
        """Find a plugin class by name."""
        # Check loaded modules
        for module in sys.modules.values():
            if not module:
                continue
                
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, Plugin) and 
                    obj != Plugin):
                    try:
                        metadata = await self._get_plugin_metadata(obj)
                        if metadata.name == plugin_name:
                            return obj
                    except:
                        pass
        
        return None
    
    async def _get_plugin_metadata(self, plugin_class: Type[Plugin]) -> PluginMetadata:
        """Extract metadata from plugin class."""
        # Check for metadata attribute
        if hasattr(plugin_class, 'METADATA'):
            return plugin_class.METADATA
        
        # Check for metadata method
        if hasattr(plugin_class, 'get_metadata'):
            return plugin_class.get_metadata()
        
        # Create default metadata
        return PluginMetadata(
            name=plugin_class.__name__,
            version="0.1.0",
            author="Unknown",
            description=plugin_class.__doc__ or "No description",
            capabilities=[]
        )
    
    async def _check_plugin_ethics(self, metadata: PluginMetadata) -> bool:
        """Check if plugin meets ethical standards."""
        if not self.constitutional_ai:
            return True
        
        # Check plugin description
        assessment = await self.constitutional_ai.evaluate_content(
            f"Plugin: {metadata.name}\nDescription: {metadata.description}"
        )
        
        if not assessment.passed:
            logger.warning(
                f"Plugin {metadata.name} failed ethics check: "
                f"{assessment.recommendations}"
            )
            return False
        
        return True
    
    def _register_capabilities(
        self,
        plugin_name: str,
        capabilities: List[PluginCapability]
    ) -> None:
        """Register plugin capabilities."""
        for capability in capabilities:
            if capability not in self.capabilities:
                self.capabilities[capability] = []
            self.capabilities[capability].append(plugin_name)
    
    def _unregister_capabilities(self, plugin_name: str) -> None:
        """Unregister plugin capabilities."""
        for capability_list in self.capabilities.values():
            if plugin_name in capability_list:
                capability_list.remove(plugin_name)


class PluginSandbox:
    """Sandbox for running untrusted plugins safely."""
    
    def __init__(self, resource_limits: Dict[str, Any] = None):
        self.resource_limits = resource_limits or {
            "memory_mb": 100,
            "cpu_percent": 25,
            "time_seconds": 30,
            "network_access": False
        }
    
    async def run_plugin(
        self,
        plugin: Plugin,
        method: str,
        *args,
        **kwargs
    ) -> Any:
        """Run plugin method in sandbox."""
        # In production, this would use:
        # - Process isolation
        # - Resource limits
        # - Security policies
        # - Monitoring
        
        try:
            # For now, just run with timeout
            method_func = getattr(plugin, method)
            result = await asyncio.wait_for(
                method_func(*args, **kwargs),
                timeout=self.resource_limits["time_seconds"]
            )
            return result
            
        except asyncio.TimeoutError:
            raise PluginExecutionError(f"Plugin method {method} timed out")
        except Exception as e:
            raise PluginExecutionError(f"Plugin method {method} failed: {e}")