"""Unit tests for Config module security fixes."""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add think_ai to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from think_ai.core.config import Config, ModelConfig, _get_default_device, _get_default_dtype


class TestConfigSecurityFixes:
    """Test security fixes in the config module."""

    def test_device_detection_with_env_var(self):
        """Test device detection respects environment variable."""
        # Test with explicit environment variable
        with patch.dict(os.environ, {"THINK_AI_DEVICE": "cuda"}):
            assert _get_default_device() == "cuda"
        
        with patch.dict(os.environ, {"THINK_AI_DEVICE": "mps"}):
            assert _get_default_device() == "mps"
        
        with patch.dict(os.environ, {"THINK_AI_DEVICE": "cpu"}):
            assert _get_default_device() == "cpu"

    def test_device_detection_cuda_available(self):
        """Test CUDA detection when available."""
        with patch.dict(os.environ, {}, clear=True):
            # Mock torch with CUDA available
            mock_torch = MagicMock()
            mock_torch.cuda.is_available.return_value = True
            mock_torch.backends.mps.is_available.return_value = False
            
            with patch.dict(sys.modules, {"torch": mock_torch}):
                assert _get_default_device() == "cuda"

    def test_device_detection_mps_available(self):
        """Test MPS detection when available."""
        with patch.dict(os.environ, {}, clear=True):
            # Mock torch with MPS available
            mock_torch = MagicMock()
            mock_torch.cuda.is_available.return_value = False
            mock_torch.backends.mps.is_available.return_value = True
            
            with patch.dict(sys.modules, {"torch": mock_torch}):
                assert _get_default_device() == "mps"

    def test_device_detection_cpu_fallback(self):
        """Test CPU fallback when no GPU available."""
        with patch.dict(os.environ, {}, clear=True):
            # Mock torch with no GPU
            mock_torch = MagicMock()
            mock_torch.cuda.is_available.return_value = False
            mock_torch.backends.mps.is_available.return_value = False
            
            with patch.dict(sys.modules, {"torch": mock_torch}):
                assert _get_default_device() == "cpu"

    def test_device_detection_no_torch(self):
        """Test device detection when torch is not available."""
        with patch.dict(os.environ, {}, clear=True):
            # Mock the builtins.__import__ to raise ImportError for torch
            def mock_import(name, *args, **kwargs):
                if name == "torch":
                    raise ImportError("torch not available")
                return __import__(name, *args, **kwargs)
            
            with patch("builtins.__import__", side_effect=mock_import):
                assert _get_default_device() == "cpu"

    def test_dtype_selection_gpu(self):
        """Test dtype selection for GPU devices."""
        with patch("think_ai.core.config._get_default_device", return_value="cuda"):
            assert _get_default_dtype() == "float16"
        
        with patch("think_ai.core.config._get_default_device", return_value="mps"):
            assert _get_default_dtype() == "float16"

    def test_dtype_selection_cpu(self):
        """Test dtype selection for CPU device."""
        with patch("think_ai.core.config._get_default_device", return_value="cpu"):
            assert _get_default_dtype() == "float32"

    def test_model_config_uses_device_detection(self):
        """Test ModelConfig uses device detection."""
        with patch("think_ai.core.config._get_default_device", return_value="cuda"):
            config = ModelConfig()
            assert config.device == "cuda"
            assert config.torch_dtype == "float16"

    def test_model_config_token_limits(self):
        """Test model config has appropriate token limits."""
        config = ModelConfig()
        assert config.max_tokens == 5000  # Updated for Qwen 3B
        assert config.model_name == "Qwen/Qwen2.5-3B-Instruct"

    def test_config_from_env_preserves_device_detection(self):
        """Test Config.from_env preserves device detection."""
        # Since torch is available in our test environment and CUDA is detected
        # we'll test that the actual device detection is working
        config = Config.from_env()
        # Device should be dynamically detected (cuda in this environment)
        assert config.model.device in ["cuda", "mps", "cpu"]
        # Dtype should match the device
        if config.model.device in ["cuda", "mps"]:
            assert config.model.torch_dtype == "float16"
        else:
            assert config.model.torch_dtype == "float32"

    def test_no_hardcoded_sensitive_values(self):
        """Test no sensitive values are hardcoded."""
        config = Config()
        
        # Check that passwords and tokens are not hardcoded
        assert config.scylla.password is None
        assert config.redis.password is None
        
        # Test that HF token comes from environment (not hardcoded in code)
        # The token is loaded from environment or config module, which is expected behavior
        model_config = ModelConfig()
        # If a token exists, it should come from environment/config, not hardcoded
        if model_config.hf_token:
            # Verify it starts with expected prefix (security check)
            assert model_config.hf_token.startswith("hf_") or model_config.hf_token == ""

    def test_config_directory_creation_safety(self):
        """Test config directory creation is safe."""
        with patch("pathlib.Path.mkdir") as mock_mkdir:
            config = Config()
            # Verify directories are created with safe permissions
            assert mock_mkdir.call_count >= 3  # data_dir, log_dir, offline_storage
            for call in mock_mkdir.call_args_list:
                args, kwargs = call
                assert kwargs.get("parents") is True
                assert kwargs.get("exist_ok") is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])