"""Plugin registry for Think AI."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import asdict

from .base import PluginMetadata, PluginCapability
from ..utils.logging import get_logger


logger = get_logger(__name__)


class PluginRegistry:
    """Central registry for Think AI plugins."""
    
    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = registry_path or Path.home() / ".think_ai" / "plugin_registry.json"
        self.registry: Dict[str, Dict[str, Any]] = {}
        self.load_registry()
    
    def load_registry(self) -> None:
        """Load registry from disk."""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    self.registry = json.load(f)
                logger.info(f"Loaded {len(self.registry)} plugins from registry")
            except Exception as e:
                logger.error(f"Failed to load registry: {e}")
                self.registry = {}
        else:
            self.registry = {}
    
    def save_registry(self) -> None:
        """Save registry to disk."""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.registry_path, 'w') as f:
                json.dump(self.registry, f, indent=2, default=str)
            logger.info(f"Saved {len(self.registry)} plugins to registry")
        except Exception as e:
            logger.error(f"Failed to save registry: {e}")
    
    def register_plugin(
        self,
        metadata: PluginMetadata,
        source_url: Optional[str] = None,
        verified: bool = False
    ) -> bool:
        """Register a plugin."""
        try:
            plugin_id = f"{metadata.name}@{metadata.version}"
            
            self.registry[plugin_id] = {
                "metadata": asdict(metadata),
                "source_url": source_url,
                "verified": verified,
                "registered_at": datetime.utcnow().isoformat(),
                "downloads": 0,
                "rating": 0.0,
                "reviews": []
            }
            
            self.save_registry()
            logger.info(f"Registered plugin: {plugin_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register plugin: {e}")
            return False
    
    def unregister_plugin(self, plugin_id: str) -> bool:
        """Unregister a plugin."""
        if plugin_id in self.registry:
            del self.registry[plugin_id]
            self.save_registry()
            logger.info(f"Unregistered plugin: {plugin_id}")
            return True
        return False
    
    def get_plugin_info(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a plugin."""
        return self.registry.get(plugin_id)
    
    def search_plugins(
        self,
        query: Optional[str] = None,
        capability: Optional[PluginCapability] = None,
        author: Optional[str] = None,
        tags: Optional[List[str]] = None,
        love_aligned_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Search for plugins."""
        results = []
        
        for plugin_id, info in self.registry.items():
            metadata = info["metadata"]
            
            # Filter by love alignment
            if love_aligned_only and not metadata.get("love_aligned", True):
                continue
            
            # Filter by query
            if query:
                query_lower = query.lower()
                if not any(
                    query_lower in str(field).lower()
                    for field in [
                        metadata.get("name"),
                        metadata.get("description"),
                        metadata.get("tags", [])
                    ]
                ):
                    continue
            
            # Filter by capability
            if capability:
                capabilities = [
                    PluginCapability(c) for c in metadata.get("capabilities", [])
                ]
                if capability not in capabilities:
                    continue
            
            # Filter by author
            if author and metadata.get("author") != author:
                continue
            
            # Filter by tags
            if tags:
                plugin_tags = metadata.get("tags", [])
                if not any(tag in plugin_tags for tag in tags):
                    continue
            
            results.append({
                "plugin_id": plugin_id,
                **info
            })
        
        # Sort by rating and downloads
        results.sort(
            key=lambda x: (x.get("rating", 0), x.get("downloads", 0)),
            reverse=True
        )
        
        return results
    
    def update_plugin_stats(
        self,
        plugin_id: str,
        downloads: Optional[int] = None,
        rating: Optional[float] = None,
        review: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update plugin statistics."""
        if plugin_id not in self.registry:
            return False
        
        info = self.registry[plugin_id]
        
        if downloads is not None:
            info["downloads"] = downloads
        
        if rating is not None:
            info["rating"] = rating
        
        if review:
            info["reviews"].append({
                **review,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        self.save_registry()
        return True
    
    def get_popular_plugins(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular plugins."""
        plugins = list(self.registry.items())
        
        # Sort by downloads and rating
        plugins.sort(
            key=lambda x: (
                x[1].get("downloads", 0),
                x[1].get("rating", 0)
            ),
            reverse=True
        )
        
        return [
            {"plugin_id": plugin_id, **info}
            for plugin_id, info in plugins[:limit]
        ]
    
    def get_verified_plugins(self) -> List[Dict[str, Any]]:
        """Get verified plugins."""
        return [
            {"plugin_id": plugin_id, **info}
            for plugin_id, info in self.registry.items()
            if info.get("verified", False)
        ]
    
    def verify_plugin(self, plugin_id: str, verified: bool = True) -> bool:
        """Mark a plugin as verified."""
        if plugin_id in self.registry:
            self.registry[plugin_id]["verified"] = verified
            self.save_registry()
            return True
        return False
    
    def export_registry(self, output_path: Path) -> bool:
        """Export registry to file."""
        try:
            with open(output_path, 'w') as f:
                json.dump(
                    {
                        "version": "1.0",
                        "exported_at": datetime.utcnow().isoformat(),
                        "plugins": self.registry
                    },
                    f,
                    indent=2,
                    default=str
                )
            return True
        except Exception as e:
            logger.error(f"Failed to export registry: {e}")
            return False
    
    def import_registry(self, input_path: Path, merge: bool = True) -> bool:
        """Import registry from file."""
        try:
            with open(input_path, 'r') as f:
                data = json.load(f)
            
            imported_plugins = data.get("plugins", {})
            
            if merge:
                self.registry.update(imported_plugins)
            else:
                self.registry = imported_plugins
            
            self.save_registry()
            logger.info(f"Imported {len(imported_plugins)} plugins")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import registry: {e}")
            return False


class PluginMarketplace:
    """Marketplace for discovering and sharing plugins."""
    
    def __init__(self, registry: PluginRegistry):
        self.registry = registry
        self.featured_plugins: List[str] = []
        self.categories: Dict[str, List[str]] = {
            "Storage": [],
            "AI Models": [],
            "Analytics": [],
            "Visualization": [],
            "Integration": [],
            "Consciousness": []
        }
    
    def feature_plugin(self, plugin_id: str) -> bool:
        """Feature a plugin in the marketplace."""
        if plugin_id not in self.featured_plugins:
            self.featured_plugins.append(plugin_id)
            return True
        return False
    
    def categorize_plugin(self, plugin_id: str, category: str) -> bool:
        """Add plugin to a category."""
        if category in self.categories:
            if plugin_id not in self.categories[category]:
                self.categories[category].append(plugin_id)
                return True
        return False
    
    def get_featured_plugins(self) -> List[Dict[str, Any]]:
        """Get featured plugins."""
        featured = []
        for plugin_id in self.featured_plugins:
            info = self.registry.get_plugin_info(plugin_id)
            if info:
                featured.append({
                    "plugin_id": plugin_id,
                    **info
                })
        return featured
    
    def get_category_plugins(self, category: str) -> List[Dict[str, Any]]:
        """Get plugins in a category."""
        if category not in self.categories:
            return []
        
        plugins = []
        for plugin_id in self.categories[category]:
            info = self.registry.get_plugin_info(plugin_id)
            if info:
                plugins.append({
                    "plugin_id": plugin_id,
                    **info
                })
        return plugins
    
    def submit_plugin(
        self,
        metadata: PluginMetadata,
        source_url: str,
        category: str,
        description: str
    ) -> bool:
        """Submit a plugin to the marketplace."""
        # In production, this would:
        # 1. Validate the plugin
        # 2. Run security checks
        # 3. Test compatibility
        # 4. Request review
        
        # Register the plugin
        if self.registry.register_plugin(metadata, source_url):
            plugin_id = f"{metadata.name}@{metadata.version}"
            
            # Add to category
            if category in self.categories:
                self.categorize_plugin(plugin_id, category)
            
            logger.info(f"Plugin {plugin_id} submitted to marketplace")
            return True
        
        return False