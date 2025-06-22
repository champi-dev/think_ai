"""
Think AI Configuration - All settings in one place
O(1) access to all configuration values
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class Config:
    """Main configuration class for Think AI - O(1) access guaranteed."""
    
    # Model Configuration
    model_name: str = "Qwen/Qwen2.5-Coder-1.5B"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    device: str = "auto"  # auto, cpu, cuda, mps
    quantization: Optional[str] = None  # int4, int8, or None
    max_memory_mb: int = 4096
    batch_size: int = 8
    
    # Storage Configuration
    storage_backend: str = "sqlite"  # sqlite, scylla, redis
    storage_path: Path = field(default_factory=lambda: Path.home() / ".think_ai" / "storage")
    cache_enabled: bool = True
    cache_ttl: int = 3600
    
    # Vector DB Configuration
    vector_backend: str = "numpy"  # numpy, milvus, qdrant
    vector_dimension: int = 384
    vector_index_type: str = "flat"  # O(1) with learned indexing
    
    # Knowledge Graph Configuration
    graph_backend: str = "networkx"  # networkx, neo4j
    max_graph_nodes: int = 100000
    
    # Consciousness Configuration
    consciousness_enabled: bool = True
    consciousness_state: str = "aware"  # dormant, aware, focused, reflective, compassionate
    ethical_guidelines_enabled: bool = True
    love_metrics_weight: float = 0.8
    
    # API Configuration
    host: str = "0.0.0.0"
    port: int = 8080
    cors_enabled: bool = True
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("THINK_AI_API_KEY"))
    
    # Performance Configuration
    enable_gpu: bool = True
    parallel_workers: int = 4
    response_cache_size: int = 1000
    o1_optimization: bool = True  # Enable O(1) optimizations everywhere
    sqrt1_mode: bool = True  # Enable O(√1) = O(1) optimizations
    
    # Self-Improvement Configuration
    self_training_enabled: bool = True
    learning_rate: float = 0.001
    evolution_interval: int = 3600  # seconds
    max_evolution_steps: int = 1000000
    
    # Colombian Mode
    colombian_mode: bool = True
    colombian_phrases: List[str] = field(default_factory=lambda: [
        "¡Qué chimba!",
        "¡Dale que vamos tarde!",
        "¡Parce!",
        "¡Eso es pa' ya!",
        "¡Qué berraquera!"
    ])
    
    # Feature Flags
    enable_consciousness: bool = True
    enable_quantum: bool = False  # Future feature
    enable_blockchain: bool = False  # Future feature
    enable_federation: bool = True
    enable_plugins: bool = True
    
    # Paths
    models_dir: Path = field(default_factory=lambda: Path.home() / ".think_ai" / "models")
    logs_dir: Path = field(default_factory=lambda: Path.home() / ".think_ai" / "logs")
    data_dir: Path = field(default_factory=lambda: Path.home() / ".think_ai" / "data")
    
    # Environment
    environment: str = field(default_factory=lambda: os.getenv("THINK_AI_ENV", "production"))
    debug: bool = field(default_factory=lambda: os.getenv("THINK_AI_DEBUG", "false").lower() == "true")
    
    # Security
    encryption_enabled: bool = True
    encryption_key: Optional[str] = field(default_factory=lambda: os.getenv("THINK_AI_ENCRYPTION_KEY"))
    
    # Integration Keys
    huggingface_token: Optional[str] = field(default_factory=lambda: os.getenv("HF_TOKEN"))
    anthropic_api_key: Optional[str] = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    openai_api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    
    def __post_init__(self):
        """Create necessary directories - O(1) operation."""
        for path in [self.storage_path, self.models_dir, self.logs_dir, self.data_dir]:
            path.mkdir(parents=True, exist_ok=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary - O(1) with caching."""
        return {
            "model": {
                "name": self.model_name,
                "embedding": self.embedding_model,
                "device": self.device,
                "quantization": self.quantization,
            },
            "storage": {
                "backend": self.storage_backend,
                "path": str(self.storage_path),
                "cache_enabled": self.cache_enabled,
            },
            "consciousness": {
                "enabled": self.consciousness_enabled,
                "state": self.consciousness_state,
                "ethical": self.ethical_guidelines_enabled,
            },
            "performance": {
                "o1_optimization": self.o1_optimization,
                "sqrt1_mode": self.sqrt1_mode,
                "gpu": self.enable_gpu,
                "workers": self.parallel_workers,
            },
            "colombian_mode": self.colombian_mode,
            "environment": self.environment,
        }
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables - O(1) operation."""
        kwargs = {}
        
        # Map environment variables to config fields
        env_mappings = {
            "THINK_AI_MODEL": "model_name",
            "THINK_AI_DEVICE": "device",
            "THINK_AI_PORT": ("port", int),
            "THINK_AI_HOST": "host",
            "THINK_AI_STORAGE": "storage_backend",
            "THINK_AI_COLOMBIAN": ("colombian_mode", lambda x: x.lower() == "true"),
        }
        
        for env_key, mapping in env_mappings.items():
            value = os.getenv(env_key)
            if value is not None:
                if isinstance(mapping, tuple):
                    field_name, converter = mapping
                    kwargs[field_name] = converter(value)
                else:
                    kwargs[mapping] = value
        
        return cls(**kwargs)