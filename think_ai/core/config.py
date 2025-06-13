"""Configuration management for Think AI system."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ScyllaDBConfig:
    """ScyllaDB configuration settings."""
    hosts: List[str] = field(default_factory=lambda: ["127.0.0.1"])
    port: int = 9042
    keyspace: str = "think_ai"
    replication_factor: int = 3
    consistency_level: str = "QUORUM"
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass
class RedisConfig:
    """Redis configuration settings."""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    max_connections: int = 100
    decode_responses: bool = True
    cluster_mode: bool = False


@dataclass
class VectorDBConfig:
    """Vector database configuration settings."""
    provider: str = "milvus"  # milvus or qdrant
    host: str = "localhost"
    port: int = 19530  # Default Milvus port
    collection_name: str = "think_ai_vectors"
    dimension: int = 768
    index_type: str = "HNSW"
    metric_type: str = "L2"
    ef_construction: int = 200
    m: int = 16


@dataclass
class OfflineStorageConfig:
    """Offline storage configuration using SQLite."""
    db_path: Path = field(default_factory=lambda: Path.home() / ".think_ai" / "offline.db")
    enable_fts: bool = True
    cache_size_mb: int = 256
    wal_mode: bool = True


@dataclass
class ModelConfig:
    """AI model configuration settings."""
    model_name: str = "EleutherAI/pythia-2.8b"
    quantization: str = "int4"
    device: str = "cpu"
    max_tokens: int = 2048
    temperature: float = 0.7
    offline_model_path: Optional[Path] = None


@dataclass
class UIConfig:
    """Terminal UI configuration settings."""
    theme: str = "dark"
    color_scheme: str = "monokai"
    enable_mouse: bool = True
    enable_animations: bool = True
    log_level: str = "INFO"


@dataclass
class ConsciousnessConfig:
    """Consciousness-aware AI configuration."""
    enable_compassion_metrics: bool = True
    harm_prevention_levels: List[str] = field(
        default_factory=lambda: ["physical", "financial", "privacy", "discrimination", "societal"]
    )
    ethical_framework: str = "constitutional_ai"
    love_based_design: bool = True
    empathy_threshold: float = 0.8


@dataclass 
class GraphDBConfig:
    """Graph database configuration."""
    provider: str = "neo4j"
    uri: str = "bolt://localhost:7687"
    username: str = "neo4j"
    password: str = "password"
    database: str = "neo4j"


@dataclass
class Config:
    """Main configuration class for Think AI system."""
    
    scylla: ScyllaDBConfig = field(default_factory=ScyllaDBConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    vector_db: VectorDBConfig = field(default_factory=VectorDBConfig)
    offline_storage: OfflineStorageConfig = field(default_factory=OfflineStorageConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    consciousness: ConsciousnessConfig = field(default_factory=ConsciousnessConfig)
    graph_db: GraphDBConfig = field(default_factory=GraphDBConfig)
    
    # General settings
    app_name: str = "Think AI"
    version: str = "0.1.0"
    debug: bool = False
    data_dir: Path = field(default_factory=lambda: Path.home() / ".think_ai")
    log_dir: Path = field(default_factory=lambda: Path.home() / ".think_ai" / "logs")
    
    def __post_init__(self):
        """Create necessary directories."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.offline_storage.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        config = cls()
        
        # Override with environment variables if present
        if hosts := os.getenv("SCYLLA_HOSTS"):
            config.scylla.hosts = hosts.split(",")
        if redis_host := os.getenv("REDIS_HOST"):
            config.redis.host = redis_host
        if vector_provider := os.getenv("VECTOR_DB_PROVIDER"):
            config.vector_db.provider = vector_provider
        if model_name := os.getenv("MODEL_NAME"):
            config.model.model_name = model_name
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "scylla": vars(self.scylla),
            "redis": vars(self.redis),
            "vector_db": vars(self.vector_db),
            "offline_storage": {
                **vars(self.offline_storage),
                "db_path": str(self.offline_storage.db_path)
            },
            "model": {
                **vars(self.model),
                "offline_model_path": str(self.model.offline_model_path) if self.model.offline_model_path else None
            },
            "ui": vars(self.ui),
            "consciousness": vars(self.consciousness),
            "graph_db": vars(self.graph_db),
            "app_name": self.app_name,
            "version": self.version,
            "debug": self.debug,
            "data_dir": str(self.data_dir),
            "log_dir": str(self.log_dir),
        }