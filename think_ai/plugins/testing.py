"""Plugin testing framework for Think AI."""

import asyncio
import pytest
from typing import Dict, Any, List, Optional, Type
from pathlib import Path
import tempfile
import json
from datetime import datetime

from .base import (
    Plugin,
    PluginMetadata,
    PluginContext,
    PluginCapability,
    PluginError
)
from .manager import PluginManager
from ..consciousness.principles import ConstitutionalAI
from ..utils.logging import get_logger


logger = get_logger(__name__)


class PluginTestCase:
    """Base test case for plugin testing."""
    
    def __init__(self, plugin_class: Type[Plugin]):
        self.plugin_class = plugin_class
        self.plugin: Optional[Plugin] = None
        self.context: Optional[PluginContext] = None
        self.temp_dir: Optional[Path] = None
    
    async def setup(self, config: Dict[str, Any] = None) -> None:
        """Set up test environment."""
        # Create temp directory
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Create mock context
        self.context = PluginContext(
            engine=MockEngine(),
            config=config or {},
            constitutional_ai=ConstitutionalAI()
        )
        
        # Create plugin instance
        self.plugin = self.plugin_class()
        
        # Initialize
        await self.plugin.initialize(self.context)
    
    async def teardown(self) -> None:
        """Clean up test environment."""
        if self.plugin:
            await self.plugin.shutdown()
        
        if self.temp_dir and self.temp_dir.exists():
            import shutil
            shutil.rmtree(self.temp_dir)
    
    async def test_metadata(self) -> Dict[str, Any]:
        """Test plugin metadata."""
        metadata = self.plugin.metadata
        
        results = {
            "has_name": bool(metadata.name),
            "has_version": bool(metadata.version),
            "has_author": bool(metadata.author),
            "has_description": bool(metadata.description),
            "has_capabilities": len(metadata.capabilities) > 0,
            "love_aligned": metadata.love_aligned,
            "valid_version": self._validate_version(metadata.version)
        }
        
        return {
            "passed": all(results.values()),
            "results": results
        }
    
    async def test_initialization(self) -> Dict[str, Any]:
        """Test plugin initialization."""
        results = {
            "initialized": self.plugin._initialized,
            "has_context": self.plugin._context is not None,
            "health_check_passes": False
        }
        
        try:
            health = await self.plugin.health_check()
            results["health_check_passes"] = health.get("status") == "healthy"
        except Exception as e:
            logger.error(f"Health check failed: {e}")
        
        return {
            "passed": all(results.values()),
            "results": results
        }
    
    async def test_ethical_compliance(self, test_content: List[str]) -> Dict[str, Any]:
        """Test ethical compliance checking."""
        results = {}
        
        for content in test_content:
            try:
                compliant = await self.plugin.check_ethical_compliance(content)
                results[content[:50]] = compliant
            except Exception as e:
                results[content[:50]] = f"Error: {e}"
        
        # Good content should pass, bad content should fail
        expected_results = {
            "Helping others with compassion": True,
            "Sharing knowledge freely": True,
            "Harmful content": False,
            "Exploitative behavior": False
        }
        
        passed = all(
            results.get(k[:50], False) == v
            for k, v in expected_results.items()
            if k[:50] in results
        )
        
        return {
            "passed": passed,
            "results": results
        }
    
    async def test_performance(self, operations: int = 100) -> Dict[str, Any]:
        """Test plugin performance."""
        import time
        
        results = {
            "operations": operations,
            "start_time": time.time()
        }
        
        # Run operations
        try:
            for i in range(operations):
                await self._perform_test_operation(i)
            
            results["end_time"] = time.time()
            results["duration"] = results["end_time"] - results["start_time"]
            results["ops_per_second"] = operations / results["duration"]
            results["passed"] = True
            
        except Exception as e:
            results["error"] = str(e)
            results["passed"] = False
        
        return results
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling."""
        results = {}
        
        # Test various error conditions
        test_cases = [
            ("null_input", None),
            ("empty_string", ""),
            ("invalid_type", [1, 2, 3]),
            ("large_input", "x" * 1000000)
        ]
        
        for test_name, test_input in test_cases:
            try:
                await self._perform_error_test(test_input)
                results[test_name] = "handled"
            except Exception as e:
                results[test_name] = f"unhandled: {type(e).__name__}"
        
        # All errors should be handled gracefully
        passed = all("unhandled" not in str(v) for v in results.values())
        
        return {
            "passed": passed,
            "results": results
        }
    
    async def test_resource_usage(self) -> Dict[str, Any]:
        """Test resource usage."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Baseline measurements
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
        baseline_cpu = process.cpu_percent(interval=0.1)
        
        # Run intensive operations
        for _ in range(1000):
            await self._perform_test_operation(_)
        
        # Measure after operations
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        final_cpu = process.cpu_percent(interval=0.1)
        
        results = {
            "memory_increase_mb": final_memory - baseline_memory,
            "cpu_usage_percent": final_cpu,
            "memory_reasonable": (final_memory - baseline_memory) < 100,  # Less than 100MB increase
            "cpu_reasonable": final_cpu < 80  # Less than 80% CPU
        }
        
        results["passed"] = results["memory_reasonable"] and results["cpu_reasonable"]
        
        return results
    
    def _validate_version(self, version: str) -> bool:
        """Validate semantic versioning."""
        import re
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$'
        return bool(re.match(pattern, version))
    
    async def _perform_test_operation(self, index: int) -> Any:
        """Override to implement plugin-specific test operation."""
        # Default: just check health
        return await self.plugin.health_check()
    
    async def _perform_error_test(self, test_input: Any) -> Any:
        """Override to implement plugin-specific error test."""
        # Default: try to process input
        if hasattr(self.plugin, 'process'):
            return await self.plugin.process(test_input)
        return None


