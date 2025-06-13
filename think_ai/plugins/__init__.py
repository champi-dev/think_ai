"""Plugin architecture for Think AI extensibility."""

from .base import Plugin, PluginCapability, PluginMetadata
from .manager import PluginManager
from .registry import PluginRegistry

__all__ = [
    "Plugin",
    "PluginCapability",
    "PluginManager",
    "PluginMetadata",
    "PluginRegistry",
]
