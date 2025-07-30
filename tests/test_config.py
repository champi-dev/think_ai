"""
Test configuration loader for Think AI tests
Loads configuration from environment variables and config files
"""

import os
import toml
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ViewportConfig:
    name: str
    width: int
    height: int


@dataclass
class TestMessage:
    input: str
    expected_response_contains: List[str]


@dataclass
class MaliciousInput:
    input: str
    expected_status: int


class TestConfig:
    """Test configuration manager"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._find_config_file()
        self.config = self._load_config()
        self._resolve_env_vars()
    
    def _find_config_file(self) -> str:
        """Find the test config file"""
        possible_paths = [
            Path(__file__).parent / "test_config.toml",
            Path.cwd() / "test_config.toml",
            Path.cwd() / "tests" / "test_config.toml",
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        raise FileNotFoundError("Could not find test_config.toml")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from TOML file"""
        with open(self.config_path, 'r') as f:
            return toml.load(f)
    
    def _resolve_env_vars(self):
        """Resolve environment variables in config values"""
        def resolve_value(value):
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                # Extract env var name and default value
                env_expr = value[2:-1]
                if ":-" in env_expr:
                    var_name, default = env_expr.split(":-", 1)
                    return os.getenv(var_name, default)
                else:
                    return os.getenv(env_expr, value)
            elif isinstance(value, dict):
                return {k: resolve_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [resolve_value(v) for v in value]
            return value
        
        self.config = resolve_value(self.config)
    
    @property
    def server_url(self) -> str:
        """Get the server URL"""
        host = self.config['server']['host']
        port = self.config['server']['port']
        return f"http://{host}:{port}"
    
    @property
    def api_base_url(self) -> str:
        """Get the API base URL"""
        return self.config['api']['base_url']
    
    @property
    def viewports(self) -> List[ViewportConfig]:
        """Get viewport configurations"""
        return [
            ViewportConfig(**vp) 
            for vp in self.config['ui_testing']['viewports']
        ]
    
    @property
    def test_messages(self) -> List[TestMessage]:
        """Get test chat messages"""
        return [
            TestMessage(**msg) 
            for msg in self.config['test_data']['chat_messages']
        ]
    
    @property
    def malicious_inputs(self) -> List[MaliciousInput]:
        """Get malicious input test cases"""
        return [
            MaliciousInput(**inp) 
            for inp in self.config['test_data']['malicious_inputs']
        ]
    
    @property
    def performance_thresholds(self) -> Dict[str, int]:
        """Get performance test thresholds"""
        return self.config['performance']
    
    @property
    def is_headless(self) -> bool:
        """Check if UI tests should run headless"""
        return self.config['ui_testing']['headless'].lower() == 'true'
    
    @property
    def should_mock_llm(self) -> bool:
        """Check if LLM should be mocked"""
        return self.config['test_environment']['use_mock_llm'].lower() == 'true'
    
    @property
    def max_concurrent_tests(self) -> int:
        """Get max concurrent tests"""
        return int(self.config['test_environment']['max_concurrent_tests'])
    
    def get_endpoint(self, endpoint_name: str) -> str:
        """Get a specific API endpoint"""
        base_url = self.api_base_url
        endpoint = self.config['api'].get(f"{endpoint_name}_endpoint", "")
        return f"{base_url}{endpoint}"
    
    def save_test_results(self, results: Dict[str, Any], filename: str = None):
        """Save test results to file"""
        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_{timestamp}.json"
        
        results_path = Path(self.config['test_environment']['test_data_dir']) / filename
        results_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results_path


# Global config instance
_config: Optional[TestConfig] = None


def get_config() -> TestConfig:
    """Get the global test configuration"""
    global _config
    if _config is None:
        _config = TestConfig()
    return _config


def reset_config():
    """Reset the global configuration (useful for tests)"""
    global _config
    _config = None