class PluginTestSuite:
    """Complete test suite for plugins."""
    
    def __init__(self, plugin_class: Type[Plugin]):
        self.plugin_class = plugin_class
        self.test_case = PluginTestCase(plugin_class)
        self.results: Dict[str, Any] = {}
    
    async def run_all_tests(self, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run all tests."""
        try:
            # Setup
            await self.test_case.setup(config)
            
            # Run tests
            self.results["metadata"] = await self.test_case.test_metadata()
            self.results["initialization"] = await self.test_case.test_initialization()
            
            # Ethical compliance tests
            test_content = [
                "Helping others with compassion",
                "Sharing knowledge freely",
                "Building community connections",
                "Harmful content",
                "Exploitative behavior",
                "Discriminatory language"
            ]
            self.results["ethical_compliance"] = await self.test_case.test_ethical_compliance(test_content)
            
            # Performance tests
            self.results["performance"] = await self.test_case.test_performance()
            
            # Error handling tests
            self.results["error_handling"] = await self.test_case.test_error_handling()
            
            # Resource usage tests
            self.results["resource_usage"] = await self.test_case.test_resource_usage()
            
            # Calculate overall result
            self.results["overall_passed"] = all(
                test.get("passed", False)
                for test in self.results.values()
                if isinstance(test, dict)
            )
            
            self.results["timestamp"] = datetime.now().isoformat()
            
        finally:
            # Teardown
            await self.test_case.teardown()
        
        return self.results
    
    def generate_report(self) -> str:
        """Generate test report."""
        report_lines = [
            f"Plugin Test Report",
            f"==================",
            f"Plugin: {self.plugin_class.__name__}",
            f"Timestamp: {self.results.get('timestamp', 'N/A')}",
            f"Overall: {'PASSED' if self.results.get('overall_passed') else 'FAILED'}",
            "",
            "Test Results:",
            "-------------"
        ]
        
        for test_name, test_result in self.results.items():
            if test_name in ["overall_passed", "timestamp"]:
                continue
            
            if isinstance(test_result, dict):
                status = "PASSED" if test_result.get("passed") else "FAILED"
                report_lines.append(f"  {test_name}: {status}")
                
                # Add details for failed tests
                if not test_result.get("passed"):
                    for key, value in test_result.get("results", {}).items():
                        report_lines.append(f"    - {key}: {value}")
        
        return "\n".join(report_lines)


class MockEngine:
    """Mock engine for testing."""
    
    def __init__(self):
        self.storage_backends = ["mock_storage"]
        self.vector_stores = ["mock_vector"]


def create_test_plugin(
    name: str = "test_plugin",
    capabilities: List[PluginCapability] = None
) -> Type[Plugin]:
    """Create a test plugin class."""
    
    class TestPlugin(Plugin):
        METADATA = PluginMetadata(
            name=name,
            version="1.0.0",
            author="Test Author",
            description="Test plugin for testing",
            capabilities=capabilities or [PluginCapability.ANALYTICS],
            love_aligned=True
        )
        
        def __init__(self):
            super().__init__(self.METADATA)
            self.operations = []
        
        async def initialize(self, context: PluginContext) -> None:
            await super().initialize(context)
            self.operations.append("initialized")
        
        async def shutdown(self) -> None:
            self.operations.append("shutdown")
            await super().shutdown()
        
        async def process(self, data: Any) -> Any:
            """Process data."""
            if data is None:
                raise ValueError("Data cannot be None")
            
            self.operations.append(f"process:{data}")
            return f"processed:{data}"
        
        async def health_check(self) -> Dict[str, Any]:
            health = await super().health_check()
            health["operations_count"] = len(self.operations)
            return health
    
    return TestPlugin


# Pytest fixtures
@pytest.fixture
async def plugin_test_case():
    """Create a plugin test case."""
    plugin_class = create_test_plugin()
    test_case = PluginTestCase(plugin_class)
    await test_case.setup()
    yield test_case
    await test_case.teardown()


@pytest.fixture
async def plugin_manager():
    """Create a plugin manager."""
    temp_dir = Path(tempfile.mkdtemp())
    manager = PluginManager(plugin_dir=temp_dir)
    yield manager
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


# Example test functions
@pytest.mark.asyncio
async def test_plugin_lifecycle(plugin_test_case):
    """Test plugin lifecycle."""
    assert plugin_test_case.plugin._initialized
    
    # Test operation
    result = await plugin_test_case.plugin.process("test_data")
    assert result == "processed:test_data"
    
    # Check operations log
    assert "initialized" in plugin_test_case.plugin.operations
    assert "process:test_data" in plugin_test_case.plugin.operations


@pytest.mark.asyncio
async def test_plugin_error_handling(plugin_test_case):
    """Test plugin error handling."""
    with pytest.raises(ValueError):
        await plugin_test_case.plugin.process(None)


@pytest.mark.asyncio
async def test_plugin_health_check(plugin_test_case):
    """Test plugin health check."""
    health = await plugin_test_case.plugin.health_check()
    
    assert health["status"] == "healthy"
    assert health["plugin"] == "test_plugin"
    assert health["version"] == "1.0.0"
    assert "operations_count" in health