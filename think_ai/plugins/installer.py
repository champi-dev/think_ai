"""Plugin installer for Think AI."""

import os
import json
import shutil
import tempfile
import hashlib
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from urllib.parse import urlparse
import subprocess
import zipfile
import tarfile

from .base import PluginMetadata, PluginCapability
from .manager import PluginManager
from .registry import PluginRegistry
from ..utils.logging import get_logger


logger = get_logger(__name__)


class PluginInstaller:
    """Handles plugin installation, updates, and removal."""
    
    def __init__(
        self,
        plugin_dir: Path,
        registry: PluginRegistry,
        manager: PluginManager
    ):
        self.plugin_dir = plugin_dir
        self.registry = registry
        self.manager = manager
        self.temp_dir = Path(tempfile.gettempdir()) / "think_ai_plugins"
        self.temp_dir.mkdir(exist_ok=True)
    
    async def install_from_url(
        self,
        url: str,
        verify_signature: bool = True
    ) -> Tuple[bool, str]:
        """Install a plugin from URL."""
        try:
            logger.info(f"Installing plugin from {url}")
            
            # Download plugin
            plugin_path = await self._download_plugin(url)
            
            # Verify plugin
            if verify_signature:
                if not await self._verify_plugin_signature(plugin_path):
                    return False, "Plugin signature verification failed"
            
            # Extract and validate
            metadata = await self._extract_and_validate(plugin_path)
            
            if not metadata:
                return False, "Invalid plugin package"
            
            # Check love alignment
            if not metadata.love_aligned:
                return False, "Plugin is not love-aligned"
            
            # Install
            success = await self._install_plugin_files(plugin_path, metadata)
            
            if success:
                # Register in registry
                self.registry.register_plugin(metadata, url, verified=verify_signature)
                
                # Install dependencies
                await self._install_dependencies(metadata)
                
                return True, f"Successfully installed {metadata.name} v{metadata.version}"
            
            return False, "Failed to install plugin files"
            
        except Exception as e:
            logger.error(f"Plugin installation failed: {e}")
            return False, f"Installation error: {str(e)}"
    
    async def install_from_file(
        self,
        file_path: Path,
        verify_signature: bool = True
    ) -> Tuple[bool, str]:
        """Install a plugin from local file."""
        if not file_path.exists():
            return False, f"Plugin file not found: {file_path}"
        
        # Treat as URL for consistency
        return await self.install_from_url(
            f"file://{file_path.absolute()}",
            verify_signature
        )
    
    async def update_plugin(
        self,
        plugin_name: str,
        version: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Update an installed plugin."""
        try:
            # Get plugin info from registry
            current_plugins = self.registry.search_plugins(
                query=plugin_name,
                love_aligned_only=True
            )
            
            if not current_plugins:
                return False, f"Plugin {plugin_name} not found"
            
            current = current_plugins[0]
            source_url = current.get("source_url")
            
            if not source_url:
                return False, "No update source available"
            
            # Check for updates
            latest_version = await self._check_latest_version(source_url)
            
            if version:
                target_version = version
            else:
                target_version = latest_version
            
            if target_version == current["metadata"]["version"]:
                return False, "Already at target version"
            
            # Backup current version
            backup_path = await self._backup_plugin(plugin_name)
            
            try:
                # Unload plugin if loaded
                if self.manager.get_plugin(plugin_name):
                    await self.manager.unload_plugin(plugin_name)
                
                # Install new version
                success, message = await self.install_from_url(
                    source_url.replace(
                        current["metadata"]["version"],
                        target_version
                    )
                )
                
                if success:
                    # Remove backup
                    shutil.rmtree(backup_path)
                    return True, f"Updated {plugin_name} to v{target_version}"
                else:
                    # Restore backup
                    await self._restore_plugin(plugin_name, backup_path)
                    return False, f"Update failed: {message}"
                    
            except Exception as e:
                # Restore backup
                await self._restore_plugin(plugin_name, backup_path)
                raise e
                
        except Exception as e:
            logger.error(f"Plugin update failed: {e}")
            return False, f"Update error: {str(e)}"
    
    async def uninstall_plugin(
        self,
        plugin_name: str,
        remove_data: bool = False
    ) -> Tuple[bool, str]:
        """Uninstall a plugin."""
        try:
            # Unload plugin if loaded
            if self.manager.get_plugin(plugin_name):
                await self.manager.unload_plugin(plugin_name)
            
            # Find plugin files
            plugin_path = self.plugin_dir / plugin_name
            
            if not plugin_path.exists():
                # Try alternative locations
                plugin_path = None
                for file in self.plugin_dir.glob(f"{plugin_name}*"):
                    if file.is_dir():
                        plugin_path = file
                        break
            
            if not plugin_path:
                return False, f"Plugin {plugin_name} not found"
            
            # Remove plugin files
            shutil.rmtree(plugin_path)
            
            # Remove from registry
            plugins = self.registry.search_plugins(query=plugin_name)
            for plugin in plugins:
                self.registry.unregister_plugin(plugin["plugin_id"])
            
            # Remove data if requested
            if remove_data:
                data_path = Path.home() / ".think_ai" / "plugin_data" / plugin_name
                if data_path.exists():
                    shutil.rmtree(data_path)
            
            return True, f"Successfully uninstalled {plugin_name}"
            
        except Exception as e:
            logger.error(f"Plugin uninstall failed: {e}")
            return False, f"Uninstall error: {str(e)}"
    
    async def list_installed_plugins(self) -> List[Dict[str, Any]]:
        """List all installed plugins."""
        installed = []
        
        # Check plugin directory
        for path in self.plugin_dir.iterdir():
            if path.is_dir() and not path.name.startswith("_"):
                manifest_path = path / "manifest.json"
                if manifest_path.exists():
                    try:
                        with open(manifest_path) as f:
                            manifest = json.load(f)
                        
                        installed.append({
                            "name": manifest["name"],
                            "version": manifest["version"],
                            "path": str(path),
                            "enabled": manifest["name"] in self.manager.plugins
                        })
                    except:
                        pass
        
        return installed
    
    async def check_updates(self) -> List[Dict[str, Any]]:
        """Check for available updates."""
        updates = []
        
        for plugin in await self.list_installed_plugins():
            plugin_info = self.registry.get_plugin_info(
                f"{plugin['name']}@{plugin['version']}"
            )
            
            if plugin_info and plugin_info.get("source_url"):
                latest = await self._check_latest_version(
                    plugin_info["source_url"]
                )
                
                if latest and latest != plugin["version"]:
                    updates.append({
                        "name": plugin["name"],
                        "current_version": plugin["version"],
                        "latest_version": latest,
                        "source": plugin_info["source_url"]
                    })
        
        return updates
    
    async def _download_plugin(self, url: str) -> Path:
        """Download plugin from URL."""
        parsed = urlparse(url)
        
        if parsed.scheme == "file":
            # Local file
            return Path(parsed.path)
        
        elif parsed.scheme in ["http", "https"]:
            # Download from web
            import aiohttp
            
            filename = os.path.basename(parsed.path) or "plugin.zip"
            download_path = self.temp_dir / filename
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    
                    with open(download_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            f.write(chunk)
            
            return download_path
        
        else:
            raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")
    
    async def _verify_plugin_signature(self, plugin_path: Path) -> bool:
        """Verify plugin signature."""
        # In production, this would:
        # 1. Check cryptographic signature
        # 2. Verify against trusted keys
        # 3. Check integrity
        
        # For now, just check hash
        signature_path = plugin_path.with_suffix(".sig")
        
        if signature_path.exists():
            with open(plugin_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            with open(signature_path, 'r') as f:
                expected_hash = f.read().strip()
            
            return file_hash == expected_hash
        
        # No signature file - warn but allow
        logger.warning(f"No signature file found for {plugin_path}")
        return True
    
    async def _extract_and_validate(self, plugin_path: Path) -> Optional[PluginMetadata]:
        """Extract and validate plugin package."""
        extract_dir = self.temp_dir / f"extract_{plugin_path.stem}"
        
        try:
            # Extract based on file type
            if plugin_path.suffix == ".zip":
                with zipfile.ZipFile(plugin_path) as zf:
                    zf.extractall(extract_dir)
            
            elif plugin_path.suffix in [".tar", ".gz", ".tgz"]:
                with tarfile.open(plugin_path) as tf:
                    tf.extractall(extract_dir)
            
            else:
                # Single file plugin
                extract_dir.mkdir(exist_ok=True)
                shutil.copy2(plugin_path, extract_dir)
            
            # Find manifest
            manifest_path = extract_dir / "manifest.json"
            
            if not manifest_path.exists():
                # Look in subdirectories
                for path in extract_dir.rglob("manifest.json"):
                    manifest_path = path
                    break
            
            if not manifest_path.exists():
                logger.error("No manifest.json found in plugin package")
                return None
            
            # Load and validate manifest
            with open(manifest_path) as f:
                manifest = json.load(f)
            
            # Create metadata
            metadata = PluginMetadata(
                name=manifest["name"],
                version=manifest["version"],
                author=manifest["author"],
                description=manifest["description"],
                capabilities=[
                    PluginCapability(c) for c in manifest["capabilities"]
                ],
                dependencies=manifest.get("dependencies", []),
                love_aligned=manifest.get("love_aligned", True),
                ethical_review_passed=manifest.get("ethical_review_passed", False),
                license=manifest.get("license", "Apache-2.0"),
                tags=manifest.get("tags", [])
            )
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to extract/validate plugin: {e}")
            return None
        
        finally:
            # Keep extract dir for installation
            pass
    
    async def _install_plugin_files(
        self,
        plugin_path: Path,
        metadata: PluginMetadata
    ) -> bool:
        """Install plugin files to plugin directory."""
        try:
            # Determine source directory
            if plugin_path.is_file():
                source_dir = self.temp_dir / f"extract_{plugin_path.stem}"
            else:
                source_dir = plugin_path
            
            # Determine destination
            dest_dir = self.plugin_dir / metadata.name
            
            # Remove existing if present
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            
            # Copy files
            shutil.copytree(source_dir, dest_dir)
            
            # Create manifest in destination
            manifest_path = dest_dir / "manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump({
                    "name": metadata.name,
                    "version": metadata.version,
                    "author": metadata.author,
                    "description": metadata.description,
                    "capabilities": [c.value for c in metadata.capabilities],
                    "dependencies": metadata.dependencies,
                    "love_aligned": metadata.love_aligned,
                    "ethical_review_passed": metadata.ethical_review_passed,
                    "license": metadata.license,
                    "tags": metadata.tags
                }, f, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to install plugin files: {e}")
            return False
    
    async def _install_dependencies(self, metadata: PluginMetadata) -> None:
        """Install plugin dependencies."""
        if not metadata.dependencies:
            return
        
        try:
            # Use pip to install dependencies
            cmd = [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--quiet"
            ] + metadata.dependencies
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.warning(
                    f"Failed to install some dependencies: {stderr.decode()}"
                )
            else:
                logger.info(f"Installed dependencies for {metadata.name}")
                
        except Exception as e:
            logger.warning(f"Failed to install dependencies: {e}")
    
    async def _check_latest_version(self, source_url: str) -> Optional[str]:
        """Check the latest version available."""
        # In production, this would:
        # 1. Query version endpoint
        # 2. Parse version manifest
        # 3. Compare versions
        
        # For now, return None (no update available)
        return None
    
    async def _backup_plugin(self, plugin_name: str) -> Path:
        """Backup a plugin before update."""
        plugin_path = self.plugin_dir / plugin_name
        backup_path = self.temp_dir / f"{plugin_name}_backup"
        
        if backup_path.exists():
            shutil.rmtree(backup_path)
        
        shutil.copytree(plugin_path, backup_path)
        return backup_path
    
    async def _restore_plugin(self, plugin_name: str, backup_path: Path) -> None:
        """Restore plugin from backup."""
        plugin_path = self.plugin_dir / plugin_name
        
        if plugin_path.exists():
            shutil.rmtree(plugin_path)
        
        shutil.copytree(backup_path, plugin_path)
        shutil.rmtree(backup_path)