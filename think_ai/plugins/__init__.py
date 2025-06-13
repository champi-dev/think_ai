"""Plugin architecture for Think AI extensibility."""

from .base import Plugin, PluginMetadata, PluginCapability
from .manager import PluginManager
from .registry import PluginRegistry

__all__ = [
    "Plugin",
    "PluginMetadata",
    "PluginCapability",
    "PluginManager",
    "PluginRegistry"
]